"""Selected, attributed workspace snapshots. No sync service or second truth store.

The UI and CLI use the same inventory, package, review, apply and undo functions.
Incoming memory is source material, never silently adopted as recipient business truth.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from contextlib import contextmanager
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import zipfile

from _common import PRODUCT_ROOT, write_json_atomic
from canonical_store import INSTANCE_PATHS, validate_canonical
from migrate_workspace import _sha256
from workspace_organization import _refs
from validate_references import references_in
import workspace_catalog as catalog
import workspace_storage as storage
from workspace_startup import state_dir

FORMAT = 'aura-selected-share-1'
MAX_FILES, MAX_BYTES = 10000, 2 * 1024 ** 3
SECRET_FIELDS = {'password', 'api_key', 'apikey', 'access_token', 'refresh_token', 'private_key', 'credentials', 'secrets'}


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


@contextmanager
def destination_lock(target):
    """OS-owned lock releases on process exit; no stale PID or lease service."""
    target = unlinked(target)
    path = target.parent / ('.aura-share-' + digest(str(target))[:24] + '.lock')
    path.parent.mkdir(parents=True, exist_ok=True)
    with unlinked(path).open('a+b') as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(b'0'); handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise ValueError('Another transfer is using this destination. Wait for it to finish.') from None
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def safe(value):
    if not isinstance(value, str) or not value or re.search(r'[\\:<>"|?*\x00-\x1f]', value):
        raise ValueError('A shared file has an unsafe location.')
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in {'', '.', '..'} or part.endswith((' ', '.')) or
            re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', part) for part in value.split('/')):
        raise ValueError('A shared file has an unsafe location.')
    return Path(*p.parts)


def unlinked(path):
    """Reject links/junctions before resolving, including linked parent folders."""
    path = Path(path).absolute()
    for parent in (path, *path.parents):
        if parent.is_symlink() or getattr(parent, 'is_junction', lambda: False)():
            raise ValueError('A selected location is a folder link. Choose its original location explicitly.')
    return path.resolve()


def read(path, default=None):
    path = unlinked(path)
    if path.exists() and path.stat().st_size > 16 * 1024 ** 2:
        raise ValueError('This sharing record is too large. Choose a smaller selection.')
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return default


def business(root, bid):
    if not isinstance(bid, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', bid):
        raise ValueError('Choose a business for sharing.')
    root = unlinked(root)
    obj = read(root / 'instances' / bid / 'context/business.json')
    if not isinstance(obj, dict) or obj.get('business_id') != bid:
        raise ValueError('Choose an existing business in this workspace.')
    return obj


def objects(root, bid):
    business(root, bid)
    out = {}
    for kind, rel in INSTANCE_PATHS.items():
        base = Path(root) / 'instances' / bid / rel
        paths = [base] if base.suffix == '.json' else sorted(base.glob('*.json'))
        for path in paths:
            if not path.exists():
                continue
            obj = read(path)
            if not isinstance(obj, dict) or obj.get('object_type') != kind or obj.get('business_id') != bid:
                raise ValueError('A saved record needs attention before sharing: ' + path.name)
            validate_canonical(kind, obj)
            out[obj['id']] = (obj, path)
    return out


def title(obj):
    return str(obj.get('name') or obj.get('title') or obj.get('extensions', {}).get('businessos', {}).get('display_name') or
               obj.get('source_reference') or obj.get('business_role') or obj.get('summary') or obj.get('object_type', 'Saved information'))[:250]


def description(obj):
    for key in ('description','summary','purpose','statement','business_role'):
        value = obj.get(key)
        if isinstance(value,str) and value.strip() and value.strip()!=title(obj):
            text = ' '.join(value.split())
            return text[:197] + '…' if len(text)>200 else text
    return ''


def walk(path, notes, excluded=None):
    path = unlinked(path)
    exclusions = notes if excluded is None else excluded
    if not path.exists():
        notes.append('Missing: ' + path.name)
        return []
    if storage.private_file(path):
        exclusions.append('Private settings or credentials excluded: ' + path.name)
        return []
    if path.is_file():
        return [path]
    out = []
    def failed(error):
        raise ValueError('Some selected files cannot be read. Reconnect the folder before sharing.')
    for directory, dirs, names in os.walk(path, followlinks=False, onerror=failed):
        base = Path(directory)
        for name in list(dirs):
            child = base / name
            if name == '.sharing':
                dirs.remove(name)
                continue
            if storage.private_file(child) or child.is_symlink() or getattr(child, 'is_junction', lambda: False)():
                exclusions.append('Excluded folder: ' + name)
                dirs.remove(name)
        for name in sorted(names):
            child = base / name
            if child.is_symlink() or storage.private_file(child):
                exclusions.append('Excluded file: ' + name)
            else:
                out.append(child)
            if len(out) > MAX_FILES:
                raise ValueError('Choose fewer files for one transfer.')
    return out


def inventory(root, bid, locations=None):
    root = unlinked(root)
    objs = objects(root, bid)
    items, notes, excluded, seen = [], [], [], set()
    for oid, (obj, _) in objs.items():
        items.append({'key':'record:' + oid, 'kind':'record', 'title':title(obj), 'description':description(obj), 'type':obj['object_type'],
                      '_location_reference':obj.get('location_reference')})
    def add(path, label=None, explicit=False, support_only=False):
        path = Path(path).absolute()
        if path in seen:
            return
        seen.add(path)
        try:
            path = unlinked(path)
            if storage.private_file(path):
                return
            # Even explicitly connected folders may not disclose another business.
            for other in (root / 'instances').iterdir():
                if other.name != bid and other.is_dir() and any(path.is_relative_to(root / ns / other.name) or
                        (path.is_dir() and (root / ns / other.name).is_relative_to(path)) for ns in ('instances', 'attachments', 'knowledge', 'runtime/runs')):
                    return
            if path in {root, Path(path.anchor), Path.home().resolve()} or root.is_relative_to(path):
                return
            if not path.exists():
                notes.append('Missing: ' + (label or path.name))
                return
            rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else 'external/' + digest(str(path))[:16] + '/' + path.name
            key = ('folder:' if path.is_dir() else 'file:') + rel
            items.append({'key':key, 'kind':'folder' if path.is_dir() else 'file', 'title':label or path.name,
                          'location':rel, '_path':str(path), 'bytes':path.stat().st_size if path.is_file() else None,
                          '_support_only':support_only,
                          'external':not path.is_relative_to(root)})
        except (OSError, ValueError):
            notes.append('Unavailable or linked location: ' + (label or path.name))
    for base in (root / 'attachments' / bid, root / 'knowledge' / bid / 'notes'):
        if base.is_dir():
            for path in walk(base, notes, excluded):
                rel = path.relative_to(root).parts
                if len(rel)>4 and rel[:3]==('attachments',bid,'shared') and rel[4] in {'packages','records'}:
                    continue
                if len(items) > MAX_FILES:
                    raise ValueError('This business has too many items for one sharing view. Use the CLI with a smaller selection.')
                add(path)
                parent = path.parent
                while parent != base and parent.is_relative_to(base):
                    add(parent)
                    parent = parent.parent
    for obj, _ in objs.values():
        fields = ['location_reference'] if obj['object_type']=='Asset' else ['source_reference','content_hash_reference'] if obj['object_type']=='SourceRecord' else []
        for field in fields:
            ref = obj.get(field, '')
            if isinstance(ref,str) and ref and not re.match(r'^[a-zA-Z]+://', ref):
                path = Path(ref) if Path(ref).is_absolute() else root / ref
                if path.exists():
                    add(path, title(obj), True, obj['object_type']=='SourceRecord')
    for row in locations if locations is not None else storage.view_preferences(root).get('file_locations', {}).get(bid, []):
        add(row['path'], row.get('name'), True)
    return {'items':items, 'notes':sorted(set(notes))[:100], 'excluded':sorted(set(excluded))[:100]}


def public_inventory(root, bid, locations=None):
    inv = inventory(root, bid, locations)
    public = []
    by_path = {row['_path']:row for row in inv['items'] if row.get('_path') and not row.get('_support_only')}
    for row in inv['items']:
        if row.get('_support_only'):
            continue
        visible = {k:v for k,v in row.items() if not k.startswith('_')}
        if row.get('type')=='Asset':
            ref = row.get('_location_reference')
            if isinstance(ref,str) and ref and not re.match(r'^[a-zA-Z]+://',ref):
                path = (Path(ref) if Path(ref).is_absolute() else Path(root) / ref).resolve()
                related = by_path.get(str(path))
                if related:
                    visible.update(related_key=related['key'], file_kind=related['kind'], file_name=path.name,
                                   location=related['location'], bytes=related['bytes'], external=related['external'])
        public.append(visible)
    return {'items':public, 'notes':inv['notes'], 'excluded':inv['excluded'],
            'selections':history(root, bid)['selections']}


def metadata(root, bid):
    return Path(root) / 'attachments' / bid / '.sharing'


def recent_receipts(root, bid):
    paths = sorted((metadata(root,bid) / 'receipts').glob('*.json'), key=lambda p:p.stat().st_mtime_ns, reverse=True)[:40]
    return sorted((read(p) for p in paths), key=lambda r:r['created'], reverse=True)


def history(root, bid):
    business(root, bid)
    base = metadata(root, bid)
    receipts = recent_receipts(root, bid)
    return {'selections':read(base / 'selections.json', []),
            'imports':[{k:r[k] for k in ('id', 'name', 'origin', 'created', 'status', 'counts', 'notes') if k in r} for r in receipts],
            'last_destination':read(base / 'last-destination.json', {})}


def save_selection(root, bid, name, keys, note='', selection_id='', locations=None):
    name = str(name).strip()
    if not name or len(name) > 160 or not isinstance(keys, list) or not keys or len(keys) > MAX_FILES:
        raise ValueError('Name a non-empty selection of up to 10,000 items.')
    available = {r['key'] for r in inventory(root, bid, locations)['items']}
    if any(key not in available for key in keys):
        raise ValueError('Some selected items are no longer available. Refresh the selection.')
    with destination_lock(root):
        rows = history(root, bid)['selections']
        if selection_id and not any(r['id']==selection_id for r in rows):
            raise ValueError('This saved selection is no longer available. Start a new selection.')
        if any(r['name'].casefold()==name.casefold() and r['id']!=selection_id for r in rows):
            raise ValueError('A saved selection already uses that name. Choose it to update, or use a different name.')
        row = {'id':selection_id or uuid.uuid4().hex[:20], 'name':name, 'keys':list(dict.fromkeys(keys)), 'note':str(note)[:8000], 'updated':now()}
        rows = [row, *(r for r in rows if r['id'] != row['id'])][:100]
        write_json_atomic(metadata(root, bid) / 'selections.json', rows)
    return row


def remember_package(root, bid, path):
    """Remember locations, not duplicate archives or their contents."""
    business(root, bid)
    path = unlinked(path)
    location = path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path)
    with destination_lock(root):
        index = metadata(root, bid) / 'packages.json'
        rows = read(index, [])
        write_json_atomic(index, [location, *(p for p in rows if p!=location)][:100])


def discover_packages(root, bid, locations=None, folder=None):
    """Bounded metadata-only discovery. Import still verifies every archived byte."""
    root = unlinked(root)
    business(root, bid)
    if folder and not unlinked(folder).is_dir():
        raise ValueError('Choose an existing folder to look for packages.')
    known = [] if folder else read(metadata(root, bid) / 'packages.json', [])
    candidates = [Path(p) if Path(p).is_absolute() else root / p for p in known]
    locations = locations if locations is not None else storage.view_preferences(root).get('file_locations', {}).get(bid, [])
    roots = [(unlinked(folder), 4)] if folder else [(root, 0), (root / 'attachments' / bid, 4),
             (root / 'knowledge' / bid / 'notes', 3), (Path.home() / 'Downloads', 2),
             *((Path(row['path']), 3) for row in locations)]
    pending = [(path, 0, depth) for path, depth in roots]
    visited, seen, found, notes = set(), set(), [], []
    checked = 0
    while pending and len(visited)<400 and len(candidates)<200:
        path, level, depth = pending.pop(0)
        try:
            path = unlinked(path)
            if storage.private_file(path) or path.name=='.sharing':
                continue
            if path.is_file():
                if path.suffix.lower()=='.zip':candidates.append(path)
                continue
            if not path.is_dir() or path in visited:
                continue
            visited.add(path)
            with os.scandir(path) as children:
                for child in children:
                    checked += 1
                    if checked>20000:
                        break
                    childpath = Path(child.path)
                    if storage.private_file(childpath) or child.name=='.sharing' or child.is_symlink() or getattr(childpath,'is_junction',lambda:False)():
                        continue
                    if child.is_file() and childpath.suffix.lower()=='.zip':candidates.append(childpath)
                    elif level<depth and child.is_dir():pending.append((childpath,level+1,depth))
                    if len(candidates)>=200:break
        except (OSError, ValueError):
            notes.append('Could not check: ' + str(path))
        if checked>20000:break
    if pending or len(candidates)>=200 or checked>20000:
        notes.append('Search was limited. Choose a more specific folder to look further.')
    for path in candidates[:200]:
        try:
            path = unlinked(path)
            if path in seen or storage.private_file(path):continue
            seen.add(path)
            with zipfile.ZipFile(path) as archive:
                if 'innovation-package.json' in archive.namelist() and 'AURA-SHARE.json' not in archive.namelist():
                    from workspace_exchange import archive_manifest
                    from innovation_common import validate_package
                    archive_manifest(archive)
                    if archive.getinfo('innovation-package.json').file_size>2*1024**2:continue
                    contribution=json.loads(archive.read('innovation-package.json'))
                    validate_package(contribution,require_export_approval=True)
                    found.append({'path':str(path),'name':contribution['process']['title'],'origin':contribution['contributor'].get('display_name') or contribution['contributor'].get('pseudonym') or 'Community contributor','created':contribution['created_at'],'items':1,'bytes':path.stat().st_size})
                    continue
                manifest = _archive_manifest(archive)
                found.append({'path':str(path), 'name':manifest['name'], 'origin':manifest['origin']['name'],
                              'created':manifest['created'], 'items':len(manifest['items']), 'bytes':path.stat().st_size})
        except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, RuntimeError):
            if str(path) in {str(Path(p) if Path(p).is_absolute() else root / p) for p in known}:
                notes.append('A recent package is missing or unreadable: ' + path.name + '. Choose its current file location.')
    return {'items':sorted(found,key=lambda row:row['created'],reverse=True), 'notes':sorted(set(notes)),
            'folders':[str(path) for path,_ in roots]}


def imported_detail(root, bid, receipt_id):
    business(root, bid)
    if not re.fullmatch(r'[0-9]{8}T[0-9]{6}-[a-f0-9]{12}', str(receipt_id)):
        raise ValueError('Choose an import from this workspace’s sharing history.')
    receipt = read(metadata(root, bid) / 'receipts' / (receipt_id + '.json'))
    if not receipt:
        raise ValueError('This import is no longer available.')
    package_path = receipt.get('package_reference')
    manifest = read(Path(root) / safe(package_path), {}) if package_path else {}
    items = []
    for row in manifest.get('items', []):
        local = manifest.get('local_items', {}).get(row['key'])
        incoming = (Path(package_path).parent / safe(row['path'])).as_posix() if package_path else None
        item = {'title':row['title'], 'kind':row['kind'], 'action':manifest.get('local_actions',{}).get(row['key'])}
        for kind, rel in (('local',local), ('incoming',incoming)):
            path = unlinked(Path(root) / safe(rel)) if rel else None
            if path and not path.is_relative_to(Path(root).resolve() / 'attachments' / bid / 'shared'):
                raise ValueError('A shared item points outside this business. Keep the import for review.')
            item[kind + '_path'] = rel if path and path.is_file() else None
            item[kind + '_bytes'] = path.stat().st_size if path and path.is_file() else None
        items.append(item)
    return {**{k:receipt[k] for k in ('id', 'name', 'origin', 'status', 'created', 'counts')},
            'note':manifest.get('note',''), 'notes':receipt.get('notes',[]), 'package_reference':package_path,
            'items':items}


def _job(ident, store=None):
    if not re.fullmatch(r'[a-f0-9]{32}', str(ident)):
        raise ValueError('Choose an existing sharing review.')
    return unlinked(Path(store or state_dir()) / 'sharing' / ident)


def _secrets(value):
    if isinstance(value, dict):
        return any(str(k).lower() in SECRET_FIELDS or _secrets(v) for k,v in value.items())
    return isinstance(value, list) and any(_secrets(v) for v in value)


def prepare(root, bid, keys, name='', note='', store=None, locations=None):
    ident = uuid.uuid4().hex
    try:
        return _prepare(root, bid, keys, name, note, store, locations, ident)
    except Exception:
        job = _job(ident, store)
        if job.exists():
            shutil.rmtree(job)
        raise


def _prepare(root, bid, keys, name, note, store, locations, ident):
    root = unlinked(root)
    org = business(root, bid)
    inv = inventory(root, bid, locations)
    available = {r['key']:r for r in inv['items']}
    if not isinstance(keys, list) or not keys or len(keys) > MAX_FILES or any(k not in available for k in keys):
        raise ValueError('Choose available information, files, or folders to share.')
    job = _job(ident, store)
    payload = job / 'payload'
    payload.mkdir(parents=True)
    objs = objects(root, bid)
    origin = {'id':digest([org['id'], org.get('created_at'), read(root / 'instances' / bid / 'instance.json', {}).get('created_at')])[:32],
              'name':org['name'], 'business_id':bid}
    entries, inputs, notes, seen = [], [], [], set()
    chosen = set(keys)
    record_queue = [k[7:] for k in keys if k.startswith('record:')]
    while record_queue:
        oid = record_queue.pop(0)
        if oid in seen:
            continue
        seen.add(oid)
        obj, path = objs[oid]
        if _secrets(obj):
            raise ValueError('A selected record contains credential fields. Remove them before sharing: ' + title(obj))
        deps = sorted(ref for ref in references_in(obj) if ref in objs and ref != oid)
        record_queue.extend(ref for ref in deps if ref not in seen)
        original_bytes = path.read_bytes()
        if json.loads(original_bytes) != obj:
            raise ValueError('A selected record changed. Refresh the selection.')
        content = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
        rel = 'records/' + digest(oid)[:24] + '.json'
        (payload / safe(rel)).parent.mkdir(parents=True, exist_ok=True)
        (payload / safe(rel)).write_bytes(content)
        entries.append({'key':'record:' + oid, 'kind':'record', 'title':title(obj), 'type':obj['object_type'], 'path':rel,
                        'sha256':digest(content), 'bytes':len(content), 'supporting':'record:' + oid not in chosen,
                        'dependencies':['record:' + dep for dep in deps]})
        inputs.append({'path':str(path), 'sha256':digest(original_bytes)})
        fields = ['location_reference'] if obj['object_type']=='Asset' else ['content_hash_reference','source_reference'] if obj['object_type']=='SourceRecord' else []
        for field in fields:
            ref = obj.get(field, '')
            if ref and not re.match(r'^[a-zA-Z]+://', ref):
                original = (Path(ref) if Path(ref).is_absolute() else root / ref).resolve()
                item = next((r for r in inv['items'] if r.get('_path') == str(original)), None)
                if item:
                    chosen.add(item['key'])
                elif obj['object_type']=='Asset' or field=='content_hash_reference':
                    notes.append('File not included for ' + title(obj) + ': missing, private, or outside the permitted business.')
    file_keys = [k for k in chosen if not k.startswith('record:')]
    file_seen = set()
    folder_inputs = []
    for key in file_keys:
        row = available[key]
        path = Path(row['_path'])
        paths = walk(path, notes)
        if row['kind'] == 'folder':
            folder_inputs.append({'path':str(path), 'files':[str(p) for p in paths]})
        for file in paths:
            if file in file_seen:
                continue
            file_seen.add(file)
            if len(entries) >= MAX_FILES or sum(e['bytes'] for e in entries) + file.stat().st_size > MAX_BYTES:
                raise ValueError('Choose a smaller transfer (up to 10,000 files or 2 GB).')
            relative = file.relative_to(root).as_posix() if file.is_relative_to(root) else row['location'] + ('/' + file.relative_to(path).as_posix() if path.is_dir() else '')
            rel = 'files/' + relative
            target = payload / safe(rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            before = _sha256(unlinked(file))
            shutil.copyfile(file, target)
            if _sha256(file) != before or _sha256(target) != before:
                raise ValueError('A selected file changed. Review the selection again.')
            entries.append({'key':'file:' + relative, 'kind':'file', 'title':file.name, 'path':rel, 'sha256':before,
                            'bytes':target.stat().st_size, 'supporting':key not in keys, 'dependencies':[]})
            inputs.append({'path':str(file), 'sha256':before})
    if not entries:
        raise ValueError('There are no readable items in this selection.')
    if len(entries) > MAX_FILES or sum(e['bytes'] for e in entries) > MAX_BYTES:
        raise ValueError('Choose a smaller transfer (up to 10,000 files or 2 GB).')
    names = [e['path'].casefold() for e in entries]
    if len(set(names)) != len(names):
        raise ValueError('Some file names overlap on another computer. Rename them before sharing.')
    manifest = {'format':FORMAT, 'name':str(name or 'Shared work from ' + org['name'])[:160], 'origin':origin,
                'created':now(), 'note':str(note)[:8000], 'items':sorted(entries, key=lambda e:e['key']), 'notes':sorted(set(notes))}
    manifest['revision'] = digest({k:manifest[k] for k in ('name', 'origin', 'note', 'items', 'notes')})
    write_json_atomic(payload / 'AURA-SHARE.json', manifest)
    write_json_atomic(job / 'source.json', {'root':str(root), 'business':bid, 'keys':keys, 'inputs':inputs, 'folders':folder_inputs})
    return package_summary(ident, manifest)


def package_summary(ident, manifest):
    return {'id':ident, **{k:manifest[k] for k in ('name', 'origin', 'created', 'revision', 'note', 'notes')},
            'items':manifest['items'], 'bytes':sum(e['bytes'] for e in manifest['items'])}


def validate_manifest(manifest):
    """Validate portable metadata before using any path, identity, or allocation."""
    if not isinstance(manifest, dict) or manifest.get('format') != FORMAT:
        raise ValueError('Choose a supported AURA sharing package. Workspace backups use Back up or restore.')
    origin = manifest.get('origin')
    if (not isinstance(origin, dict) or not re.fullmatch(r'[a-f0-9]{32}', str(origin.get('id'))) or
            not isinstance(origin.get('name'), str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', str(origin.get('business_id')))):
        raise ValueError('This sharing package has no valid origin.')
    if any(not isinstance(manifest.get(k), str) for k in ('name','created','note','revision')) or len(manifest['note']) > 8000:
        raise ValueError('This package description is invalid.')
    items = manifest.get('items')
    if not isinstance(items, list) or not items or len(items) > MAX_FILES or not isinstance(manifest.get('notes'), list) or any(not isinstance(n,str) for n in manifest['notes']):
        raise ValueError('This sharing package has an invalid file list.')
    for item in items:
        if (not isinstance(item, dict) or item.get('kind') not in {'record','file'} or
                any(not isinstance(item.get(k),str) for k in ('key','title','path','sha256')) or
                not re.fullmatch(r'[a-f0-9]{64}', item['sha256']) or type(item.get('bytes')) is not int or item['bytes'] < 0 or
                not isinstance(item.get('dependencies'),list) or any(not isinstance(d,str) for d in item['dependencies'])):
            raise ValueError('A shared item has invalid metadata.')
        rel = safe(item['path'])
        if rel.parts[0] != ('records' if item['kind']=='record' else 'files') or len(rel.parts) < 2 or storage.private_file(rel):
            raise ValueError('This sharing package contains excluded material.')
        if item['kind']=='file' and item['key'] != 'file:' + '/'.join(rel.parts[1:]):
            raise ValueError('A shared file does not match its identity.')
    if sum(item['bytes'] for item in items) > MAX_BYTES:
        raise ValueError('Choose a smaller AURA sharing package.')


def load_package(ident, store=None):
    payload = _job(ident, store) / 'payload'
    manifest = read(payload / 'AURA-SHARE.json')
    validate_manifest(manifest)
    if not isinstance(manifest, dict) or manifest.get('format') != FORMAT:
        raise ValueError('This sharing package needs a supported AURA version.')
    if not isinstance(manifest.get('items'), list) or not manifest['items'] or len(manifest['items']) > MAX_FILES:
        raise ValueError('This sharing package has an invalid file list.')
    origin = manifest.get('origin', {})
    if not re.fullmatch(r'[a-f0-9]{32}', str(origin.get('id'))) or not isinstance(origin.get('name'), str):
        raise ValueError('This sharing package has no valid origin.')
    seen, keys, total = set(), set(), 0
    for item in manifest['items']:
        rel = safe(item['path'])
        if rel.parts[0] not in {'records', 'files'} or storage.private_file(rel) or len(rel.parts) < 2:
            raise ValueError('This sharing package contains excluded material.')
        if item['kind'] not in {'record', 'file'} or item['path'].casefold() in seen or item['key'] in keys:
            raise ValueError('This sharing package has overlapping items.')
        seen.add(item['path'].casefold()); keys.add(item['key'])
        path = unlinked(payload / rel)
        total += path.stat().st_size
        if total > MAX_BYTES or path.stat().st_size != item['bytes'] or _sha256(path) != item['sha256']:
            raise ValueError('Package verification failed. Export a fresh copy.')
        if item['kind'] == 'record':
            obj = read(path)
            if _secrets(obj):
                raise ValueError('A shared record contains credential fields.')
            validate_canonical(obj.get('object_type'), obj)
            if obj.get('business_id') != origin.get('business_id') or item['key'] != 'record:' + obj['id'] or item.get('type') != obj['object_type']:
                raise ValueError('A shared record does not match its original business identity.')
    if any(dep not in keys for e in manifest['items'] for dep in e.get('dependencies', [])):
        raise ValueError('Supporting records are missing from this package.')
    if manifest.get('revision') != digest({k:manifest[k] for k in ('name', 'origin', 'note', 'items', 'notes')}):
        raise ValueError('The package description changed. Export a fresh copy.')
    return manifest, payload


def check_source(ident, store=None):
    source = read(_job(ident, store) / 'source.json')
    if not source:
        return
    try:
        for row in source['inputs']:
            if _sha256(unlinked(row['path'])) != row['sha256']:
                raise ValueError('changed')
        for row in source.get('folders', []):
            if [str(p) for p in walk(row['path'], [])] != row['files']:
                raise ValueError('changed')
    except (OSError, ValueError):
        raise ValueError('The source changed or is unavailable. Prepare a fresh sharing review.') from None


def export_package(ident, destination, store=None):
    manifest, payload = load_package(ident, store)
    check_source(ident, store)
    output = unlinked(destination)
    if output.suffix.lower() != '.zip' or output.exists():
        raise ValueError('Choose a new ZIP file name. Existing files are not replaced.')
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.aura-share-', suffix='.tmp', dir=output.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(payload / 'AURA-SHARE.json', 'AURA-SHARE.json')
            for item in manifest['items']:
                archive.write(payload / safe(item['path']), item['path'])
        # Validate actual archived bytes, rather than only trusting the source hashes.
        loaded = import_package(temporary, store)
        shutil.rmtree(_job(loaded['id'], store))
        check_source(ident, store)
        source_info=read(_job(ident,store)/'source.json',{})
        if source_info.get('community') and Path(temporary).stat().st_size>10*1024**2:
            raise ValueError('This public package exceeds 10 MB compressed. Select fewer files before exporting.')
        # Publish the already verified file atomically; a competing name is never replaced.
        if os.name == 'nt':
            # Windows rename refuses an occupied name and also works on USB/exFAT.
            os.rename(temporary, output)
        else:
            try:
                os.link(temporary, output)
            except FileExistsError:
                raise
            except OSError:
                # Some removable filesystems do not support hard links. Keep
                # exclusive creation and clean up a failed, incomplete copy.
                created = False
                try:
                    with output.open('xb') as target, open(temporary,'rb') as source:
                        created = True
                        shutil.copyfileobj(source,target)
                        target.flush(); os.fsync(target.fileno())
                except Exception:
                    if created:
                        output.unlink(missing_ok=True)
                    raise
    finally:
        Path(temporary).unlink(missing_ok=True)
    result = {'path':str(output), 'verified':True, **package_summary(ident, manifest)}
    source = read(_job(ident, store) / 'source.json') or read(_job(ident, store) / 'ui-scope.json', {})
    if source:
        try:
            remember_package(Path(source.get('root') or source['workspace']), source['business'], output)
        except (OSError, ValueError):
            result['catalog_note'] = 'The ZIP was saved, but its recent location could not be remembered. Use Choose file to open it.'
    return result


def _archive_manifest(archive):
    """One structural check for discovery and import; import also verifies contents."""
    infos = archive.infolist()
    if len(infos)>MAX_FILES+1 or sum(i.file_size for i in infos)>MAX_BYTES+16*1024**2:
        raise ValueError('Choose a smaller AURA sharing package.')
    names = [i.filename for i in infos]
    if len(set(n.casefold() for n in names))!=len(names) or 'AURA-SHARE.json' not in names:
        raise ValueError('Choose an AURA sharing ZIP. Workspace backups use Back up or restore.')
    if archive.getinfo('AURA-SHARE.json').file_size>16*1024**2:
        raise ValueError('The package description is too large.')
    manifest = json.loads(archive.read('AURA-SHARE.json'))
    validate_manifest(manifest)
    expected = {'AURA-SHARE.json'} | {e['path'] for e in manifest['items']}
    if set(names)!=expected:
        raise ValueError('The package contains unlisted or missing files.')
    for info in infos:
        if info.is_dir() or ((info.external_attr>>16)&0o170000)==0o120000:
            raise ValueError('Folder links are not allowed in sharing packages.')
    return manifest


def import_package(archive_path, store=None):
    ident = uuid.uuid4().hex
    job = _job(ident, store)
    payload = job / 'payload'
    try:
        with zipfile.ZipFile(unlinked(archive_path)) as archive:
            manifest = _archive_manifest(archive)
            infos = archive.infolist()
            for info in infos:
                rel = safe(info.filename)
                path = payload / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as source, path.open('xb') as target:
                    shutil.copyfileobj(source, target)
        verified, _ = load_package(ident, store)
        return package_summary(ident, verified)
    except (OSError, KeyError, TypeError, zipfile.BadZipFile, ValueError, RuntimeError) as exc:
        if job.exists():
            shutil.rmtree(job)
        raise ValueError(str(exc) if isinstance(exc, ValueError) else 'This package could not be read. Choose a verified AURA sharing ZIP.') from None


def _index_path(root, bid):
    return metadata(root, bid) / 'index.json'


def select_package(ident, keys, store=None):
    """Prepare an independent subset, preserving required supporting records."""
    manifest,payload=load_package(ident,store)
    by_key={row['key']:row for row in manifest['items']}
    if not isinstance(keys,list) or not keys or any(key not in by_key for key in keys):
        raise ValueError('Select available package items before continuing.')
    wanted=set(keys);pending=list(keys)
    while pending:
        for dependency in by_key[pending.pop()].get('dependencies',[]):
            if dependency not in wanted:wanted.add(dependency);pending.append(dependency)
    new_id=uuid.uuid4().hex;job=_job(new_id,store);target=job/'payload';target.mkdir(parents=True)
    try:
        selected=[]
        for row in manifest['items']:
            if row['key'] not in wanted:continue
            relative=safe(row['path']);dest=target/relative;dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(payload/relative,dest);selected.append({**row,'supporting':row['key'] not in keys})
        updated={**manifest,'items':selected}
        updated['revision']=digest({k:updated[k] for k in ('name','origin','note','items','notes')})
        write_json_atomic(target/'AURA-SHARE.json',updated)
        return package_summary(new_id,updated)
    except Exception:
        shutil.rmtree(job);raise


def review(ident, destination, bid='', new_name='', store=None):
    manifest, payload = load_package(ident, store)
    check_source(ident, store)
    target = unlinked(destination)
    if target == PRODUCT_ROOT.resolve() or target.is_relative_to(PRODUCT_ROOT.resolve()) or target in {Path(target.anchor), Path.home().resolve()}:
        raise ValueError('Choose a workspace outside the AURA application, home root, or drive root.')
    new_name = str(new_name).strip()
    if new_name:
        if len(new_name) > 160 or (target.exists() and any(target.iterdir())):
            raise ValueError('Choose a new or empty folder and a name of up to 160 characters.')
        from setup import _stable_business_id
        bid = _stable_business_id(new_name)
        existing = {}
    else:
        business(target, bid)
        existing = read(_index_path(target, bid), {})
    rows = []
    for item in manifest['items']:
        token = digest([manifest['origin']['id'], item['key']])[:24]
        rel = Path('attachments') / bid / 'shared' / manifest['origin']['id'] / safe(item['path'])
        local_token = digest([bid, token])[:24]
        source_id = 'src_shared_' + local_token
        record_rel = Path('instances') / bid / 'intelligence/sources' / (source_id + '.json')
        previous = existing.get(token)
        actual = _sha256(unlinked(target / rel)) if (target / rel).is_file() else None
        record_hash = _sha256(unlinked(target / record_rel)) if (target / record_rel).is_file() else None
        asset_rel = Path('instances') / bid / 'assets' / ('ast_shared_' + local_token + '.json') if item['kind'] == 'file' else None
        asset_hash = _sha256(unlinked(target / asset_rel)) if asset_rel and (target / asset_rel).is_file() else None
        if previous:
            unchanged = actual == previous['file_hash'] and record_hash == previous['record_hash'] and (not asset_rel or asset_hash == previous.get('asset_hash'))
            action = 'already' if previous['source_hash'] == item['sha256'] else 'update' if unchanged else 'conflict'
            if not unchanged:
                action = 'local' if previous['source_hash'] == item['sha256'] else 'conflict'
        else:
            action = 'add' if actual is None and record_hash is None and asset_hash is None else 'conflict'
        rows.append({**item, 'token':token, 'local_token':local_token, 'target':rel.as_posix(), 'record':record_rel.as_posix(), 'source_id':source_id,
                     'action':action, 'expected_file':actual, 'expected_record':record_hash, 'expected_asset':asset_hash})
    notes_changed = False
    if not new_name:
        for receipt in recent_receipts(target, bid):
            if receipt.get('status')=='added' and receipt.get('origin',{}).get('id')==manifest['origin']['id'] and receipt.get('package_reference'):
                previous_package = read(target / safe(receipt['package_reference']), {})
                notes_changed = any(previous_package.get(k) != manifest[k] for k in ('name','note'))
                break
    result = {'id':ident, 'destination':str(target), 'business':bid, 'new_name':new_name, 'name':manifest['name'],
              'origin':manifest['origin'], 'created':now(), 'revision':manifest['revision'], 'note':manifest['note'],
              'notes':manifest['notes'], 'notes_changed':notes_changed, 'items':rows, 'counts':{a:sum(r['action'] == a for r in rows) for a in ('add','update','already','local','conflict')}}
    write_json_atomic(_job(ident, store) / 'review.json', result)
    return result


def _write_bytes(path, data):
    path = unlinked(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.aura-share-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        Path(temp).unlink(missing_ok=True)


def _copy_file(source, destination):
    source, destination = unlinked(source), unlinked(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.aura-share-', dir=destination.parent)
    os.close(fd)
    try:
        expected = _sha256(source)
        shutil.copyfile(source, temporary)
        if _sha256(Path(temporary)) != expected or _sha256(source) != expected:
            raise ValueError('A shared file changed while it was copied. Review the transfer again.')
        os.replace(temporary, destination)
    finally:
        Path(temporary).unlink(missing_ok=True)


def apply(ident, include_updates=False, store=None):
    plan = read(_job(ident, store) / 'review.json')
    if not plan:
        raise ValueError('Review the destination before adding shared work.')
    with destination_lock(plan['destination']):
        return _apply(ident, include_updates, store)


def _apply(ident, include_updates=False, store=None):
    plan = read(_job(ident, store) / 'review.json')
    if not plan:
        raise ValueError('Review the destination before adding shared work.')
    manifest, payload = load_package(ident, store)
    check_source(ident, store)
    target = unlinked(plan['destination'])
    bid = plan['business']
    current = review(ident, target, bid, plan['new_name'], store)
    if current['items'] != plan['items'] or current['revision'] != plan['revision']:
        raise ValueError('The destination changed after your review. Review it again before adding anything.')
    changes = [r for r in plan['items'] if r['action'] == 'add' or (r['action'] == 'update' and include_updates)]
    conflicts = [r for r in plan['items'] if r['action'] == 'conflict']
    archive_rel = (Path('attachments') / bid / 'shared' / manifest['origin']['id'] / 'packages' / manifest['revision']).as_posix()
    retain_review = (conflicts or plan.get('notes_changed')) and not (target / archive_rel / 'AURA-SHARE.json').exists()
    if not changes and not retain_review:
        return {**plan, 'status':'unchanged', 'message':'No changes were made. Existing work was kept.'}
    created_root = bool(plan['new_name'])
    receipt_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:12]
    undo_dir = metadata(target, bid) / 'undo' / receipt_id
    journal, original_index, index_path = [], None, _index_path(target, bid)
    try:
        latest = review(ident, target, bid, plan['new_name'], store)
        if latest['items'] != plan['items']:
            raise ValueError('The destination changed. Review it again.')
        if created_root:
            env = dict(os.environ, BUSINESSOS_WORKSPACE=str(target), BUSINESSOS_WORKSPACE_CONFIG=str(target / '.businessos/workspace.json'))
            flags = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
            subprocess.run([sys.executable, str(PRODUCT_ROOT / 'scripts/setup.py'), '--organization', plan['new_name'], '--no-link', '--json'],
                           env=env, capture_output=True, check=True, timeout=90, **flags)
        original_index = index_path.read_bytes() if index_path.exists() else None
        index = read(index_path, {})
        receipt_path = metadata(target, bid) / 'receipts' / (receipt_id + '.json')
        progress_path = metadata(target, bid) / 'receipts' / (receipt_id + '.jsonl')
        receipt = {'id':receipt_id, 'status':'adding', 'created':now(), 'name':manifest['name'], 'origin':manifest['origin'],
                   'counts':plan['counts'], 'notes':manifest['notes'], 'changes':journal,
                   'before_index':{r['token']:index[r['token']] for r in changes if r['token'] in index},
                   'tokens':[r['token'] for r in changes], 'after_index':{}}
        write_json_atomic(receipt_path, receipt)
        def write(rel, content):
            path = unlinked(target / safe(rel))
            previous = None
            if path.exists():
                previous = str(len(journal)) + '.bin'
                undo_dir.mkdir(parents=True, exist_ok=True)
                _copy_file(path, undo_dir / previous)
            journal.append({'path':rel, 'before':previous, 'after':_sha256(content) if isinstance(content, Path) else digest(content)})
            # Append one durable operation instead of rewriting an ever-growing
            # receipt for every file in a large project.
            with unlinked(progress_path).open('a', encoding='utf-8') as progress:
                progress.write(json.dumps(journal[-1], ensure_ascii=False) + '\n')
                progress.flush(); os.fsync(progress.fileno())
            if isinstance(content, Path):
                _copy_file(content, path)
            else:
                _write_bytes(path, content)
        manifest_rel = archive_rel + '/AURA-SHARE.json'
        receipt['package_reference'] = manifest_rel
        if not (target / manifest_rel).exists():
            # Keeps original identities, dependency mapping and setup notes outside canonical local truth.
            mapped = {**manifest, 'local_items':{r['key']:r['target'] for r in plan['items']},
                      'local_actions':{r['key']:r['action'] for r in plan['items']}}
            write(manifest_rel, (json.dumps(mapped, ensure_ascii=False, indent=2) + '\n').encode())
        # Source evidence stays separate from editable local copies. This also makes
        # conflicting incoming versions available without replacing local work.
        for row in changes + conflicts:
            rel = archive_rel + '/' + row['path']
            if not (target / rel).exists():
                write(rel, payload / safe(row['path']))
        for row in changes:
            for field, expected in (('target','expected_file'), ('record','expected_record')):
                path = unlinked(target / safe(row[field]))
                actual = _sha256(path) if path.exists() else None
                if actual != row[expected]:
                    raise ValueError('An item changed during import. Nothing from this transfer was kept; review again.')
            content = payload / safe(row['path'])
            write(row['target'], content)
            stamp = now()
            old_record = read(target / row['record'], {})
            obj = {'id':row['source_id'], 'object_type':'SourceRecord', 'schema_version':'1.0.0', 'business_id':bid,
                   'created_at':old_record.get('created_at',stamp), 'updated_at':stamp, 'lineage':[],
                   'source_type':'aura_shared_material', 'source_reference':archive_rel + '/' + row['path'], 'origin':manifest['origin']['name'],
                   'retrieved_at':stamp, 'published_at':manifest['created'], 'content_hash':'sha256:' + row['sha256'],
                   'content_hash_target':'file_bytes', 'content_hash_reference':archive_rel + '/' + row['path'], 'access_class':'private',
                   'access_scope':'Explicitly shared source material; not automatically adopted as local business truth.',
                   'extensions':{'businessos':{'authority':'unknown', 'display_name':row['title']},
                                 'aura_sharing':{'origin':manifest['origin'], 'item_token':row['token'], 'original_type':row.get('type'),
                                                 'package':manifest['name'], 'package_reference':manifest_rel,
                                                 'revision':manifest['revision'], 'copied_at':stamp}}}
            validate_canonical('SourceRecord', obj)
            record_bytes = (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode()
            write(row['record'], record_bytes)
            if row['kind'] == 'file':
                asset = {'id':'ast_shared_' + row['local_token'], 'object_type':'Asset', 'schema_version':'1.0.0', 'business_id':bid,
                         'created_at':old_record.get('created_at',stamp), 'updated_at':stamp, 'lineage':[row['source_id']],
                         'asset_type':'shared file', 'business_role':row['title'], 'version':row['sha256'][:12], 'status':'draft',
                         'location_reference':row['target'], 'extensions':{'aura_sharing':{'source_ref':row['source_id']}}}
                asset_rel = f"instances/{bid}/assets/{asset['id']}.json"
                # Never overwrite an independently edited file registration.
                existing_asset = read(target / asset_rel)
                previous_asset = index.get(row['token'], {}).get('asset_hash')
                if existing_asset and (not previous_asset or _sha256(target / asset_rel) != previous_asset):
                    raise ValueError('A shared file registration was edited locally. Keep it and review this transfer.')
                validate_canonical('Asset', asset)
                write(asset_rel, (json.dumps(asset, indent=2, ensure_ascii=False) + '\n').encode())
            index[row['token']] = {'source_hash':row['sha256'], 'file_hash':row['sha256'], 'record_hash':digest(record_bytes),
                                   'origin':manifest['origin'], 'key':row['key'],
                                   **({'asset_hash':_sha256(target / asset_rel)} if row['kind'] == 'file' else {})}
        receipt['after_index'] = {r['token']:index[r['token']] for r in changes}
        write_json_atomic(receipt_path, receipt)
        write_json_atomic(index_path, index)
        receipt['status'] = 'added'
        write_json_atomic(receipt_path, receipt)
        source = read(_job(ident, store) / 'source.json')
        if source:
            # This convenience must never turn a completed import into a failed operation.
            try:
                write_json_atomic(metadata(source['root'], source['business']) / 'last-destination.json', {'path':str(target), 'business':bid})
            except OSError:
                pass
        return {**plan, 'receipt':receipt_id, 'status':'added', 'comparison':archive_rel if conflicts else '', 'added':sum(r['action']=='add' for r in changes),
                'updated':sum(r['action']=='update' for r in changes), 'message':'Shared work added. Existing business information was kept.'}
    except Exception:
        for row in reversed(journal):
            path = unlinked(target / safe(row['path']))
            if row['before'] is None:
                path.unlink(missing_ok=True)
            else:
                _copy_file(undo_dir / row['before'], path)
        if original_index is not None:
            _write_bytes(index_path, original_index)
        elif index_path.exists():
            index_path.unlink()
        if 'receipt_path' in locals():
            receipt_path.unlink(missing_ok=True)
            progress_path.unlink(missing_ok=True)
        # Failed new-workspace setup remains available rather than deleting unfamiliar files.
        raise


def undo(root, bid, receipt_id, apply_changes=False):
    with destination_lock(root):
        return _undo(root, bid, receipt_id, apply_changes)


def _undo(root, bid, receipt_id, apply_changes=False):
    business(root, bid)
    if not re.fullmatch(r'[0-9]{8}T[0-9]{6}-[a-f0-9]{12}', str(receipt_id)):
        raise ValueError('Choose an import from this workspace’s sharing history.')
    base = metadata(root, bid)
    path = base / 'receipts' / (receipt_id + '.json')
    receipt = read(path)
    if not receipt or receipt['status'] == 'undone':
        raise ValueError('This import is unavailable or was already undone.')
    interrupted = receipt['status'] in {'adding', 'undoing'}
    if receipt['status']=='adding' and not receipt.get('changes'):
        progress_path = base / 'receipts' / (receipt_id + '.jsonl')
        if progress_path.exists():
            lines = unlinked(progress_path).read_text(encoding='utf-8').splitlines()
            for number, line in enumerate(lines):
                try:
                    receipt['changes'].append(json.loads(line))
                except ValueError:
                    if number != len(lines)-1:
                        raise ValueError('The recovery journal needs review. Keep this workspace and ask your AI to inspect it.') from None
    def unchanged(row):
        dest = unlinked(Path(root) / safe(row['path']))
        actual = _sha256(dest) if dest.is_file() else None
        if actual == row['after']:
            return True
        if interrupted:
            before = base / 'undo' / receipt_id / row['before'] if row['before'] is not None else None
            return actual == (_sha256(unlinked(before)) if before and before.is_file() else None)
        return False
    changed = [row['path'] for row in receipt['changes'] if not unchanged(row)]
    index = read(_index_path(root, bid), {})
    if any(index.get(token) != receipt['after_index'].get(token) and
           (not interrupted or index.get(token) != receipt.get('before_index', {}).get(token)) for token in receipt['tokens']):
        changed.append('A later transfer updated this material.')
    # Detect canonical work that now relies on the imported SourceRecords/Assets.
    imported = {Path(r['path']).stem for r in receipt['changes'] if r['path'].startswith('instances/')}
    own = {r['path'] for r in receipt['changes']}
    for obj, record in objects(root, bid).values():
        def values(value):
            if isinstance(value, dict):
                return set().union(*(values(v) for v in value.values())) if value else set()
            if isinstance(value, list):
                return set().union(*(values(v) for v in value)) if value else set()
            return {value} if isinstance(value,str) else set()
        if record.relative_to(root).as_posix() not in own and ((references_in(obj) & imported) or (values(obj) & own)):
            changed.append('Other saved work now refers to ' + title(obj))
    if changed:
        return {'can_undo':False, 'changed':changed, 'message':'This work changed or is now in use. It was kept; ask your AI to review it.'}
    if not apply_changes:
        return {'can_undo':True, 'message':'Undo will remove untouched additions and restore replaced copies. Your other work stays in place.'}
    receipt['status'] = 'undoing'
    write_json_atomic(path, receipt)
    for row in reversed(receipt['changes']):
        dest = unlinked(Path(root) / safe(row['path']))
        if row['before'] is None:
            dest.unlink(missing_ok=interrupted)
        else:
            _copy_file(base / 'undo' / receipt_id / row['before'], dest)
    for token in receipt['tokens']:
        if token in receipt.get('before_index', {}):
            index[token] = receipt['before_index'][token]
        else:
            index.pop(token, None)
    write_json_atomic(_index_path(root, bid), index)
    receipt['status'] = 'undone'
    write_json_atomic(path, receipt)
    return {'can_undo':True, 'status':'undone', 'message':'Import undone. Your other work was kept.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', help='Optional local review store')
    sub = parser.add_subparsers(dest='action', required=True)
    for action in ('list', 'history'):
        p = sub.add_parser(action); p.add_argument('workspace'); p.add_argument('business')
    p = sub.add_parser('discover'); p.add_argument('workspace'); p.add_argument('business'); p.add_argument('--folder')
    p = sub.add_parser('prepare'); p.add_argument('workspace'); p.add_argument('business'); p.add_argument('--select', action='append', required=True); p.add_argument('--name', default=''); p.add_argument('--note', default='')
    p = sub.add_parser('save-selection'); p.add_argument('workspace'); p.add_argument('business'); p.add_argument('--select', action='append', required=True); p.add_argument('--name', required=True); p.add_argument('--note', default=''); p.add_argument('--id', default='', help='Update this saved selection, preserving its identity')
    p = sub.add_parser('export'); p.add_argument('id'); p.add_argument('output')
    p = sub.add_parser('import'); p.add_argument('archive')
    p = sub.add_parser('select'); p.add_argument('id'); p.add_argument('--select', action='append', required=True)
    p = sub.add_parser('review'); p.add_argument('id'); p.add_argument('destination'); p.add_argument('--business', default=''); p.add_argument('--new-name', default='')
    p = sub.add_parser('apply'); p.add_argument('id'); p.add_argument('--include-updates', action='store_true')
    p = sub.add_parser('detail'); p.add_argument('workspace'); p.add_argument('business'); p.add_argument('receipt')
    p = sub.add_parser('undo'); p.add_argument('workspace'); p.add_argument('business'); p.add_argument('receipt'); p.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        if args.action == 'list': result = public_inventory(args.workspace, args.business)
        elif args.action == 'history': result = history(args.workspace, args.business)
        elif args.action == 'discover': result = discover_packages(args.workspace, args.business, folder=args.folder)
        elif args.action == 'save-selection': result = save_selection(args.workspace, args.business, args.name, args.select, args.note, args.id)
        elif args.action == 'prepare': result = prepare(args.workspace, args.business, args.select, args.name, args.note, args.store)
        elif args.action == 'export': result = export_package(args.id, args.output, args.store)
        elif args.action == 'import':
            from workspace_exchange import import_package as import_exchange_package
            result = import_exchange_package(args.archive, args.store)
        elif args.action == 'select': result = select_package(args.id, args.select, args.store)
        elif args.action == 'review': result = review(args.id, args.destination, args.business, args.new_name, args.store)
        elif args.action == 'apply': result = apply(args.id, args.include_updates, args.store)
        elif args.action == 'detail': result = imported_detail(args.workspace, args.business, args.receipt)
        else: result = undo(args.workspace, args.business, args.receipt, args.apply)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
