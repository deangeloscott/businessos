"""Control only the process tree started for one interface request."""
import os
import signal
import subprocess
import threading
import secrets


class Stopped(Exception):
    pass


class Execution:
    def __init__(self):
        self.stopped = threading.Event()
        self.lock = threading.Lock()
        self.process = None
        self.interactive = False
        self.permission = 'native'
        self.native_goal = None
        self.goal_control = None
        self.goal_cancelled = False
        self.retry_check_at = None
        self.retry_check = None
        self.on_started = None
        self.interrupt = None
        self.steer = None
        self.interrupt_requested = False
        self.native_options = {}
        self.child_model = ''
        self.native_handler = None
        self.native_cwd = None
        self.native_env = None
        self.attachments = []
        self.notices = []
        self.helpers = set()
        self.controls = {}
        self.native_session = None
        self.native_client_tools = None
        from workspace_interactions import Requests
        self.requests = Requests()

    def check(self):
        if self.stopped.is_set():
            raise Stopped()

    def control(self,send,value):
        ident='aura-control-'+secrets.token_hex(8);ready=threading.Event();result={}
        with self.lock:self.controls[ident]=(ready,result)
        try:
            send({**value,'id':ident})
            if not ready.wait(15):raise ValueError('The native app has not confirmed this update. Check the chat before sending it again.')
            if result.get('error'):raise ValueError(result['error'])
        finally:
            with self.lock:self.controls.pop(ident,None)

    def resolve_control(self,ident,error=None):
        with self.lock:
            row=self.controls.get(ident)
            if not row:return False
            ready,result=row
            if error:result['error']=str(error)
            ready.set();return True

    def close_controls(self):
        with self.lock:
            for ready,result in self.controls.values():
                result.setdefault('error','The native connection ended before confirming this update. Check the chat before sending it again.')
                ready.set()

    def popen(self, *args, **kwargs):
        with self.lock:
            self.check()
            if os.name == 'nt':
                kwargs['creationflags'] = kwargs.get('creationflags', 0) | subprocess.CREATE_NO_WINDOW
            else:
                kwargs['start_new_session'] = True
            self.process = subprocess.Popen(*args, **kwargs)
            self.native_cwd=kwargs.get('cwd');self.native_env=kwargs.get('env')
            process=self.process
            if self.native_session:
                self.native_session.process=process
                self.native_session.cwd=self.native_cwd;self.native_session.env=self.native_env
        if self.on_started:self.on_started(process)
        return process

    def stop(self):
        if self.native_session and (not self.native_session.active or self.native_session.active.execution is not self):return
        # Native cancellation gets the first chance to settle tools and children.
        # A timer supplies the process-tree fallback without holding the UI lock.
        with self.lock:
            if self.interrupt and not self.interrupt_requested and self.process and self.process.poll() is None:
                self.interrupt_requested=True
                try:self.interrupt()
                except (OSError,ValueError):pass
                else:
                    timer=threading.Timer(5,self._force_if_running);timer.daemon=True;timer.start()
                    return
        self._force_stop()

    def _force_if_running(self):
        with self.lock:
            if not self.process or self.process.poll() is not None:return
        self._force_stop()

    def _force_stop(self):
        with self.lock:
            if self.native_client_tools:self.native_client_tools.close()
            process = self.process
            self.stopped.set()
            for helper in list(self.helpers):
                if helper.poll() is None:helper.terminate()
            if process is None or process.poll() is not None:
                self.requests.close()
                return
            if os.name == 'nt':
                result = subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                                        capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode and process.poll() is None:
                    self.stopped.clear()
                    raise ValueError('The request could not be stopped. Open your AI app to stop it there.')
            else:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            self.requests.close()
