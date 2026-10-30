"""Optional user-login launch and reuse of the local visual interface."""
from pathlib import Path
import base64
import hashlib
import json
import os
import plistlib
import subprocess
import sys
import time
from urllib.request import Request, urlopen


def state_dir():
    if os.environ.get('AURA_STATE_DIR'):
        return Path(os.environ['AURA_STATE_DIR']).expanduser().resolve()
    return Path(os.environ.get('LOCALAPPDATA') or os.environ.get('XDG_STATE_HOME') or
                Path.home() / '.local/state') / 'ViralTrac/Aura'


def launch_background(argv, product):
    """Explicit app launch, independent of an agent/terminal's process cleanup."""
    argv = list(map(str, argv))
    if os.name == 'nt':
        # Creating another child (even Start-Process or breakaway) can retain
        # an outer Windows job. The existing Windows process broker avoids it.
        if Path(argv[0]).with_name('pythonw.exe').is_file():
            argv[0] = str(Path(argv[0]).with_name('pythonw.exe'))
        quoted = lambda value: "'" + str(value).replace("'", "''") + "'"
        command = ("$e=[string[]](Get-ChildItem Env:|ForEach-Object{$_.Name+'='+$_.Value});"
            "$s=New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly -Property "
            "@{ShowWindow=[uint16]0;CreateFlags=[uint32]1024;EnvironmentVariables=$e};"
            "$r=Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=" +
            quoted(subprocess.list2cmdline(argv)) + ";CurrentDirectory=" + quoted(Path(product).resolve()) +
            ";ProcessStartupInformation=$s};if($r.ReturnValue -ne 0){throw 'AURA could not start in the background.'};$r.ProcessId")
        encoded = base64.b64encode(command.encode('utf-16-le')).decode('ascii')
        powershell = Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
        result = subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-EncodedCommand', encoded],
                                capture_output=True, text=True, check=True, timeout=20,
                                env=dict(os.environ, AURA_STATE_DIR=str(state_dir().resolve())),
                                creationflags=subprocess.CREATE_NO_WINDOW)
        return int(result.stdout.strip())
    state_dir().mkdir(parents=True, exist_ok=True)
    with (state_dir() / 'interface.log').open('ab') as output:
        process = subprocess.Popen(argv, cwd=product, stdin=subprocess.DEVNULL,
                                   stdout=output, stderr=output, start_new_session=True)
    return process.pid


def registration():
    if sys.platform == 'win32':
        return Path(os.environ['APPDATA']) / 'Microsoft/Windows/Start Menu/Programs/Startup/ViralTrac AURA.lnk'
    if sys.platform == 'darwin':
        return Path.home() / 'Library/LaunchAgents/com.viraltrac.aura.plist'
    if sys.platform.startswith('linux'):
        return Path(os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config') / 'autostart/viraltrac-aura.desktop'
    raise ValueError('Automatic startup is not available on this system.')


def status():
    try:
        target = registration()
    except (ValueError, KeyError):
        return {'supported':False, 'enabled':False}
    try:
        saved = json.loads((state_dir() / 'startup.json').read_text(encoding='utf-8'))
        owned = saved['sha256'] == hashlib.sha256(target.read_bytes()).hexdigest()
        return {'supported':True, 'enabled':owned, 'workspace':saved.get('workspace', ''), 'product':saved.get('product', '')}
    except (OSError, ValueError, KeyError, TypeError):
        return {'supported':True, 'enabled':False}


def configure(enabled, product, workspace, business='', extra=(), interpreter=None):
    target = registration()
    saved = state_dir() / 'startup.json'
    current = status()
    if target.exists() and not current['enabled']:
        raise ValueError('An existing AURA startup entry was changed elsewhere. Remove it in your system startup settings first.')
    if not enabled:
        if current['enabled']:
            target.unlink()
        saved.unlink(missing_ok=True)
        return status()
    product, workspace = Path(product).resolve(), Path(workspace).resolve()
    interpreter = Path(interpreter or sys.executable).resolve()
    if sys.platform == 'win32' and interpreter.with_name('pythonw.exe').is_file():
        interpreter = interpreter.with_name('pythonw.exe')
    argv = [str(interpreter), '-E', '-s', '-B', str(product / 'scripts/open_aura.py'),
            '--no-open', '--workspace', str(workspace), '--local-state', str(state_dir().resolve()), *extra]
    if business:
        argv += ['--business-id', business]
    target.parent.mkdir(parents=True, exist_ok=True)
    state_dir().mkdir(parents=True, exist_ok=True)
    if sys.platform == 'win32':
        def quoted(value):
            return "'" + str(value).replace("'", "''") + "'"
        command = ("$s=(New-Object -ComObject WScript.Shell).CreateShortcut(" + quoted(target) + ");"
                   "$s.TargetPath=" + quoted(argv[0]) + ";$s.Arguments=" + quoted(subprocess.list2cmdline(argv[1:])) +
                   ";$s.WorkingDirectory=" + quoted(product) + ";$s.WindowStyle=7;"
                   "$s.Description='Start the local AURA interface';$s.Save()")
        encoded = base64.b64encode(command.encode('utf-16-le')).decode('ascii')
        powershell = Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
        subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-EncodedCommand', encoded],
                       check=True, timeout=15, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    elif sys.platform == 'darwin':
        target.write_bytes(plistlib.dumps({'Label':'com.viraltrac.aura', 'ProgramArguments':argv,
            'WorkingDirectory':str(product), 'RunAtLoad':True,
            'StandardOutPath':str(state_dir() / 'startup.log'),
            'StandardErrorPath':str(state_dir() / 'startup-error.log')}))
    else:
        def escaped(value):
            return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"').replace('`', '\\`').replace('$', '\\$').replace('%', '%%') + '"'
        target.write_text('[Desktop Entry]\nType=Application\nName=AURA\nTerminal=false\nExec=' +
                          ' '.join(map(escaped, argv)) + '\n', encoding='utf-8')
    target.chmod(0o600)
    saved.write_text(json.dumps({'workspace':str(workspace), 'product':str(product),
                                'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}), encoding='utf-8')
    return status()


class VisualInstance:
    """One normal launcher per product; explicit server invocations stay independent."""
    def __init__(self, product):
        identity = hashlib.sha256(str(Path(product).resolve()).encode()).hexdigest()[:16]
        self.path = state_dir() / ('running-' + identity + '.json')
        self.handle = None
        self.product = str(Path(product).resolve())

    def acquire(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.with_suffix('.lock').open('a+b')
        self.handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            if os.fstat(self.handle.fileno()).st_size == 0:
                self.handle.write(b'0'); self.handle.flush()
            self.handle.seek(0)
            try:
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                self.handle.close(); self.handle = None
                return False
        else:
            import fcntl
            try:
                fcntl.flock(self.handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                self.handle.close(); self.handle = None
                return False
        return True

    def existing(self):
        for _ in range(20):
            try:
                record = json.loads(self.path.read_text(encoding='utf-8'))
                port = int(record['port'])
                if not 1 <= port <= 65535:
                    raise ValueError('Invalid local port')
                url = 'http://127.0.0.1:' + str(port)
                request = Request(url + '/api/state', headers={'X-Aura-Token':record['token']})
                with urlopen(request, timeout=.5) as response:
                    data = json.load(response)
                if data['product'] == self.product:
                    return url + '/'
            except (OSError, ValueError, KeyError, TypeError):
                pass
            time.sleep(.15)
        raise ValueError('AURA is already starting. Wait a moment and open it again.')

    def publish(self, port, token):
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps({'port':port, 'token':token}), encoding='utf-8')
        temporary.chmod(0o600)
        temporary.replace(self.path)

    def close(self):
        if self.handle:
            self.path.unlink(missing_ok=True)
            self.handle.close()
            self.handle = None
