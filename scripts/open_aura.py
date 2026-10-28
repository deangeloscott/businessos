#!/usr/bin/env python3
"""Launch the normal optional interface with the interpreter shipped beside it."""
import os
from pathlib import Path
import runpy
import sys


def main():
    root = Path(__file__).resolve().parents[1]
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
    sys.path.insert(0, str(root / 'scripts'))
    if not any(a == '--workspace' or a.startswith('--workspace=') for a in sys.argv) and not os.environ.get('BUSINESSOS_WORKSPACE') and not os.environ.get('BUSINESSOS_WORKSPACE_CONFIG'):
        import workspace_catalog
        sys.argv += ['--workspace', str(workspace_catalog.launch_workspace(root))]
    # Clicking the launcher again opens the running view instead of starting
    # another copy. Explicit workspace_ui.py servers remain independent.
    if '--reuse' not in sys.argv:
        sys.argv.append('--reuse')
    runpy.run_path(str(root / 'scripts/workspace_ui.py'), run_name='__main__')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
