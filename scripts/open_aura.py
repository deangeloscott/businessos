#!/usr/bin/env python3
"""Launch the normal optional interface with the interpreter shipped beside it."""
import os
from pathlib import Path
import runpy
import sys


def alive(pid):
    """Whether the background AURA is still running (so a quick failure is reported at once, not after the wait)."""
    if os.name == 'nt':
        import ctypes
        kernel = ctypes.windll.kernel32
        handle = kernel.OpenProcess(0x1000, False, pid)  # query-only access
        if not handle:return False
        code = ctypes.c_ulong()
        try:kernel.GetExitCodeProcess(handle, ctypes.byref(code))
        finally:kernel.CloseHandle(handle)
        return code.value == 259  # still running
    try:return os.waitpid(pid, os.WNOHANG)[0] == 0
    except ChildProcessError:return False


def opened(workspace_startup, pid, wait=90):
    """Wait for the AURA started in the background to answer (it opens the browser itself), then say so. If it
    doesn't, show what it reported, so the person isn't left with nothing."""
    import time
    running, until, found = workspace_startup.RunningAura(Path(__file__).resolve().parents[1]), time.monotonic() + wait, None
    while not found and time.monotonic() < until:
        found = running.running(wait=1)
        # A background AURA that has finished without answering failed, unless it handed over to one already open.
        if not found and not alive(pid):found = running.running(wait=2);break
    if found:
        print('AURA is open in your browser (' + found['url'] + '). It keeps running when this window closes; '
              'to stop it, choose Quit AURA in its Settings.', flush=True)
        return 0
    print("AURA didn't open. What it reported:", flush=True)
    try:
        lines = (workspace_startup.state_dir() / 'interface.log').read_text(encoding='utf-8', errors='replace').splitlines()
        print('\n'.join(lines[-12:]) or '(nothing yet)', flush=True)
    except OSError:
        print('(nothing yet)', flush=True)
    return 1


def main():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / 'scripts'))
    if '--local-state' in sys.argv:
        pos = sys.argv.index('--local-state')
        if pos + 1 >= len(sys.argv):
            raise ValueError('Choose the local AURA settings folder.')
        os.environ['AURA_STATE_DIR'] = str(Path(sys.argv[pos + 1]).expanduser().resolve())
        del sys.argv[pos:pos + 2]
    # A desktop launch has no console. Keep startup errors available locally
    # instead of letting pythonw discard them. Never log requests or credentials.
    # Opened with no window of its own (the Start menu shortcut); a window that started it reports problems itself.
    desktop = sys.stdout is None and '--no-open' not in sys.argv and os.environ.pop('AURA_OPENED_FROM_WINDOW', '') != '1'
    if sys.stdout is None or sys.stderr is None:
        import time
        from workspace_startup import state_dir
        folder = state_dir(); folder.mkdir(parents=True, exist_ok=True)
        log = folder / 'interface.log'
        if log.exists() and log.stat().st_size > 2 * 1024 * 1024:
            log.replace(folder / 'interface-previous.log')
        stream = log.open('a', encoding='utf-8', buffering=1)
        if sys.stdout is None: sys.stdout = stream
        if sys.stderr is None: sys.stderr = stream
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' Opening AURA', flush=True)
    # Ignore another Python installation's configuration, only in this process.
    for name in ('PYTHONHOME', 'PYTHONPATH', 'PYTHONUSERBASE', 'PYTHONSTARTUP'):
        os.environ.pop(name, None)
    os.environ['PYTHONUTF8'] = '1'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    os.environ['PYTHONNOUSERSITE'] = '1'
    os.environ['PATH'] = os.pathsep.join(filter(None, [os.environ.get('PATH'), str(Path(sys.executable).parent)]))
    try:
        import yaml
        import jsonschema
    except ImportError:
        print('AURA’s required files are missing. Extract the complete bundled download and open AURA again.', file=sys.stderr)
        return 1
    import workspace_updates
    bypass = os.environ.pop('AURA_UPDATE_HANDOFF', '') == '1'
    target = None if bypass else workspace_updates.launch_target(root)
    if target:
        import subprocess
        argv = [str(workspace_updates.bundled_python(target)), '-X', 'utf8', '-E', '-s', '-B',
                str(target / 'scripts/open_aura.py'), *sys.argv[1:]]
        return subprocess.call(argv)
    if not any(a == '--workspace' or a.startswith('--workspace=') for a in sys.argv) and not os.environ.get('BUSINESSOS_WORKSPACE') and not os.environ.get('BUSINESSOS_WORKSPACE_CONFIG'):
        import workspace_catalog
        sys.argv += ['--workspace', str(workspace_catalog.launch_workspace(root))]
    # A person double-clicking Open AURA gets a window that runs this. AURA itself runs in the background, as it does
    # when it starts at sign-in, so closing that window doesn't close AURA; the window closes once AURA answers.
    # Starts that are already in the background (sign-in, updates, restarts) pass --no-open and have no console.
    # --foreground keeps the old behaviour, for running AURA from a terminal.
    person = False
    if '--foreground' in sys.argv:
        sys.argv.remove('--foreground')
    elif ('--no-open' not in sys.argv and '--background' not in sys.argv and
          sys.stdout is not None and sys.stdout.isatty() and sys.stdin is not None and sys.stdin.isatty()):
        person = True
        sys.argv.append('--background')
    if '--background' in sys.argv:
        import workspace_startup
        import hashlib
        if '--workspace' in sys.argv:
            workspace = Path(sys.argv[sys.argv.index('--workspace') + 1]).expanduser().resolve()
            identity = hashlib.sha256(str(workspace).encode()).hexdigest()[:20]
            preferences = workspace_startup.state_dir() / (identity + '.json')
            if preferences.is_file():
                # Store-packaged launchers can redirect individual AppData files.
                # Resolve the existing file, not a merged virtual directory.
                os.environ['AURA_STATE_DIR'] = str(preferences.resolve().parent)
        arguments = [a for a in sys.argv[1:] if a != '--background']
        if person:
            print('Opening AURA…', flush=True)
            os.environ['AURA_OPENED_FROM_WINDOW'] = '1'
        pid = workspace_startup.launch_background(
            [sys.executable, '-X', 'utf8', '-E', '-s', '-B', str(root / 'scripts/open_aura.py'), *arguments], root)
        if not person:
            print('AURA is opening in the background (process ' + str(pid) + ').', flush=True)
            return 0
        return opened(workspace_startup, pid)
    # Clicking the launcher again opens the running view instead of starting
    # another copy. Explicit workspace_ui.py servers remain independent.
    if '--reuse' not in sys.argv:
        sys.argv.append('--reuse')
    try:
        runpy.run_path(str(root / 'scripts/workspace_ui.py'), run_name='__main__')
    except BaseException as error:
        # Opened from the Start menu with no window: say so on screen instead of only in the log.
        if desktop and os.name == 'nt' and not isinstance(error, KeyboardInterrupt) and getattr(error, 'code', 1) not in (0, None):
            import ctypes
            from workspace_startup import state_dir
            ctypes.windll.user32.MessageBoxW(None, "AURA couldn't open. What happened is in " + str(state_dir() / 'interface.log') + '.',
                                             'AURA', 0x10)
        raise
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
