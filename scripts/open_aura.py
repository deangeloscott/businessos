#!/usr/bin/env python3
"""Launch the normal optional interface with the interpreter shipped beside it."""
import os
from pathlib import Path
import runpy
import sys


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
        argv = [str(workspace_updates.bundled_python(target)), '-E', '-s', '-B',
                str(target / 'scripts/open_aura.py'), *sys.argv[1:]]
        return subprocess.call(argv)
    if not any(a == '--workspace' or a.startswith('--workspace=') for a in sys.argv) and not os.environ.get('BUSINESSOS_WORKSPACE') and not os.environ.get('BUSINESSOS_WORKSPACE_CONFIG'):
        import workspace_catalog
        sys.argv += ['--workspace', str(workspace_catalog.launch_workspace(root))]
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
        pid = workspace_startup.launch_background(
            [sys.executable, '-E', '-s', '-B', str(root / 'scripts/open_aura.py'), *arguments], root)
        print('AURA is opening in the background (process ' + str(pid) + ').', flush=True)
        return 0
    # Clicking the launcher again opens the running view instead of starting
    # another copy. Explicit workspace_ui.py servers remain independent.
    if '--reuse' not in sys.argv:
        sys.argv.append('--reuse')
    runpy.run_path(str(root / 'scripts/workspace_ui.py'), run_name='__main__')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
