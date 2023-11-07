/**
 * The Python Interface for JavaScript
 */

const util = require('util')
if (typeof performance === 'undefined') var { performance } = require('perf_hooks')
const log = () => { }
const errors = require('./errors')
// use REQ_TIMEOUT env var value if parseable as integer, otherwise default to 100000 (ms)
const REQ_TIMEOUT = parseInt(process.env.REQ_TIMEOUT) || 100000

class BridgeException extends Error {
  constructor (...a) {
    super(...a)
    this.message += ` Python didn't respond in time (${REQ_TIMEOUT}ms), look above for any Python errors. If no errors, the API call hung.`
    // We'll fix the stack trace once this is shipped.
  }
}

class PythonException extends Error {
  constructor (stack, error) {
    super()
    const failedCall = stack.join('.')
    const trace = this.stack.split('\n').slice(1).join('\n')

    // Stack is generated at runtime when (and if) the error is printed
    Object.defineProperty(this, 'stack', {
      get: () => errors.getErrorMessage(failedCall, trace, error || this.pytrace)
    })
  }

  setPythonTrace (value) {
    // When the exception is thrown, we don't want this to be printed out.
    // We could also use new class "hard-privates"
    Object.defineProperty(this, 'pytrace', { enumerable: false, value })
  }
}

async function waitFor (cb, withTimeout, onTimeout) {
  let t
  if (withTimeout === Infinity) return new Promise(resolve => cb(resolve))
  const ret = await Promise.race([
    new Promise(resolve => cb(resolve)),
    new Promise(resolve => { t = setTimeout(() => resolve('timeout'), withTimeout) })
  ])
  clearTimeout(t)
  if (ret === 'timeout') onTimeout()
  return ret
}

const SnowflakeMode = {
  //A unique "mode" Enum for generating a unique snowflake based on the desired request.
  pyrid: 0,
  jsffid: 1,
  jsrid: 2,
  pyffid: 3,
};
function generateSnowflake(parameter, mode = SnowflakeMode.jsrid) {
  /*
    Generates a unique snowflake value based on the current timestamp
    and a passed in 'mode' parameter.

    Args:
        parameter(int): integer from 0-131071.
        mode(int,SnowflakeMode): Determines which type of snowflake to generate.  
        The nodejs side of the bridge only uses SnowflakeMode.jsffid and SnowflakeMode.jsrid

    
    */
  // Validate that parameter is within the 0-131071 (0x1FFFF) range, use a modulo if it isn't.
  let param=parameter
  if (!(param >= 0 && param <= 0x1FFFF)) {
    param=param% (0x20000)
    //throw new Error("Parameter value must be in the range [0, 131071]");
  }
  
  const timestamp = Math.floor(Date.now()/1000) & 0xFFFFFFFF;  // Get the current time in SECONDS, and limit it to 32 bits.
  const snowflake = (timestamp << 20) | ((mode & 0x07) << 17) | (param & 0x1FFFF);  // Combine timestamp, mode, and parameter
  return snowflake;
}

let nextReqId = 10000
//function nextReq(){  return generateSnowflake(nextReqId++)}
const nextReq = () => generateSnowflake(nextReqId++)


class PyBridge {
  constructor (com, jsi) {
    this.com = com
    // This is a ref map used so Python can call back JS APIs
    this.jrefs = {}
    this.jsi = jsi

    // We don't want to GC things individually, so batch all the GCs at once
    // to Python
    this.freeable = []
    this.loop = setInterval(this.runTasks, 1000)

    // This is called on GC
    this.finalizer = new FinalizationRegistry(ffid => {
      this.freeable.push(ffid)
      // Once the Proxy is freed, we also want to release the pyClass ref
      delete this.jsi.m[ffid]
    })
    globalThis.JSPyBridge = {
      
      python: this.makePyObject(0).python
    }
  }

  runTasks = () => {
    if (this.freeable.length) this.free(this.freeable)
    this.freeable = []
  }

  end () {
    clearInterval(this.loop)
  }

  request (req, cb) {
    // When we call Python functions with Proxy paramaters, we need to just send the FFID
    // so it can be mapped on the python side.
    req.c = 'pyi'
    this.com.write(req, cb)
  }

  async len (ffid, stack) {
    const req = { r: nextReq(), action: 'length', ffid: ffid, key: stack, val: '' }
    const resp = await waitFor(cb => this.request(req, cb), REQ_TIMEOUT, () => {
      throw new BridgeException(`Attempt to access '${stack.join('.')}' failed.`)
    })
    if (resp.key === 'error') throw new PythonException(stack, resp.sig)
    return resp.val
  }

  async get (ffid, stack, args, suppressErrors) {
    const req = { r: nextReq(), action: 'get', ffid: ffid, key: stack, val: args }

    const resp = await waitFor(cb => this.request(req, cb), REQ_TIMEOUT, () => {
      throw new BridgeException(`Attempt to access '${stack.join('.')}' failed.`)
    })
    if (resp.key === 'error') {
      if (suppressErrors) return undefined
      throw new PythonException(stack, resp.sig)
    }
    switch (resp.key) {
      case 'string':
      case 'int':
        return resp.val // Primitives don't need wrapping
      default: {
        const py = this.makePyObject(resp.val, resp.sig)
        this.queueForCollection(resp.val, py)
        return py
      }
    }
  }

  // This does a function call to Python. We assign the FFIDs, so we can assign them and send the call to Python.
  // We also need to keep track of the Python objects so we can GC them.
  async call (ffid, stack, args, kwargs, set, timeout) {
    const r = nextReq()
    //console.log('callffid',ffid, stack, args, kwargs, set, timeout)
    const req = { r, c: 'pyi', action: set ? 'setval' : 'pcall', ffid: ffid, key: stack, val: [args, kwargs] }
    const payload = JSON.stringify(req, (k, v) => {

      if (!k) return v
      if (v && !v.r) {
        if (v.ffid) return { ffid: v.ffid }
        if (
          typeof v === 'function' ||
          (typeof v === 'object' && (v.constructor.name !== 'Object' && v.constructor.name !== 'Array'))
        ) {

          //console.log(this.jsi.ffid);
          const ffid = this.jsi.ffidinc();
          //console.log(ffid);
          this.jsi.m[ffid] = v;
          this.queueForCollection(ffid, v);
          return { ffid }
        }
      }
      return v
    })

    const stacktrace = new PythonException(stack)
    const resp = await waitFor(resolve => this.com.writeRaw(payload, r, resolve), timeout || REQ_TIMEOUT, () => {
      throw new BridgeException(`Attempt to access '${stack.join('.')}' failed.`)
    })
    if (resp.key === 'error') {
      stacktrace.setPythonTrace(resp.sig)
      throw stacktrace
    }

    if (set) {
      return true // Do not allocate new FFID if setting
    }

    log('call', ffid, stack, args, resp)
    switch (resp.key) {
      case 'string':
      case 'int':
        return resp.val // Primitives don't need wrapping
      default: {
        const py = this.makePyObject(resp.val, resp.sig)
        this.queueForCollection(resp.val, py)
        return py
      }
    }
  }

  async value (ffid, stack) {
    const req = { r: nextReq(), action: 'value', ffid: ffid, key: stack, val: '' }
    const resp = await waitFor(cb => this.request(req, cb), REQ_TIMEOUT, () => {
      throw new BridgeException(`Attempt to access '${stack.join('.')}' failed.`)
    })
    if (resp.key === 'error') throw new PythonException(stack, resp.sig)
    return resp.val
  }

  async inspect (ffid, stack) {
    const req = { r: nextReq(), action: 'inspect', ffid: ffid, key: stack, val: '' }
    const resp = await waitFor(cb => this.request(req, cb), REQ_TIMEOUT, () => {
      throw new BridgeException(`Attempt to access '${stack.join('.')}' failed.`)
    })
    if (resp.key === 'error') throw new PythonException(stack, resp.sig)
    return resp.val
  }

  async free (ffids) {
    const req = { r: nextReq(), action: 'free', ffid: '', key: '', val: ffids }
    this.request(req)
    return true
  }

  queueForCollection (ffid, val) {
    this.finalizer.register(val, ffid)
  }

  makePyObject (ffid, inspectString) {
    const self = this
    // "Intermediate" objects are returned while chaining. If the user tries to log
    // an Intermediate then we know they forgot to use await, as if they were to use
    // await, then() would be implicitly called where we wouldn't return a Proxy, but
    // a Promise. Must extend Function to be a "callable" object in JS for the Proxy.
    class Intermediate extends Function {
      constructor (callstack) {
        super()
        this.callstack = [...callstack]
      }

      [util.inspect.custom] () {
        return '\n[You must use await when calling a Python API]\n'
      }
    }
    const handler = {
      get: (target, prop, reciever) => {
        const next = new Intermediate(target.callstack)
        // log('```prop', next.callstack, prop)
        if (prop === '$$') return target
        if (prop === 'ffid') return ffid
        if (prop === 'toJSON') return () => ({ ffid })
        if (prop === 'toString' && inspectString) return target[prop]
        if (prop === 'then') {
          // Avoid .then loops
          if (!next.callstack.length) {
            return undefined
          }
          return (resolve, reject) => {
            this.get(ffid, next.callstack, []).then(resolve).catch(reject)
            next.callstack = [] // Empty the callstack afer running fn
          }
        }
        if (prop === 'length') return this.len(ffid, next.callstack, [])
        if (typeof prop === 'symbol') {
          if (prop === Symbol.iterator) {
            // This is just for destructuring arrays
            return function * iter () {
              for (let i = 0; i < 100; i++) {
                const next = new Intermediate([...target.callstack, i])
                yield new Proxy(next, handler)
              }
              throw SyntaxError('You must use `for await` when iterating over a Python object in a for-of loop')
            }
          }
          if (prop === Symbol.asyncIterator) {
            return async function * iter () {
              const it = await self.call(0, ['Iterate'], [{ ffid }])
              while (true) {
                const val = await it.Next()
                if (val === '$$STOPITER') {
                  return
                } else {
                  yield val
                }
              }
            }
          }
          log('Get symbol', next.callstack, prop)
          return
        }
        if (Number.isInteger(parseInt(prop))) prop = parseInt(prop)
        next.callstack.push(prop)
        return new Proxy(next, handler) // no $ and not fn call, continue chaining
      },
      apply: (target, self, args) => { // Called for function call
        const final = target.callstack[target.callstack.length - 1]
        let kwargs, timeout
        if (final === 'apply') {
          target.callstack.pop()
          args = [args[0], ...args[1]]
        } else if (final === 'call') {
          target.callstack.pop()
        } else if (final?.endsWith('$')) {
          kwargs = args.pop()
          timeout = kwargs.$timeout
          delete kwargs.$timeout
          target.callstack[target.callstack.length - 1] = final.slice(0, -1)
        } else if (final === 'valueOf') {
          target.callstack.pop()
          const ret = this.value(ffid, [...target.callstack])
          return ret
        } else if (final === 'toString') {
          target.callstack.pop()
          const ret = this.inspect(ffid, [...target.callstack])
          return ret
        }
        const ret = this.call(ffid, target.callstack, args, kwargs, false, timeout)
        target.callstack = [] // Flush callstack to py
        return ret
      },
      set: (target, prop, val) => {
        if (Number.isInteger(parseInt(prop))) prop = parseInt(prop)
        const ret = this.call(ffid, [...target.callstack], [prop, val], {}, true)
        return ret
      }
    }
    // A CustomLogger is just here to allow the user to console.log Python objects
    // since this must be sync, we need to call inspect in Python along with every CALL or GET
    // operation, which does bring some small overhead.
    class CustomLogger extends Function {
      constructor () {
        super()
        this.callstack = []
      }

      [util.inspect.custom] () {
        return inspectString || '(Some Python object)'
      }
    }
    return new Proxy(new CustomLogger(), handler)
  }
}

module.exports = { PyBridge, SnowflakeMode,generateSnowflake }
