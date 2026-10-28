"""Open known workspace folders and make verified, portable workspace backups."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
import sys
import tempfile
import zipfile

from _common import PRODUCT_ROOT, workspace_root
from migrate_workspace import NAMESPACES, _source_files, _sha256
import workspace_catalog

VIEW_FILE = '.businessos/view.json'
PRIVATE = {'.git', '.businessos', '.aura-runtime', '.venv', 'venv', 'node_modules', '__pycache__',
           'credentials', 'secrets', '.ssh', '.aws', '.azure', '.codex', '.claude', '.pi', '.hermes', '.gemini'}
OUTPUT_DIRS = {'deliverables', 'outputs', 'exports', 'projects', 'work'}


def private_file(path):
    secret_names = {'auth.json','credentials.json','api_keys.json','secrets.json'}
    def private(part):
        part = part.lower()
        return (part in PRIVATE or part in secret_names or
                (part.startswith('.env') and not part.endswith(('.example','.sample','.template'))))
    return any(private(p) for p in path.parts) or path.suffix.lower() in {'.pem','.key','.p12','.pfx'}


def load_view(root):
    if (Path(root) / VIEW_FILE).is_symlink():
        raise ValueError('Workspace links point outside this folder. Keep the original and reconnect them explicitly.')
    data = workspace_catalog.read_json(Path(root) / VIEW_FILE, {})
    if not isinstance(data, dict) or not isinstance(data.get('file_locations', {}), dict):
        raise ValueError('Saved workspace links need attention. The original settings were kept.')
    return data


def save_view(root, preferences):
    root = Path(root).resolve()
    locations = {}
    for bid, items in preferences.get('file_locations', {}).items():
        locations[bid] = []
        for item in items:
            path = Path(item['path'])
            relative = path.is_absolute() and path.is_relative_to(root)
            locations[bid].append({k:item[k] for k in ('id','name','kind')})
            locations[bid][-1].update(path=path.relative_to(root).as_posix() if relative else str(path), relative=relative)
    workspace_catalog.write_json(root / VIEW_FILE, {'format':1, 'file_locations':locations,
        'appearance':preferences.get('appearance','system'), 'model_picker':preferences.get('model_picker', {})})


def view_preferences(root):
    data = load_view(root)
    if not isinstance(data.get('model_picker', {}), dict) or data.get('appearance','system') not in {'system','light','dark'}:
        raise ValueError('Saved workspace preferences need attention.')
    locations = {}
    for bid, items in data.get('file_locations', {}).items():
        if not isinstance(items, list):
            raise ValueError('A saved folder link needs attention.')
        locations[bid] = []
        for item in items:
            if not isinstance(item, dict) or not all(isinstance(item.get(k), str) for k in ('id','path','name','kind')):
                raise ValueError('A saved folder link needs attention.')
            path = Path(item['path'])
            if item.get('relative'):
                if path.is_absolute() or '..' in path.parts:
                    raise ValueError('A saved folder link is outside its workspace.')
                path = Path(root) / path
            locations[bid].append({**item,'path':str(path)})
    return {**data, 'file_locations':locations}


def workspace_files(source, hashes=True):
    """Workspace-owned files, including legacy outputs; never copy an AURA installation."""
    source = Path(source).resolve()
    embedded = (source / 'scripts').is_dir() and (source / 'VERSION').is_file()
    rows, excluded = [], []
    for directory, dirs, names in os.walk(source, followlinks=False):
        base = Path(directory)
        relative = base.relative_to(source)
        kept = []
        for name in sorted(dirs):
            child = base / name
            rel = child.relative_to(source)
            if child.is_symlink() or (name == '.businessos'):
                if child.is_symlink():excluded.append(rel.as_posix())
                continue
            if private_file(rel) or (rel.parts[:2] in {('instances','_template'),('runtime','tmp')}) or (rel.parts[0]=='runtime' and name=='logs'):
                excluded.append(rel.as_posix());continue
            if embedded and base == source and name not in set(NAMESPACES) | OUTPUT_DIRS:
                excluded.append(rel.as_posix())
                continue
            kept.append(name)
        dirs[:] = kept
        for name in sorted(names):
            path = base / name; rel = path.relative_to(source)
            if name == 'AURA-BACKUP.json' or path.is_symlink() or private_file(rel) or (embedded and base == source):
                excluded.append(rel.as_posix());continue
            rows.append((rel,path,_sha256(path) if hashes else '',path.stat().st_size))
    metadata = source / VIEW_FILE
    if metadata.is_file() and not metadata.is_symlink():
        rows.append((Path(VIEW_FILE),metadata,_sha256(metadata) if hashes else '',metadata.stat().st_size))
    return sorted(rows, key=lambda r:r[0].as_posix()), excluded


def backup_plan(source, include_linked=False, hashes=False):
    source = Path(source).resolve()
    rows, excluded = workspace_files(source, hashes)
    view = load_view(source)
    links, overrides, folder_targets = [], {}, {}
    businesses = {b['id'] for b in workspace_catalog.preview(source)['businesses']}
    for bid, items in view.get('file_locations', {}).items():
        if bid not in businesses:
            continue
        for item in items:
            relative_link = item.get('relative') is True
            relative_path = Path(item['path'])
            if relative_link and (relative_path.is_absolute() or '..' in relative_path.parts):
                raise ValueError('A saved file link is outside the workspace. Reconnect it before exporting.')
            path = (source / relative_path).resolve() if relative_link else relative_path
            valid = path.is_absolute() and path.exists() and not path.is_symlink() and not private_file(path)
            if not relative_link:
                links.append({'name':item['name'], 'path':str(path), 'missing':not valid, 'included':bool(include_linked and valid)})
            if not valid or (not relative_link and not include_linked):
                continue
            if not all(part and part not in {'.','..'} and '/' not in part and '\\' not in part and ':' not in part for part in (bid,item['id'])):
                raise ValueError('A linked folder identity needs attention before export.')
            destination = Path(item['path']) if relative_link and path.is_dir() else Path(item['path']).parent if relative_link else Path('attachments') / bid / 'linked' / item['id']
            if path.is_dir():
                folder_targets[os.path.normcase(str(path.resolve()))] = destination
            candidates = workspace_files(path, hashes)[0] if path.is_dir() else [(Path(path.name),path,_sha256(path) if hashes else '',path.stat().st_size)]
            for rel, file, digest, size in candidates:
                if private_file(rel):
                    continue
                target_rel = destination / rel
                if not any(r[0] == target_rel for r in rows):
                    rows.append((target_rel,file,digest,size))
            if not relative_link:
                item.update(path=(destination if path.is_dir() else destination / path.name).as_posix(), relative=True)
    # Native apps/CLIs can save Assets without ever using the UI's folder linker.
    # Include referenced local outputs and optionally bundle external originals.
    for record in (source / 'instances').glob('*/assets/*.json'):
        data = workspace_catalog.read_json(record,{})
        value = data.get('location_reference') if isinstance(data,dict) else None
        if not isinstance(value,str) or '://' in value:
            continue
        path = Path(value)
        path = (path if path.is_absolute() else source / path).resolve()
        if private_file(path) or path in {Path(path.anchor),Path.home().resolve(),source}:
            continue
        internal = path.is_relative_to(source)
        valid = path.exists() and (path.is_file() or path.is_dir()) and not path.is_symlink()
        if not internal or not valid:
            links.append({'name':path.name,'path':str(path),'missing':not valid,'included':bool(include_linked and valid)})
        if not valid or (not internal and not include_linked):
            continue
        existing = next((r[0] for r in rows if r[1] == path),None)
        rel = existing or (path.relative_to(source) if internal else Path('attachments') / record.parent.parent.name / 'imported' / record.stem / path.name)
        if path.is_dir():
            rel = folder_targets.get(os.path.normcase(str(path)),rel)
            for child,file,digest,size in workspace_files(path,hashes)[0]:
                if not any(r[0]==rel / child for r in rows):
                    rows.append((rel / child,file,digest,size))
        elif not existing:
            rows.append((rel,path,_sha256(path) if hashes else '',path.stat().st_size))
        if not internal:
            data['location_reference'] = rel.as_posix()
            overrides[record.relative_to(source).as_posix()] = json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8')
    if len({r[0].as_posix().casefold() for r in rows}) != len(rows):
        raise ValueError('Export locations overlap. Reconnect the linked folder or export without its files.')
    return {'rows':rows, 'view':view, 'links':links, 'excluded':excluded, 'overrides':overrides,
            'files':len(rows), 'bytes':sum(row[3] for row in rows)}


def normalize_file_links(root, old_root):
    if not old_root:
        return
    for file in (Path(root) / 'instances').glob('*/assets/*.json'):
        data = workspace_catalog.read_json(file, {})
        value = data.get('location_reference') if isinstance(data, dict) else None
        if not isinstance(value, str):
            continue
        cls = PureWindowsPath if PureWindowsPath(old_root).drive else PurePosixPath
        try:
            relative = cls(value).relative_to(cls(old_root))
            if '..' in relative.parts:
                continue
        except ValueError:
            continue
        data['location_reference'] = relative.as_posix()
        workspace_catalog.write_json(file,data)


def inspect(value):
    if not str(value).strip():
        raise ValueError('Choose your existing workspace folder.')
    candidates = workspace_catalog.candidates(value)['items']
    candidates = [r for r in candidates if r['kind'] == 'workspace']
    if len(candidates) != 1:
        raise ValueError('Choose one of the saved workspaces in the preview.')
    folder = Path(candidates[0]['path']).resolve(strict=True)
    profile = workspace_catalog.read_json(folder / '.businessos/workspace.json', {})
    if not isinstance(profile, dict):
        raise ValueError('The workspace settings need attention. Keep the original and ask your AI to check them.')
    location = Path(os.path.expandvars(profile.get('workspace_root') or str(folder))).expanduser()
    location = location if location.is_absolute() else folder / location
    env = dict(os.environ, BUSINESSOS_WORKSPACE=str(location.resolve()),
               BUSINESSOS_WORKSPACE_CONFIG=str(folder / '.businessos/workspace.json'), PYTHONUTF8='1')
    flags = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
    result = subprocess.run([sys.executable, str(PRODUCT_ROOT / 'scripts/workspace_status.py'), '--json'],
                            env=env, capture_output=True, text=True, encoding='utf-8', timeout=30, **flags)
    if result.returncode:
        raise ValueError('This workspace could not be read. Check its location and permissions.')
    data = json.loads(result.stdout)
    if not data['business_directory']:
        raise ValueError('No saved businesses were found in that folder. Choose the folder containing your existing work.')
    root = Path(data['workspace_root']).resolve(strict=True)
    # Readiness checks only the selected workspace, never creates another business.
    env['BUSINESSOS_WORKSPACE'] = str(root)
    ready = subprocess.run([sys.executable, str(PRODUCT_ROOT / 'scripts/doctor.py'), '--business-id', data['businesses'][0], '--json'],
                           env=env, capture_output=True, text=True, encoding='utf-8', timeout=90, **flags)
    if ready.returncode or json.loads(ready.stdout).get('status') != 'ready':
        raise ValueError('The saved workspace needs attention. Keep the original and ask your AI to check AURA doctor before switching.')
    return {'path':str(root), 'businesses':data['business_directory']}


def backup(source, destination, include_linked=False):
    source, destination = Path(source).resolve(), Path(destination).expanduser().resolve(strict=True)
    if not destination.is_dir() or destination.is_relative_to(source) or destination.is_relative_to(PRODUCT_ROOT):
        raise ValueError('Choose a backup folder outside your workspace and the AURA product folder.')
    plan = backup_plan(source, include_linked, hashes=True)
    rows = plan['rows']
    if not rows:
        raise ValueError('There is no workspace data to back up yet.')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
    output = destination / ('AURA-backup-' + stamp + '.zip')
    overrides = dict(plan['overrides'])
    if plan['view']:
        overrides[VIEW_FILE] = json.dumps(plan['view'],ensure_ascii=False,indent=2).encode('utf-8')
    manifest = {'format':'aura-workspace-backup-2', 'created_at':datetime.now(timezone.utc).isoformat(),
                'source_workspace':str(source), 'linked_locations':plan['links'],
                'workspace_profile':{k:v for k,v in workspace_catalog.read_json(source / '.businessos/workspace.json',{}).items()
                                     if k in {'profile','knowledge_enabled'}},
                'files':{rel.as_posix():{'sha256':digest, 'bytes':size} for rel, _, digest, size in rows}}
    for name, value in overrides.items():
        manifest['files'][name] = {'sha256':hashlib.sha256(value).hexdigest(), 'bytes':len(value)}
    # Publish only a complete verified archive. No machine credentials/preferences.
    fd, temp = tempfile.mkstemp(prefix='.aura-backup-', suffix='.tmp', dir=destination)
    os.close(fd)
    staged = Path(temp)
    try:
        with zipfile.ZipFile(staged, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for rel, path, digest, size in rows:
                if rel.as_posix() not in overrides:
                    z.write(path, rel.as_posix())
            for name, value in overrides.items():
                z.writestr(name,value)
            z.writestr('AURA-BACKUP.json', json.dumps(manifest, indent=2))
        with zipfile.ZipFile(staged) as z:
            for name, record in manifest['files'].items():
                with z.open(name) as stream:
                    if hashlib.file_digest(stream, 'sha256').hexdigest() != record['sha256']:
                        raise ValueError('A file changed during backup. Nothing was replaced; try again when work has finished.')
        if [(str(r), digest) for r, _, digest, _ in backup_plan(source,include_linked,hashes=True)['rows']] != [(str(r), digest) for r, _, digest, _ in rows]:
            raise ValueError('The workspace changed during backup. Try again when work has finished.')
        staged.replace(output)
    finally:
        staged.unlink(missing_ok=True)
    return {'path':str(output), 'files':len(manifest['files']), 'verified':True, 'links':plan['links']}


def restore(archive, destination):
    try:
        return _restore(archive, destination)
    except (zipfile.BadZipFile, KeyError, TypeError, RuntimeError, json.JSONDecodeError):
        raise ValueError('This backup could not be verified. Choose an AURA backup ZIP; the original workspace was not changed.') from None


def _restore(archive, destination):
    archive = Path(archive).expanduser().resolve(strict=True)
    target = Path(destination).expanduser().resolve()
    if target.is_relative_to(workspace_root().resolve()) or target.is_relative_to(PRODUCT_ROOT) or (target.exists() and (not target.is_dir() or any(target.iterdir()))):
        raise ValueError('Choose a new or empty folder outside the AURA product. Existing files will not be replaced.')
    if not target.parent.is_dir():
        raise ValueError('Choose a location inside an existing folder.')
    with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory(prefix='.aura-restore-', dir=target.parent) as temporary:
        if len(z.infolist()) > 100000 or z.getinfo('AURA-BACKUP.json').file_size > 16 * 1024 * 1024:
            raise ValueError('This backup is too large to restore through the interface. Ask your AI to help.')
        manifest = json.loads(z.read('AURA-BACKUP.json'))
        if manifest.get('format') not in {'aura-workspace-backup-1','aura-workspace-backup-2'} or not isinstance(manifest.get('files'), dict):
            raise ValueError('Choose a verified AURA workspace backup.')
        profile = manifest.get('workspace_profile',{})
        if not isinstance(profile,dict) or profile.get('profile','power_user') not in {'simple','power_user','organization'}:
            raise ValueError('The backup workspace settings need attention. Nothing was restored.')
        names = z.namelist()
        if len(names) != len({name.casefold() for name in names}) or set(names) != set(manifest['files']) | {'AURA-BACKUP.json'}:
            raise ValueError('The backup contents do not match its file list. The original was not changed.')
        stage = Path(temporary)
        for name, record in manifest['files'].items():
            rel = PurePosixPath(name)
            allowed = (rel.parts and (rel.parts[0] in NAMESPACES if manifest['format']=='aura-workspace-backup-1'
                       else not private_file(rel) or name == VIEW_FILE))
            if not allowed or '..' in rel.parts or '\\' in name or ':' in name or rel.is_absolute():
                raise ValueError('The backup contains an unsafe file location. Nothing was restored.')
            info = z.getinfo(name)
            if info.file_size != record['bytes'] or ((info.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError('The backup contains an invalid file. Nothing was restored.')
            path = stage.joinpath(*rel.parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as src, path.open('xb') as dst:
                while chunk := src.read(1024 * 1024):
                    dst.write(chunk)
            if _sha256(path) != record['sha256']:
                raise ValueError('Backup verification failed. Nothing was restored.')
        # All bytes were checked before touching the destination. Destination is
        # deliberately empty; the existing migration helper retains the source.
        from migrate_workspace import _copy_verified
        rows = [(Path(name),stage / name,record['sha256'],record['bytes']) for name,record in manifest['files'].items()]
        target.mkdir(exist_ok=True)
        _copy_verified(target, rows)
        normalize_file_links(target, manifest.get('source_workspace'))
        # Set up only scaffold/profile, in a separate process so active selection
        # does not change until the caller explicitly opens this restored folder.
        env = dict(os.environ, BUSINESSOS_WORKSPACE=str(target), BUSINESSOS_WORKSPACE_CONFIG=str(target / '.businessos/workspace.json'))
        flags = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
        result = subprocess.run([sys.executable, str(PRODUCT_ROOT / 'scripts/configure_workspace.py'), str(target), '--profile', profile.get('profile','power_user'), '--no-link', '--json',
                                 *(['--no-knowledge'] if profile.get('knowledge_enabled') is False else [])],
                                env=env, capture_output=True, text=True, encoding='utf-8', timeout=30, **flags)
        if result.returncode:
            raise ValueError('Your files were restored, but setup needs attention. Keep the backup and ask your AI to finish connecting the restored folder.')
    return {'path':str(target), 'files':len(rows), 'verified':True}


def relocate(source, destination):
    """Copy, verify, then reconnect elsewhere; originals are never removed or merged."""
    source, target = Path(source).resolve(), Path(destination).expanduser().resolve()
    if target == source or target.is_relative_to(source) or source.is_relative_to(target) or target.is_relative_to(PRODUCT_ROOT):
        raise ValueError('Choose a separate workspace folder outside the AURA application.')
    if target.exists() and any(target.iterdir()):
        raise ValueError('That folder already contains files. Open it separately or choose a new folder.')
    rows = backup_plan(source,hashes=True)['rows']
    if not rows:
        raise ValueError('There is no saved workspace data to copy.')
    from migrate_workspace import _copy_verified, _verify_target
    target.mkdir(parents=True, exist_ok=True)
    _copy_verified(target,rows)
    _verify_target(target,rows)
    if [(str(r),digest) for r,_,digest,_ in backup_plan(source,hashes=True)['rows']] != [(str(r),digest) for r,_,digest,_ in rows]:
        raise ValueError('The source changed while copying. The original is intact; finish active work before trying again.')
    normalize_file_links(target,str(source))
    profile = workspace_catalog.read_json(source / '.businessos/workspace.json',{})
    flags = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
    env = dict(os.environ, BUSINESSOS_WORKSPACE=str(target), BUSINESSOS_WORKSPACE_CONFIG=str(target / '.businessos/workspace.json'))
    subprocess.run([sys.executable,str(PRODUCT_ROOT / 'scripts/configure_workspace.py'),str(target),
        '--profile',profile.get('profile','power_user'),'--no-link','--json',
        *(['--no-knowledge'] if profile.get('knowledge_enabled') is False else [])],env=env,check=True,capture_output=True,timeout=30,**flags)
    return {'path':str(target),'files':len(rows),'verified':True,'source_retained':True}
