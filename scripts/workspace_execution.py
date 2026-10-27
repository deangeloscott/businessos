"""Control only the process tree started for one interface request."""
import os
import signal
import subprocess
import threading


class Stopped(Exception):
    pass


class Execution:
    def __init__(self):
        self.stopped = threading.Event()
        self.lock = threading.Lock()
        self.process = None

    def check(self):
        if self.stopped.is_set():
            raise Stopped()

    def popen(self, *args, **kwargs):
        with self.lock:
            self.check()
            if os.name == 'nt':
                kwargs['creationflags'] = kwargs.get('creationflags', 0) | subprocess.CREATE_NO_WINDOW
            else:
                kwargs['start_new_session'] = True
            self.process = subprocess.Popen(*args, **kwargs)
            return self.process

    def stop(self):
        with self.lock:
            process = self.process
            self.stopped.set()
            if process is None or process.poll() is not None:
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
