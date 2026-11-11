#!/usr/bin/env python3
"""Real terminals for AURA's side panel, using each system's own pseudo-terminal.

Windows uses its built-in pseudo console (ConPTY, the same system feature Windows Terminal
uses) through ctypes; macOS and Linux use Python's standard pty support. Nothing is installed.
A terminal runs as the signed-in user with the same power as the AI apps AURA already runs;
access goes only through AURA's token-protected local API. Terminals end when AURA stops.
"""
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid

MAX_TERMINALS = 8
KEEP_BYTES = 1_000_000      # Recent output kept for reconnecting panels.
TEXT_CHARS = 20_000         # Plain text kept for reading and automation.
ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[@-Z\\-_]|[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


def default_shell():
    if os.name == 'nt':
        return [shutil.which('pwsh') or shutil.which('powershell') or 'powershell.exe', '-NoLogo']
    return [os.environ.get('SHELL') or shutil.which('bash') or '/bin/sh']


def plain(text):
    """Terminal output as readable text: escape sequences removed, carriage returns resolved."""
    lines = []
    for line in ANSI.sub('', text.replace('\r\n', '\n')).split('\n'):
        lines.append(line.rsplit('\r', 1)[-1] if '\r' in line else line)
    return '\n'.join(lines)


class _Posix:
    def wait(self):self.process.wait()
    def close_console(self):pass

    def __init__(self, argv, cwd, env, cols, rows):
        import pty
        master, slave = pty.openpty()
        self._size(slave, cols, rows)
        # Acquire the slave in the new session before exec. Running this in a
        # fresh interpreter keeps preexec_fn out of the threaded server.
        acquire = 'import os,sys,fcntl,termios;fcntl.ioctl(0,termios.TIOCSCTTY,0);os.execvpe(sys.argv[1],sys.argv[1:],os.environ)'
        try:
            self.process = subprocess.Popen([sys.executable, '-c', acquire, *argv], stdin=slave,
                                            stdout=slave, stderr=slave, cwd=cwd, env=env,
                                            start_new_session=True, close_fds=True)
        except OSError:
            os.close(master)
            raise
        finally:
            os.close(slave)
        self.master = master

    @staticmethod
    def _size(fd, cols, rows):
        import fcntl, struct, termios
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack('HHHH', rows, cols, 0, 0))

    def read(self):
        try:return os.read(self.master, 65536)
        except OSError:return b''

    def write(self, data):os.write(self.master, data)
    def resize(self, cols, rows):self._size(self.master, cols, rows)
    def poll(self):return self.process.poll()

    def kill(self):
        import signal
        try:os.killpg(self.process.pid, signal.SIGHUP)
        except (OSError, ProcessLookupError):pass
        try:self.process.wait(2)
        except subprocess.TimeoutExpired:
            try:os.killpg(self.process.pid, signal.SIGKILL)
            except (OSError, ProcessLookupError):pass

    def close(self):
        try:os.close(self.master)
        except OSError:pass


class _Windows:
    """ConPTY: CreatePseudoConsole plus a process started with that console attached."""

    def __init__(self, argv, cwd, env, cols, rows):
        import ctypes
        from ctypes import wintypes as wt
        self.ctypes, self.wt = ctypes, wt
        k = self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

        class COORD(ctypes.Structure):_fields_ = [('X', wt.SHORT), ('Y', wt.SHORT)]

        class STARTUPINFOW(ctypes.Structure):
            _fields_ = [('cb', wt.DWORD), ('lpReserved', wt.LPWSTR), ('lpDesktop', wt.LPWSTR), ('lpTitle', wt.LPWSTR),
                        ('dwX', wt.DWORD), ('dwY', wt.DWORD), ('dwXSize', wt.DWORD), ('dwYSize', wt.DWORD),
                        ('dwXCountChars', wt.DWORD), ('dwYCountChars', wt.DWORD), ('dwFillAttribute', wt.DWORD),
                        ('dwFlags', wt.DWORD), ('wShowWindow', wt.WORD), ('cbReserved2', wt.WORD),
                        ('lpReserved2', ctypes.c_void_p), ('hStdInput', wt.HANDLE), ('hStdOutput', wt.HANDLE), ('hStdError', wt.HANDLE)]

        class STARTUPINFOEXW(ctypes.Structure):_fields_ = [('StartupInfo', STARTUPINFOW), ('lpAttributeList', ctypes.c_void_p)]

        class PROCESS_INFORMATION(ctypes.Structure):
            _fields_ = [('hProcess', wt.HANDLE), ('hThread', wt.HANDLE), ('dwProcessId', wt.DWORD), ('dwThreadId', wt.DWORD)]

        self.COORD = COORD
        k.CreatePseudoConsole.argtypes = [COORD, wt.HANDLE, wt.HANDLE, wt.DWORD, ctypes.POINTER(wt.HANDLE)]
        k.CreatePseudoConsole.restype = ctypes.c_long
        k.ResizePseudoConsole.argtypes = [wt.HANDLE, COORD];k.ResizePseudoConsole.restype = ctypes.c_long
        k.ClosePseudoConsole.argtypes = [wt.HANDLE];k.ClosePseudoConsole.restype = None
        k.CreatePipe.argtypes = [ctypes.POINTER(wt.HANDLE), ctypes.POINTER(wt.HANDLE), ctypes.c_void_p, wt.DWORD]
        k.InitializeProcThreadAttributeList.argtypes = [ctypes.c_void_p, wt.DWORD, wt.DWORD, ctypes.POINTER(ctypes.c_size_t)]
        k.UpdateProcThreadAttribute.argtypes = [ctypes.c_void_p, wt.DWORD, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p]
        k.DeleteProcThreadAttributeList.argtypes = [ctypes.c_void_p]
        k.CreateProcessW.argtypes = [wt.LPCWSTR, wt.LPWSTR, ctypes.c_void_p, ctypes.c_void_p, wt.BOOL, wt.DWORD, ctypes.c_void_p, wt.LPCWSTR,
                                     ctypes.POINTER(STARTUPINFOEXW), ctypes.POINTER(PROCESS_INFORMATION)]
        k.ReadFile.argtypes = [wt.HANDLE, ctypes.c_void_p, wt.DWORD, ctypes.POINTER(wt.DWORD), ctypes.c_void_p]
        k.WriteFile.argtypes = [wt.HANDLE, ctypes.c_void_p, wt.DWORD, ctypes.POINTER(wt.DWORD), ctypes.c_void_p]
        k.WaitForSingleObject.argtypes = [wt.HANDLE, wt.DWORD];k.WaitForSingleObject.restype = wt.DWORD
        k.GetExitCodeProcess.argtypes = [wt.HANDLE, ctypes.POINTER(wt.DWORD)]
        k.TerminateProcess.argtypes = [wt.HANDLE, wt.UINT]
        k.CloseHandle.argtypes = [wt.HANDLE]
        if not hasattr(k, 'CreatePseudoConsole'):raise OSError('This version of Windows has no pseudo console. Use your own terminal instead.')

        in_read, in_write, out_read, out_write = wt.HANDLE(), wt.HANDLE(), wt.HANDLE(), wt.HANDLE()
        if not k.CreatePipe(ctypes.byref(in_read), ctypes.byref(in_write), None, 0) or not k.CreatePipe(ctypes.byref(out_read), ctypes.byref(out_write), None, 0):
            raise ctypes.WinError(ctypes.get_last_error())
        self.console = wt.HANDLE()
        result = k.CreatePseudoConsole(COORD(cols, rows), in_read, out_write, 0, ctypes.byref(self.console))
        if result != 0:raise OSError(f'Windows could not create a terminal ({result & 0xffffffff:#x}).')
        size = ctypes.c_size_t()
        k.InitializeProcThreadAttributeList(None, 1, 0, ctypes.byref(size))
        self.attributes = ctypes.create_string_buffer(size.value)
        if not k.InitializeProcThreadAttributeList(self.attributes, 1, 0, ctypes.byref(size)):raise ctypes.WinError(ctypes.get_last_error())
        # PROC_THREAD_ATTRIBUTE_PSEUDOCONSOLE takes the console handle itself as its value.
        if not k.UpdateProcThreadAttribute(self.attributes, 0, 0x00020016, self.console, ctypes.sizeof(wt.HANDLE), None, None):
            raise ctypes.WinError(ctypes.get_last_error())
        info = STARTUPINFOEXW();info.StartupInfo.cb = ctypes.sizeof(STARTUPINFOEXW);info.lpAttributeList = ctypes.cast(self.attributes, ctypes.c_void_p)
        # Empty standard handles: without this, a child of a redirected parent (AURA's server)
        # writes to the parent's pipes instead of the pseudo console.
        info.StartupInfo.dwFlags = 0x00000100
        self.info = PROCESS_INFORMATION()
        command = ctypes.create_unicode_buffer(subprocess.list2cmdline(argv))
        block = None
        if env is not None:
            # Windows expects the block sorted by name, ignoring case.
            text = ''.join(f'{k_}={v}\0' for k_, v in sorted(env.items(), key=lambda kv: kv[0].upper()) if '=' not in k_ and '\0' not in str(v)) + '\0'
            block = ctypes.create_unicode_buffer(text, len(text))
        if not k.CreateProcessW(None, command, None, None, False, 0x00080000 | 0x00000400, block, cwd, ctypes.byref(info), ctypes.byref(self.info)):
            error = ctypes.get_last_error()
            k.ClosePseudoConsole(self.console)
            raise OSError(f'The terminal could not start {argv[0]} ({ctypes.FormatError(error).strip()}).')
        # The pseudo console now owns its ends of the pipes.
        k.CloseHandle(in_read);k.CloseHandle(out_write)
        self.input, self.output = in_write, out_read
        self.closed = False;self.console_closed = threading.Lock();self._console_open = True

    def read(self):
        buffer = self.ctypes.create_string_buffer(65536);count = self.wt.DWORD()
        if not self.kernel32.ReadFile(self.output, buffer, 65536, self.ctypes.byref(count), None):return b''
        return buffer.raw[:count.value]

    def write(self, data):
        count = self.wt.DWORD()
        if not self.kernel32.WriteFile(self.input, data, len(data), self.ctypes.byref(count), None):
            raise OSError('The terminal is no longer accepting input.')

    def resize(self, cols, rows):self.kernel32.ResizePseudoConsole(self.console, self.COORD(cols, rows))

    def poll(self):
        if self.kernel32.WaitForSingleObject(self.info.hProcess, 0) != 0:return None
        code = self.wt.DWORD();self.kernel32.GetExitCodeProcess(self.info.hProcess, self.ctypes.byref(code));return code.value

    def kill(self):
        if self.poll() is None:self.kernel32.TerminateProcess(self.info.hProcess, 1)

    def wait(self):
        self.kernel32.WaitForSingleObject(self.info.hProcess, 0xFFFFFFFF)

    def close_console(self):
        """The pseudo console keeps its output open after the program exits; closing it ends the reader."""
        with self.console_closed:
            if not self._console_open:return
            self._console_open = False
        self.kernel32.ClosePseudoConsole(self.console)

    def close(self):
        if self.closed:return
        self.closed = True
        self.close_console()
        for handle in (self.input, self.output, self.info.hProcess, self.info.hThread):self.kernel32.CloseHandle(handle)
        self.kernel32.DeleteProcThreadAttributeList(self.attributes)


class Terminal:
    def __init__(self, argv, cwd, env=None, cols=100, rows=30, title='Terminal', purpose='', on_change=None):
        self.id = uuid.uuid4().hex[:16];self.title = title;self.purpose = purpose;self.cwd = str(cwd);self.on_change = on_change or (lambda: None)
        self.started = time.time();self.ended = None;self.exit_code = None
        self.cols, self.rows = max(20, min(400, int(cols))), max(5, min(200, int(rows)))
        env = dict(os.environ if env is None else env);env.setdefault('TERM', 'xterm-256color');env['AURA_TERMINAL'] = '1'
        self.engine = (_Windows if os.name == 'nt' else _Posix)(list(argv), self.cwd, env, self.cols, self.rows)
        self.changed = threading.Condition();self.chunks = [];self.offset = 0;self.base = 0;self.text = ''
        self._decoder = __import__('codecs').getincrementaldecoder('utf-8')('replace')
        threading.Thread(target=self._pump, daemon=True, name='aura-terminal-'+self.id).start()
        threading.Thread(target=self._watch, daemon=True, name='aura-terminal-exit-'+self.id).start()

    def _watch(self):
        self.engine.wait()
        time.sleep(.3)  # Let the last output arrive before the console closes.
        self.engine.close_console()

    def _pump(self):
        while True:
            data = self.engine.read()
            if not data:break
            text = self._decoder.decode(data)
            with self.changed:
                self.chunks.append(text);self.offset += len(text);self.text = (self.text + text)[-TEXT_CHARS * 2:]
                while self.offset - self.base > KEEP_BYTES and len(self.chunks) > 1:self.base += len(self.chunks.pop(0))
                self.changed.notify_all()
            self.on_change()
        code = None
        for _ in range(40):
            code = self.engine.poll()
            if code is not None:break
            time.sleep(.05)
        with self.changed:
            self.ended = time.time();self.exit_code = code;self.changed.notify_all()
        self.on_change()
        self.engine.close()

    @property
    def alive(self):return self.ended is None

    def output(self, since=0, wait=0.0):
        deadline = time.monotonic() + max(0.0, min(float(wait), 25.0))
        with self.changed:
            while self.offset <= since and self.alive and time.monotonic() < deadline:
                self.changed.wait(deadline - time.monotonic())
            reset = since < self.base or since > self.offset
            start = self.base if reset else since
            joined = ''.join(self.chunks);data = joined[start - self.base:]
            return {'id': self.id, 'data': data, 'offset': self.offset, 'reset': reset, 'alive': self.alive, 'exit_code': self.exit_code}

    def write(self, data):
        if not self.alive:raise ValueError('This terminal has ended. Open a new one.')
        if not isinstance(data, str) or len(data) > 65536:raise ValueError('Send shorter terminal input.')
        self.engine.write(data.encode('utf-8'))

    def resize(self, cols, rows):
        self.cols, self.rows = max(20, min(400, int(cols))), max(5, min(200, int(rows)))
        if self.alive:self.engine.resize(self.cols, self.rows)

    def screen(self, chars=6000):
        """Recent output as plain text, for reading by the person's AI or by AURA's own steps."""
        with self.changed:return plain(self.text)[-int(chars):]

    def stop(self):
        if self.alive:self.engine.kill()

    def summary(self):
        return {'id': self.id, 'title': self.title, 'purpose': self.purpose, 'cwd': self.cwd, 'alive': self.alive,
                'exit_code': self.exit_code, 'started': self.started, 'ended': self.ended}


class Terminals:
    """The terminals one AURA process owns. They end with that process."""

    def __init__(self):
        self.items = {};self.lock = threading.Lock();self.changed = threading.Condition();self.version = 0

    def _changed(self):
        with self.changed:
            self.version += 1;self.changed.notify_all()

    def output_many(self, offsets, wait=0.0):
        """New output for any of several terminals, waiting on one connection until one has something.
        A browser keeps only about six connections per address, so one wait serves every open tab."""
        deadline = time.monotonic() + max(0.0, min(float(wait), 25.0))
        while True:
            with self.changed:seen = self.version
            items = []
            for ident, offset in offsets.items():
                with self.lock:terminal = self.items.get(ident)
                if not terminal:items.append({'id': ident, 'gone': True});continue
                if terminal.offset != offset or not terminal.alive or offset < terminal.base:items.append(terminal.output(offset, 0))
            remaining = deadline - time.monotonic()
            if items or remaining <= 0:return {'items': items}
            with self.changed:
                if self.version == seen:self.changed.wait(remaining)

    def start(self, argv=None, cwd=None, env=None, cols=100, rows=30, title='Terminal', purpose=''):
        cwd = os.path.abspath(cwd or os.path.expanduser('~'))
        if not os.path.isdir(cwd):raise ValueError('This folder is unavailable. Choose another folder for the terminal.')
        with self.lock:
            for ident in [i for i, t in self.items.items() if not t.alive and time.time() - (t.ended or 0) > 600]:self.items.pop(ident)
            if sum(t.alive for t in self.items.values()) >= MAX_TERMINALS:raise ValueError('Close a terminal before opening another one.')
        terminal = Terminal(argv or default_shell(), cwd, env, cols, rows, title, purpose, self._changed)
        with self.lock:self.items[terminal.id] = terminal
        return terminal

    def get(self, ident):
        with self.lock:terminal = self.items.get(str(ident))
        if not terminal:raise ValueError('This terminal is no longer available. Open a new one.')
        return terminal

    def remove(self, ident):
        terminal = self.get(ident);terminal.stop()
        with self.lock:self.items.pop(terminal.id, None)

    def list(self):
        with self.lock:return [t.summary() for t in sorted(self.items.values(), key=lambda t: t.started)]

    def stop_all(self):
        with self.lock:items = list(self.items.values())
        for terminal in items:
            try:terminal.stop()
            except OSError:pass


def wait_for(terminal, pattern, timeout=20.0, since_text=''):
    """Wait until the terminal's plain text matches; return the match or None. Never types anything."""
    deadline = time.monotonic() + timeout;compiled = re.compile(pattern, re.I | re.M);offset = 0
    while time.monotonic() < deadline:
        found = compiled.search(terminal.screen(TEXT_CHARS)[len(since_text):] if since_text else terminal.screen(TEXT_CHARS))
        if found:return found
        if not terminal.alive:return None
        offset = terminal.output(offset, min(1.0, max(0.05, deadline - time.monotonic())))['offset']
    return None



def available():
    """Whether this computer can run a built-in terminal. Otherwise AURA opens the person's own terminal."""
    if os.name == 'nt':
        try:
            import ctypes
            return hasattr(ctypes.WinDLL('kernel32'), 'CreatePseudoConsole')
        except OSError:return False
    try:
        import pty  # noqa: F401
        return True
    except ImportError:return False


TERMINALS = Terminals()


if __name__ == '__main__':
    # Manual check: run a command in a real terminal and print what it showed.
    terminals = Terminals()
    t = terminals.start(sys.argv[1:] or default_shell(), os.getcwd())
    end = time.monotonic() + 10
    while t.alive and time.monotonic() < end:t.output(t.offset, 1)
    print(t.screen());t.stop()
