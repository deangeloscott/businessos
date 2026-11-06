"""Live native conversations. Requests finish independently of their connection."""
import hashlib
import json
import math
import threading
import time


class Call:
    def __init__(self,prompt,native_id,execution,update):
        self.prompt=prompt;self.native_id=native_id;self.execution=execution;self.update=update
        self.ready=threading.Event();self.result=None;self.error=None


class Session:
    def __init__(self,signature,call,launch,workspace):
        self.signature=signature;self.lock=threading.RLock();self.closed=False
        self.last_activity=time.monotonic();self.goal_active=False;self.background=False;self.native_work=False;self.warming_until=0
        self.active=call;self.execution=call.execution;self.events=None;self.process=None
        self.requests=call.execution.requests;self.update=call.update
        self.native_id=call.native_id
        self.bind(call)
        def work():
            from _common import workspace_scope
            try:
                with workspace_scope(workspace):
                    result=launch()
                self.complete(result)
            except BaseException as error:
                with self.lock:
                    self.closed=True
                    if self.active:self.active.error=error;self.active.ready.set();self.active=None
            finally:
                with self.lock:
                    self.closed=True
                    if self.active:
                        self.active.error=ValueError('The native connection ended before confirming this request. Check the saved chat before sending it again.')
                        self.active.ready.set();self.active=None
                self.requests.close()
                self.execution.close_controls()
        self.worker=threading.Thread(target=work,daemon=True)

    def bind(self,call):
        self.active=call;self.execution=call.execution;self.update=call.update
        self.touch()
        call.execution.native_session=self;call.execution.requests=self.requests
        self.requests.changed=lambda rows:self.update(requests=rows)
        if self.process:
            call.execution.process=self.process
            call.execution.native_cwd=self.cwd
            call.execution.native_env=self.env
            if call.execution.on_started:call.execution.on_started(self.process)
        self.update(requests=self.requests.snapshot())

    def complete(self,result):
        with self.lock:
            if self.active:
                self.touch()
                if result and result.get('native_id'):self.native_id=result['native_id']
                self.active.result=result;self.active.ready.set();self.active=None

    def next(self,result,events,idle=lambda event:None):
        self.complete(result)
        for event in events:
            if isinstance(event,Call):
                with self.lock:self.bind(event)
                return event
            idle(event)
            if not isinstance(event,dict) or not str(event.get('type','')).startswith('cache_warming_'):self.touch()
        raise ValueError('The native connection ended. Your saved conversation is available; no message was resent.')

    def submit(self,call):
        with self.lock:
            if self.closed or not self.process or self.process.poll() is not None:raise ValueError('This native connection ended. Send your message again to reconnect.')
            if self.active:raise ValueError('This conversation is still working. Wait for its reply or send an update.')
            # Reserve before enqueueing so two API callers cannot claim one turn.
            self.active=call
            self.events.put(call)

    def close(self):
        self.closed=True
        self.execution._force_stop()

    def touch(self):self.last_activity=time.monotonic()

    def pending(self):
        return bool(self.active or self.goal_active or self.background or self.native_work or self.warming_until>time.monotonic() or self.execution.helpers or
                    self.execution.native_client_tools and self.execution.native_client_tools.busy() or
                    any(r['status']=='pending' for r in self.requests.snapshot()))


class Sessions:
    def __init__(self):self.lock=threading.RLock();self.items={}

    def busy(self):
        return any(not s.closed and s.pending() for s in list(self.items.values()))

    def owns_idle(self,key):
        session=self.items.get(key)
        return bool(session and not session.closed and session.active is None and session.process and session.process.poll() is None)

    def run(self,key,settings,prompt,native_id,execution,update,launch,workspace):
        signature=hashlib.sha256(json.dumps(settings,sort_keys=True,default=str).encode()).hexdigest()
        call=Call(prompt,native_id,execution,update)
        with self.lock:
            session=self.items.get(key)
            if session and (session.closed or session.signature!=signature or not session.process or session.process.poll() is not None):
                if not session.closed:
                    if session.pending():raise ValueError('Finish this conversation’s pending work before changing its connection.')
                    session.close()
                self.items.pop(key,None);session=None
            if session:session.submit(call)
            else:
                session=Session(signature,call,launch,workspace);self.items[key]=session;session.worker.start()
        call.ready.wait()
        if call.error:raise call.error
        return call.result

    def close(self):
        with self.lock:sessions=list(self.items.values());self.items.clear()
        for session in sessions:session.close()
        for session in sessions:session.worker.join(6)

    def release_idle(self,key,older_than=None):
        with self.lock:
            session=self.items.get(key)
            if not session:return False
            with session.lock:
                if session.pending() or older_than is not None and session.last_activity>older_than:return False
                session.closed=True
                self.items.pop(key,None)
        session.close()
        session.worker.join(6)
        return True

    def expire_idle(self,timeout=600):
        """Release settled connections, using the existing UI maintenance loop."""
        if not isinstance(timeout,(int,float)) or isinstance(timeout,bool) or not math.isfinite(timeout) or timeout<0:raise ValueError('Native idle timeout must be zero or a positive number of seconds.')
        if timeout==0:return 0
        cutoff=time.monotonic()-timeout
        with self.lock:keys=list(self.items)
        return sum(self.release_idle(key,older_than=cutoff) for key in keys)
