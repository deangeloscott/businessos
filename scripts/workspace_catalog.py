"""Small read-only workspace previews and machine-local recent selection."""
from pathlib import Path
import ctypes
import json
import os
import re
import sys

from workspace_startup import state_dir

SKIP = {'.git', '.aura-runtime', 'node_modules', '__pycache__', 'core', 'systems',
        'scripts', 'tests', 'generated', 'runtime', 'knowledge', 'attachments', 'instances', '.venv', 'venv'}


def read_json(path, default=None):
    try:
        if Path(path).stat().st_size > 4 * 1024 * 1024:
            raise ValueError('Workspace settings are too large.')
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError:
        return default


def write_json(path, data):
    from _common import write_json_atomic
    write_json_atomic(path,data)


def default_home():
    if os.environ.get('AURA_WORKSPACES_HOME'):
        return Path(os.environ['AURA_WORKSPACES_HOME']).expanduser().resolve()
    documents = Path.home() / 'Documents'
    if sys.platform == 'win32':
        buffer = ctypes.create_unicode_buffer(32768)
        if ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buffer) == 0:
            documents = Path(buffer.value)
    elif sys.platform.startswith('linux'):
        config = Path(os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config') / 'user-dirs.dirs'
        try:
            match = re.search(r'^XDG_DOCUMENTS_DIR="([^"]+)"', config.read_text(), re.M)
            if match:
                documents = Path(match[1].replace('$HOME', str(Path.home())))
        except OSError:
            pass
    return documents / 'AURA Workspaces'


def selection():
    try:
        data = read_json(state_dir() / 'workspace-selection.json', {})
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def remember(path, name, store=None):
    write_json(Path(store or state_dir()) / 'workspace-selection.json', {'path':str(Path(path).resolve()), 'name':name})


def organization_destination(row):
    stem=(row.get('businesses') or [{'id':row['name']}])[0]['id']
    stem=re.sub(r'[^a-z0-9_-]+','-',stem.lower()).strip('-')[:64] or 'workspace'
    for number in range(1,1000):
        path=default_home()/(stem+'-organized'+('' if number==1 else '-'+str(number)))
        if not path.exists():return str(path)
    raise ValueError('Choose another destination for your organized workspace.')


def preview(value, visited=None):
    folder = Path(value).expanduser().resolve()
    visited = set() if visited is None else visited
    if folder in visited or len(visited) >= 8:
        raise ValueError('This workspace link goes in a circle. Choose the folder holding the saved work.')
    visited.add(folder)
    row = {'path':str(folder), 'name':folder.name, 'businesses':[], 'version':'', 'kind':'unrecognized',
           'exists':folder.is_dir(), 'note':'', 'aliases':[]}
    if not folder.is_dir():
        row.update(kind='missing', note='This folder is missing or its drive is disconnected.')
        return row
    profile = read_json(folder / '.businessos/workspace.json', {})
    if not isinstance(profile, dict):
        raise ValueError('These workspace settings need attention. The folder was not changed.')
    if profile.get('workspace_root'):
        if not isinstance(profile['workspace_root'],str):
            raise ValueError('This workspace link needs attention.')
        linked = Path(os.path.expandvars(profile['workspace_root'])).expanduser()
        linked = linked if linked.is_absolute() else folder / linked
        if linked.resolve() != folder:
            found = preview(linked, visited)
            found['aliases'].append(str(folder))
            return found
    row['version'] = str(profile.get('product_version') or '')
    version = folder / 'VERSION'
    if version.is_file() and version.stat().st_size < 100:
        row['version'] = version.read_text(encoding='utf-8').strip()
    instances = folder / 'instances'
    if instances.is_dir():
        for child in sorted(instances.iterdir())[:500]:
            if not child.is_dir() or child.is_symlink() or child.name.startswith(('_', '.')):
                continue
            record = read_json(child / 'context/business.json') or read_json(child / 'instance.json')
            if isinstance(record, dict):
                row['businesses'].append({'id':child.name, 'name':str(record.get('name') or child.name)})
    if row['businesses']:
        row.update(kind='workspace', name=', '.join(b['name'] for b in row['businesses'])[:200])
    elif version.is_file() and (folder / 'scripts').is_dir():
        row.update(kind='application', note='AURA application only; no saved businesses were found here.')
    elif (folder / '.businessos/workspace.json').is_file():
        row.update(kind='empty', note='This workspace has no saved businesses yet.')
    return row


def discover(roots, depth=3, limit=800):
    pending = [(Path(p).expanduser(), 0) for p in roots]
    visited, found, notes = set(), {}, []
    while pending and len(visited) < limit:
        folder, level = pending.pop(0)
        try:
            if folder.is_symlink() or getattr(folder,'is_junction',lambda:False)() or not folder.is_dir():
                continue
            folder = folder.resolve()
            if folder in visited:
                continue
            visited.add(folder)
            row = preview(folder)
            if row['kind'] != 'unrecognized':
                key = os.path.normcase(row['path'])
                if key in found:
                    found[key]['aliases'] = sorted(set(found[key]['aliases'] + row['aliases']))
                else:
                    found[key] = row
            if row['kind'] == 'workspace' or level >= depth:
                continue
            for child in sorted(folder.iterdir()):
                if not child.name.startswith('.') and child.name.lower() not in SKIP and child.is_dir() and not child.is_symlink() and not getattr(child,'is_junction',lambda:False)():
                    pending.append((child, level + 1))
        except (OSError, ValueError, TypeError):
            notes.append('A folder could not be checked: ' + str(folder))
            if (folder / 'instances').is_dir() or (folder / '.businessos/workspace.json').is_file():
                found[os.path.normcase(str(folder))] = {'path':str(folder),'name':folder.name,
                    'businesses':[], 'version':'', 'kind':'attention', 'exists':True, 'aliases':[],
                    'note':'Some workspace records could not be read. Keep this folder and ask your AI to inspect it.'}
    if pending:
        notes.append('Search was limited. Choose a specific folder to look further.')
    return {'items':sorted(found.values(), key=lambda r:(r['kind'] != 'workspace', r['name'].casefold(), r['path'])),
            'notes':notes, 'checked':len(visited)}


def candidates(value):
    folder = Path(value).expanduser().resolve()
    row = preview(folder)
    if row['kind'] != 'unrecognized':
        return {'items':[row], 'notes':[]}
    # Users may select instances/, a business folder, or a ZIP's outer folder.
    for parent in list(folder.parents)[:3]:
        if (parent / 'instances').is_dir() and folder.is_relative_to(parent / 'instances'):
            found = preview(parent)
            if found['kind'] == 'workspace':
                return {'items':[found], 'notes':[]}
    return discover([folder], depth=3, limit=400)


def launch_workspace(product):
    product = Path(product).resolve()
    local = preview(product)
    if local['kind'] in {'workspace', 'missing'}:
        return Path(local['path'])
    previous = selection().get('path')
    if previous:
        # Retain a missing choice so the UI can offer repair, not an empty replacement.
        return Path(previous)
    return default_home() / 'My workspace'


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Preview existing AURA workspaces without changing them.')
    parser.add_argument('--path')
    parser.add_argument('--current',action='store_true')
    parser.add_argument('--json',action='store_true')
    args = parser.parse_args()
    if args.path:
        result = candidates(args.path)
    elif args.current:
        result = preview(launch_workspace(Path(__file__).resolve().parents[1]))
    else:
        prior = selection().get('path')
        result = discover([*([prior] if prior else []),default_home(),Path.home() / 'Downloads',Path.home() / 'Documents'])
    print(json.dumps(result,ensure_ascii=False,indent=2))
