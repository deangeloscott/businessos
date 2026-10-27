"""Open known workspace folders and make verified, portable workspace backups."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

from _common import PRODUCT_ROOT, workspace_root
from migrate_workspace import NAMESPACES, _source_files, _sha256


def inspect(value):
    if not str(value).strip():
        raise ValueError('Choose your existing workspace folder.')
    folder = Path(value).expanduser().resolve(strict=True)
    if not folder.is_dir() or not (folder / '.businessos/workspace.json').is_file():
        raise ValueError('Choose an existing AURA workspace or an older AURA folder with saved work.')
    profile = json.loads((folder / '.businessos/workspace.json').read_text(encoding='utf-8'))
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


def backup(source, destination):
    source, destination = Path(source).resolve(), Path(destination).expanduser().resolve(strict=True)
    if not destination.is_dir() or destination.is_relative_to(source) or destination.is_relative_to(PRODUCT_ROOT):
        raise ValueError('Choose a backup folder outside your workspace and the AURA product folder.')
    rows = _source_files(source)
    if not rows:
        raise ValueError('There is no workspace data to back up yet.')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
    output = destination / ('AURA-backup-' + stamp + '.zip')
    manifest = {'format':'aura-workspace-backup-1', 'created_at':datetime.now(timezone.utc).isoformat(),
                'files':{rel.as_posix():{'sha256':digest, 'bytes':size} for rel, _, digest, size in rows}}
    # Publish only a complete verified archive. No machine credentials/preferences.
    fd, temp = tempfile.mkstemp(prefix='.aura-backup-', suffix='.tmp', dir=destination)
    os.close(fd)
    staged = Path(temp)
    try:
        with zipfile.ZipFile(staged, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for rel, path, digest, size in rows:
                z.write(path, rel.as_posix())
            z.writestr('AURA-BACKUP.json', json.dumps(manifest, indent=2))
        with zipfile.ZipFile(staged) as z:
            for name, record in manifest['files'].items():
                with z.open(name) as stream:
                    if hashlib.file_digest(stream, 'sha256').hexdigest() != record['sha256']:
                        raise ValueError('A file changed during backup. Nothing was replaced; try again when work has finished.')
        if [(str(r), digest) for r, _, digest, _ in _source_files(source)] != [(str(r), digest) for r, _, digest, _ in rows]:
            raise ValueError('The workspace changed during backup. Try again when work has finished.')
        staged.replace(output)
    finally:
        staged.unlink(missing_ok=True)
    return {'path':str(output), 'files':len(rows), 'verified':True}


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
        if manifest.get('format') != 'aura-workspace-backup-1' or not isinstance(manifest.get('files'), dict):
            raise ValueError('Choose a verified AURA workspace backup.')
        names = z.namelist()
        if len(names) != len(set(names)) or set(names) != set(manifest['files']) | {'AURA-BACKUP.json'}:
            raise ValueError('The backup contents do not match its file list. The original was not changed.')
        stage = Path(temporary)
        for name, record in manifest['files'].items():
            rel = PurePosixPath(name)
            if not rel.parts or rel.parts[0] not in NAMESPACES or '..' in rel.parts or '\\' in name or ':' in name or rel.is_absolute():
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
        rows = _source_files(stage)
        target.mkdir(exist_ok=True)
        _copy_verified(target, rows)
        # Set up only scaffold/profile, in a separate process so active selection
        # does not change until the caller explicitly opens this restored folder.
        env = dict(os.environ, BUSINESSOS_WORKSPACE=str(target), BUSINESSOS_WORKSPACE_CONFIG=str(target / '.businessos/workspace.json'))
        flags = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}
        result = subprocess.run([sys.executable, str(PRODUCT_ROOT / 'scripts/configure_workspace.py'), str(target), '--profile', 'power_user', '--no-link', '--json'],
                                env=env, capture_output=True, text=True, encoding='utf-8', timeout=30, **flags)
        if result.returncode:
            raise ValueError('Your files were restored, but setup needs attention. Keep the backup and ask your AI to finish connecting the restored folder.')
    return {'path':str(target), 'files':len(rows), 'verified':True}
