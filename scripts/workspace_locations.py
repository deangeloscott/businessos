"""Explicit, read-only links to user-selected local files and folders."""
import json
import os
from pathlib import Path
import subprocess
import sys


def validate(value, workspace, businesses, bid, private):
    if not value.strip() or not Path(value).expanduser().is_absolute():
        raise ValueError('Choose a file or folder, or paste its full location.')
    path = Path(value).expanduser().resolve(strict=True)
    if path in {Path(path.anchor), Path.home().resolve(), workspace.resolve()}:
        raise ValueError('Choose a specific folder or file, rather than your whole computer or workspace.')
    if private(path) or not (path.is_dir() or path.is_file()):
        raise ValueError('Choose a regular file or folder outside private settings and credentials.')
    for business in businesses:
        if business['id'] != bid:
            for area in ('instances', 'knowledge', 'attachments', 'runtime/runs'):
                other = (workspace / area / business['id']).resolve()
                if path.is_relative_to(other) or other.is_relative_to(path):
                    raise ValueError('Choose files for this business, outside another business’s workspace.')
    return path


def resolve(ref, locations, private):
    parts = ref.split('/', 2)
    if len(parts) != 3:
        raise ValueError('Choose a linked file.')
    item = next((item for item in locations if item['id'] == parts[1]), None)
    relative = Path(parts[2])
    if not item or relative.is_absolute() or '..' in relative.parts or private(relative):
        raise ValueError('This file is outside your linked locations.')
    source = Path(item['path'])
    if source.resolve() != source:
        raise ValueError('This linked location has changed. Remove it and link the new location.')
    root = source if item['kind'] == 'folder' else source.parent
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or (item['kind'] == 'file' and path != source.resolve()):
        raise ValueError('This file is outside your linked location.')
    if not path.is_file():
        raise ValueError('This linked file is missing. Reconnect its folder if it moved.')
    return path


def entries(locations, private, media):
    out, statuses, limited = [], [], False
    for item in locations:
        source = Path(item['path'])
        statuses.append({**item, 'missing': not source.exists()})
        count = 0
        if not source.exists():
            continue
        def candidates():
            if item['kind'] == 'file':
                yield source.name
                return
            for directory, dirs, names in os.walk(source, followlinks=False):
                dirs[:] = sorted(d for d in dirs if not private(Path(d)) and not (Path(directory) / d).is_symlink())
                for name in sorted(names):
                    yield (Path(directory) / name).relative_to(source).as_posix()
        for relative in candidates():
            count += 1
            if count > 2000 or len(out) >= 1000:
                limited = True
                break
            ref = 'linked/' + item['id'] + '/' + relative
            try:
                path = resolve(ref, [item], private)
                stat = path.stat()
            except (ValueError, OSError):
                continue
            out.append({'path': ref, 'name': path.name, 'bytes': stat.st_size,
                        'modified': stat.st_mtime, 'media': path.suffix.lower() in media,
                        'location': item['id'], 'location_name': item['name'], 'local_path': str(path)})
    return {'items': out, 'locations': statuses, 'limited': limited}


def choose(kind):
    # The picker runs on its own UI thread/process, never the HTTP worker's thread.
    flags = {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
    result = subprocess.run([sys.executable, str(Path(__file__)), kind],
                            capture_output=True, text=True, encoding='utf-8', timeout=180, **flags)
    if result.returncode:
        raise ValueError('The file picker could not open. Paste the file or folder location instead.')
    return json.loads(result.stdout).get('path', '')


if __name__ == '__main__':
    import tkinter as tk
    from tkinter import filedialog
    window = tk.Tk()
    window.withdraw()
    window.attributes('-topmost', True)
    pick = filedialog.askdirectory if sys.argv[1] == 'folder' else filedialog.askopenfilename
    path = pick(parent=window, title='Link a folder to AURA' if sys.argv[1] == 'folder' else 'Link a file to AURA')
    window.destroy()
    print(json.dumps({'path': path}))
