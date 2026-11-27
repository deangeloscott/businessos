"""Optional local-interface updates. Workspaces and AI apps are never installed here."""
from pathlib import Path, PurePosixPath, PureWindowsPath
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from urllib.error import URLError
import zipfile

from package_runtime import native_platform
from workspace_startup import state_dir

REPOSITORY = 'deangeloscott/businessos'
RELEASES = 'https://api.github.com/repos/' + REPOSITORY + '/releases?per_page=30'
DOWNLOADS = 'https://github.com/' + REPOSITORY + '/releases/download/'
PAGE = 'https://github.com/' + REPOSITORY + '/releases'
DAY = 86400
MAX_DOWNLOAD = 800 * 1024 * 1024
MAX_UNPACKED = 3 * 1024 * 1024 * 1024
BUSY = {'preparing', 'downloading', 'verifying', 'restarting'}
RUNTIME = '.aura-runtime'


def read(path, default=None):
    try:
        value = json.loads(Path(path).read_text(encoding='utf-8'))
        return value if isinstance(value, dict) else (default or {})
    except (OSError, ValueError):
        return default or {}


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    temporary.chmod(0o600)
    temporary.replace(path)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def version(value):
    match = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)', str(value))
    return tuple(map(int, match.groups())) if match else (0, 0, 0)


def schema_files(root):
    return sorted([*Path(root).glob('core/**/*.schema.json'), *Path(root).glob('systems/**/*.schema.json')])


def schema_hash(root, normalized=False):
    """The workspace record format an app expects. Bundles record the exact bytes, which AURA 0.7.5 and earlier
    compare as they are; `normalized` ignores line endings, so a Windows and a macOS build of one release agree."""
    digest = hashlib.sha256()
    for path in schema_files(root):
        digest.update(path.relative_to(root).as_posix().encode())
        raw = path.read_bytes()
        digest.update(raw.replace(b'\r\n', b'\n') if normalized else raw)
    return digest.hexdigest()


def write_integrity(root):
    """Called after bundling, so edited default files can be preserved explicitly."""
    root = Path(root)
    files = {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob('*'))
             if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts
             and p.name != 'UPDATE-INTEGRITY.json'}
    links = {p.relative_to(root).as_posix(): os.readlink(p) for p in sorted(root.rglob('*')) if p.is_symlink()}
    write(root / 'UPDATE-INTEGRITY.json', {'files': files, 'links': links})


def modified(root):
    root = Path(root)
    record = read(root / 'UPDATE-INTEGRITY.json')
    files, links = record.get('files'), record.get('links', {})
    if not isinstance(files, dict) or not files:
        return True
    for name, expected in files.items():
        path = Path(root) / safe_name(name)
        if not path.is_file() or sha(path) != expected:
            return True
    for name, expected in links.items():
        path = root / safe_name(name)
        if not path.is_symlink() or os.readlink(path) != expected:
            return True
    names = {p.relative_to(root).as_posix() for p in root.rglob('*')
             if (p.is_file() or p.is_symlink()) and '__pycache__' not in p.parts
             and '.businessos' not in p.relative_to(root).parts and p.name not in {'Thumbs.db', 'desktop.ini', '.DS_Store'}}
    if names - set(files) - set(links) - {'UPDATE-INTEGRITY.json'}:
        return True
    return False


def runtime_fingerprint(root):
    """Identify an installed runtime by its expected files and link targets."""
    integrity = read(Path(root) / 'UPDATE-INTEGRITY.json')
    entries = {}
    for kind in ('files', 'links'):
        records = integrity.get(kind, {})
        if not isinstance(records, dict):
            return ''
        entries[kind] = {name: value for name, value in records.items() if name.startswith(RUNTIME + '/')}
    return hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest() if entries['files'] else ''


def safe_name(name):
    if ('\\' in name or ':' in name or PurePosixPath(name).is_absolute() or
            PureWindowsPath(name).is_absolute() or '..' in PurePosixPath(name).parts):
        raise ValueError('The update contains an unsafe file path.')
    return Path(name)


def extract(archive, destination):
    """Bound extraction and reject escapes/devices, including archive links."""
    destination = Path(destination)
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as bundle:
            members = bundle.infolist()
            if len(members) > 60000 or sum(m.file_size for m in members) > MAX_UNPACKED:
                raise ValueError('The update is too large to unpack safely.')
            for member in members:
                safe_name(member.filename)
                if stat.S_ISLNK(member.external_attr >> 16):
                    raise ValueError('The ZIP contains an unsupported link.')
            bundle.extractall(destination)
    else:
        with tarfile.open(archive, 'r:gz') as bundle:
            members = bundle.getmembers()
            if len(members) > 60000 or sum(m.size for m in members) > MAX_UNPACKED:
                raise ValueError('The update is too large to unpack safely.')
            for member in members:
                safe_name(member.name)
                if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
                    raise ValueError('The update contains an unsupported file.')
                # Python's data filter also checks resolved link destinations.
                tarfile.data_filter(member, str(destination))
            bundle.extractall(destination, filter='data')
    roots = list(destination.iterdir())
    if len(roots) != 1 or not roots[0].is_dir() or roots[0].is_symlink():
        raise ValueError('The update does not contain one AURA app folder.')
    return roots[0]


def release_choice(rows, current, target):
    if not isinstance(rows, list):
        raise ValueError('The release list could not be read.')
    candidates = []
    for row in rows:
        tag = row.get('tag_name', '')
        if row.get('draft') or not version(tag) > version(current):
            continue
        # AURA's published Alpha releases currently use numeric tags marked prerelease.
        # Development/RC/nightly suffixes are deliberately not selected.
        if not re.fullmatch(r'v\d+\.\d+\.\d+', tag):
            continue
        suffix = '.zip' if target.startswith('windows') else '.tar.gz'
        name = 'viraltrac-aura-' + tag + '-' + target + suffix
        asset = next((a for a in row.get('assets', []) if a.get('name') == name), {})
        valid = verified_asset(asset, tag, target)
        app = next((a for a in row.get('assets', []) if verified_asset(a, tag, target, app_only=True)), None)
        candidates.append({'version': tag[1:], 'tag': tag, 'notes': str(row.get('body') or '')[:18000],
                           'url': PAGE + '/tag/' + tag, 'asset': asset if valid else None,
                           'app_asset': app, 'published': row.get('published_at', '')})
    ready = [candidate for candidate in candidates if candidate['asset']]
    return max(ready or candidates, key=lambda r: version(r['version']), default=None)


def verified_asset(asset, tag, target, app_only=False):
    if not re.fullmatch(r'v\d+\.\d+\.\d+', str(tag)):
        return False
    stem = 'viraltrac-aura-' + tag + '-' + target
    suffix = '.zip' if target.startswith('windows') else '.tar.gz'
    name = asset.get('name') or ''
    matches = (re.fullmatch(re.escape(stem) + r'-app-[a-f0-9]{64}' + re.escape(suffix), name)
               if app_only else name == stem + suffix)
    return (bool(matches) and re.fullmatch(r'sha256:[a-f0-9]{64}', asset.get('digest') or '') and
            asset.get('browser_download_url') == DOWNLOADS + tag + '/' + name and
            isinstance(asset.get('size'), int) and 0 < asset['size'] <= MAX_DOWNLOAD)


def fetch_json(url):
    with urlopen(Request(url, headers={'User-Agent': 'ViralTrac-AURA', 'Accept': 'application/vnd.github+json'}), timeout=20) as response:
        raw = response.read(2 * 1024 * 1024 + 1)
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError('The release list is too large.')
    return json.loads(raw)


def code_fingerprint(product=Path(__file__).resolve().parents[1]):
    """What AURA's own code looks like on disk (names, sizes and change times of its scripts)."""
    digest = hashlib.sha256()
    try:
        for path in sorted((Path(product) / 'scripts').glob('*.py')):
            info = path.stat()
            digest.update(f'{path.name}:{info.st_size}:{info.st_mtime_ns};'.encode())
    except OSError:
        return ''
    return digest.hexdigest()


# A running AURA keeps the code it loaded when it started. If its files later change underneath
# it (a Git pull, a synced or copied folder, an edit), the screens load fresh but the engine does
# not, so AURA says a restart will finish the update instead of failing in confusing ways.
STARTED_CODE = code_fingerprint()
_code_check = {'at': None, 'changed': False}


def restart_needed():
    if not _code_check['changed'] and (_code_check['at'] is None or time.monotonic() - _code_check['at'] > 10):
        current = code_fingerprint()
        _code_check.update(at=time.monotonic(), changed=bool(STARTED_CODE and current and current != STARTED_CODE))
    return _code_check['changed']


class Updater:
    def __init__(self, product, store=None):
        self.product = Path(product).resolve()
        self.store = (Path(store) if store else state_dir() / 'updates').resolve()
        self.path = self.store / 'settings.json'
        self.lock = threading.RLock()
        self.operation = None
        self.status = 'idle'
        self.message = ''
        self.prepared = None
        self.apply_when_idle = False
        self.install_lock = None
        self.progress = None
        self.timings = {}
        self.phase_started = None
        self.waiting_for = ''
        self.settling = False

    def phase(self, status, message=''):
        with self.lock:
            now = time.monotonic()
            if self.phase_started is not None:
                self.timings[self.status] = round(self.timings.get(self.status, 0) + now - self.phase_started, 1)
            self.status, self.message = status, message
            self.phase_started = now

    def result(self, outcome, target):
        seconds = dict(self.timings)
        if self.phase_started is not None and self.status in BUSY | {'ready'}:
            seconds[self.status] = round(seconds.get(self.status, 0) + time.monotonic() - self.phase_started, 1)
        return {'outcome': outcome, 'version': target, 'seconds': seconds,
                'download': self.progress, 'at': time.time()}

    def state(self):
        with self.lock:
            saved = read(self.path)
            current = (self.product / 'VERSION').read_text(encoding='utf-8').strip()
            release = saved.get('release')
            available = bool(release and version(release['version']) > version(current))
            policy = saved.get('policy', 'notify')
            skipped = available and saved.get('skipped') == release['version']
            visible = available and not skipped and policy != 'manual' and saved.get('later_until', 0) <= time.time()
            runtime = read(self.product / 'BUNDLED-RUNTIME.json')
            source = (self.product / '.git').exists() or not runtime
            previous = saved.get('previous')
            return {'current': current, 'policy': policy, 'checked_at': saved.get('checked_at'),
                    'release': release if available else None, 'status': self.status,
                    'message': self.message or saved.get('error', ''), 'prepared': bool(self.prepared),
                    'progress': self.progress if self.status == 'downloading' else None,
                    'waiting_for': self.waiting_for if self.status == 'ready' else '',
                    'last_update': saved.get('last_update'),
                    'pending': self.apply_when_idle, 'notice': bool(visible),
                    'unread': bool(visible and saved.get('read_version') != release['version']),
                    'can_install': bool(not source and available and release.get('asset')),
                    'manual_reason': 'This is a source checkout. Update it through Git.' if (self.product / '.git').exists() else
                        'Download a bundled AURA app to use one-click updates.' if not runtime else
                        'A verified download for this computer is not available yet.' if available and not release.get('asset') else '',
                    'rollback': Path(previous).name if not source and str(self.product) in {saved.get('active'), saved.get('settled_from')} and previous and Path(previous).is_dir() else None,
                    'home_note': saved.get('home_note', ''),
                    'releases_url': PAGE, 'restart_needed': restart_needed()}

    def save(self, **values):
        with self.lock:
            # Reuse the native file lease so windows for different workspaces
            # cannot overwrite one another's global update choices.
            from workspace_startup import VisualInstance
            lease = VisualInstance(self.store / 'settings-write')
            lease.path = self.store / 'settings-write.json'
            for _ in range(50):
                if lease.acquire():
                    break
                time.sleep(.01)
            else:
                raise ValueError('Another AURA window is saving update settings. Try again.')
            try:
                saved = read(self.path)
                saved.update(values)
                write(self.path, saved)
            finally:
                lease.close()

    def check(self, force=False):
        with self.lock:
            saved = read(self.path)
            if not force and (saved.get('policy') == 'manual' or time.time() - saved.get('attempted_at', saved.get('checked_at', 0)) < DAY):
                return
            if self.status in BUSY:
                return
            self.status, self.message = 'checking', 'Checking for updates…'
        try:
            # Cache the latest published bundle for every installed copy on this
            # computer; each view compares it with its own running version.
            result = release_choice(fetch_json(RELEASES), '0.0.0', native_platform())
            changes = {'error': ''} if not saved.get('last_update') else {}
            self.save(checked_at=time.time(), attempted_at=time.time(), release=result, **changes)
            self.message = ''
        except Exception:
            # Keep the last good result and back off rather than retrying on every poll.
            try:
                self.save(attempted_at=time.time())
            except OSError:
                pass
            self.message = 'Couldn’t check for updates. Check your internet connection and try again.'
        finally:
            self.status = 'ready' if self.prepared else 'idle'

    def start(self, function):
        with self.lock:
            if self.operation and self.operation.is_alive():
                raise ValueError('An update is already being checked or prepared.')
            self.operation = threading.Thread(target=function, daemon=True)
            self.operation.start()

    def action(self, action, policy=None):
        with self.lock:
            if self.status in BUSY and action != 'read':
                raise ValueError('Wait for the update to finish preparing before changing update settings.')
            state = self.state()
            release = state.get('release') or {}
            if action == 'check':
                self.start(lambda: self.check(True))
                self.status, self.message = 'checking', 'Checking for updates…'
            elif action == 'policy':
                if policy not in {'notify', 'auto', 'manual'}:
                    raise ValueError('Choose when AURA should update.')
                self.save(policy=policy)
                if policy != 'auto':
                    self.cancel_pending()
            elif action == 'read':
                self.save(read_version=release.get('version'))
            elif action in {'later', 'skip'}:
                self.save(**({'later_until': time.time() + DAY} if action == 'later' else {'skipped': release.get('version')}))
                self.cancel_pending()
            elif action == 'install':
                if self.settling:
                    raise ValueError('AURA is finishing its last update. Try again in a minute.')
                if not state['can_install']:
                    raise ValueError(state['manual_reason'] or 'No newer update is available.')
                self.start(self.prepare)
                self.status, self.message = 'preparing', 'Preparing the update…'
            elif action == 'rollback':
                if self.settling:
                    raise ValueError('AURA is finishing its last update. Try again in a minute.')
                if not state['rollback']:
                    raise ValueError(state['manual_reason'] or 'The previous version is only available from your current updated app.')
                if self.operation and self.operation.is_alive():
                    raise ValueError('Wait for the current update check to finish.')
                previous = read(self.path).get('previous')
                if not previous or not Path(previous).is_dir():
                    raise ValueError('The previous app version is no longer in its saved folder.')
                if schema_hash(Path(previous), True) != schema_hash(self.product, True):
                    raise ValueError('The previous version saves records differently and may not read what this one saved. '
                                     'AURA backed up your workspace before this version first opened it: restore that backup '
                                     '(Back up or restore) into a new folder, then open it with the previous version from Downloads.')
                if modified(Path(previous)):
                    raise ValueError('The previous app files have changed. Open that copy separately to review your changes.')
                bundled_python(Path(previous))
                self.acquire_install()
                self.timings, self.progress, self.phase_started = {}, None, None
                self.prepared = Path(previous)
                self.apply_when_idle = True
                self.phase('ready', 'The previous version will open when AURA is idle.')
            else:
                raise ValueError('Choose an update action.')
            return self.state()

    def acquire_install(self):
        if self.install_lock:
            return
        from workspace_startup import VisualInstance
        guard = VisualInstance(self.store / 'installer')
        guard.path = self.store / 'install.json'
        if not guard.acquire():
            raise ValueError('Another AURA window is preparing an update. Wait for it to finish.')
        self.install_lock = guard

    def cancel_pending(self):
        self.apply_when_idle = False
        self.prepared = None
        self.waiting_for = ''
        if self.status == 'ready':
            self.status, self.message = 'idle', ''
        if self.install_lock:
            self.install_lock.close()
            self.install_lock = None

    def prepare(self):
        temporary = None
        release = {}
        with self.lock:
            self.timings, self.progress, self.phase_started = {}, None, None
            self.phase('preparing', 'Preparing the update…')
        try:
            self.acquire_install()
        except (OSError, ValueError) as exc:
            self.phase('error', str(exc) if isinstance(exc, ValueError) else 'AURA couldn’t open its update folder. Try again.')
            return
        try:
            state = self.state()
            release = state['release'] or {}
            if not state['can_install']:
                raise ValueError(state['manual_reason'] or 'There is no update to install.')
            if modified(self.product):
                raise ValueError('Your app files have been customized. Download the new version separately to keep your changes.')
            asset = release['asset']
            tag, platform = release.get('tag'), native_platform()
            if tag != 'v' + release['version'] or not verified_asset(asset, tag, platform):
                raise ValueError('The saved release details are incomplete. Check for updates again.')
            self.store.mkdir(parents=True, exist_ok=True)
            # Room for the download, its unpacked app (about three times the ZIP) and a copy of the current version.
            needed = 4 * asset['size'] + 256 * 1024 * 1024
            if shutil.disk_usage(self.store).free < needed:
                raise ValueError(f'There isn’t enough free space. Free up {-(-needed // (1024 * 1024))} MB and try again.')
            # Short folder names: an app folder holds paths over 100 characters, and Windows without long paths
            # turned on stops at 260 in all.
            temporary = Path(tempfile.mkdtemp(prefix='u-', dir=self.store))
            app = release.get('app_asset') or {}
            fingerprint = runtime_fingerprint(self.product) if app else ''
            target = None
            if (fingerprint and verified_asset(app, tag, platform, app_only=True) and
                    '-app-' + fingerprint + '.' in app['name'] and app['size'] < asset['size']):
                try:
                    target = self.download(app, temporary / 'a')
                    reuse_runtime(self.product, target, fingerprint)
                    self.validate_target(target, release['version'], platform)
                    asset = app
                except (OSError, ValueError, subprocess.SubprocessError, tarfile.TarError, zipfile.BadZipFile):
                    target = None
            if target is None:
                target = self.download(asset, temporary / 'f', fallback=self.progress is not None)
                self.validate_target(target, release['version'], platform)
            versions = self.store / 'versions'
            versions.mkdir(exist_ok=True)
            if versions.is_symlink() or versions.resolve().parent != self.store.resolve():
                raise ValueError('The update folder points somewhere else. Use Downloads to install this version separately.')
            destination = versions / (release['tag'] + '-' + asset['digest'][7:15] + '-' + format(time.time_ns() % 16 ** 6, '06x'))
            target.rename(destination)
            self.save(error='', failed_version=None)
            with self.lock:
                self.prepared = destination
                self.phase('ready', 'Update ready. AURA will restart when idle.')
                self.apply_when_idle = True
        except Exception as exc:
            self.apply_when_idle = False
            message = (str(exc) if isinstance(exc, ValueError) else
                'The download was interrupted. Check your internet connection and try again.' if isinstance(exc, (URLError, TimeoutError)) else
                'AURA couldn’t save the update. Check access to your local app folder and try again.' if isinstance(exc, PermissionError) else
                'The downloaded app couldn’t start. Your current version is unchanged. Try again or use Downloads.' if isinstance(exc, subprocess.SubprocessError) else
                'The update could not be prepared. Your current version is unchanged. Try again.')
            self.phase('error', message)
            try:
                self.save(error=message, failed_version=release.get('version'),
                          last_update=self.result('failed', release.get('version')))
            except (OSError, ValueError):
                pass
            self.cancel_pending()
        finally:
            if temporary and not temporary.is_symlink() and temporary.resolve().parent == self.store.resolve():
                shutil.rmtree(temporary, ignore_errors=True)

    def download(self, asset, directory, fallback=False):
        directory.mkdir()
        archive = directory / asset['name']
        with self.lock:
            self.progress = {'bytes': 0, 'total': asset['size']}
            self.phase('downloading', 'Downloading the full update…' if fallback else 'Downloading the update…')
        with urlopen(Request(asset['browser_download_url'], headers={'User-Agent': 'ViralTrac-AURA'}), timeout=60) as response, archive.open('wb') as output:
            final = urlsplit(response.geturl())
            if final.scheme != 'https' or final.hostname not in {'github.com', 'release-assets.githubusercontent.com', 'objects.githubusercontent.com'}:
                raise ValueError('The download did not come from GitHub’s release service.')
            read_block = getattr(response, 'read1', response.read)
            total = 0
            while block := read_block(64 * 1024):
                total += len(block)
                if total > asset['size'] or total > MAX_DOWNLOAD:
                    raise ValueError('The download size does not match the release.')
                output.write(block)
                with self.lock:
                    self.progress = {'bytes': total, 'total': asset['size']}
        self.phase('verifying', 'Verifying and preparing the update…')
        if total != asset['size'] or 'sha256:' + sha(archive) != asset['digest']:
            raise ValueError('The download could not be verified. Try downloading it again.')
        unpacked = directory / 'x'
        unpacked.mkdir()
        return extract(archive, unpacked)

    def validate_target(self, target, release_version, platform):
        metadata = read(target / 'BUNDLED-RUNTIME.json')
        if (metadata.get('platform') != platform or metadata.get('aura_version') != release_version or
                (target / 'VERSION').read_text(encoding='utf-8').strip() != release_version or modified(target)):
            raise ValueError('The update does not match this computer or its release.')
        if metadata.get('update_protocol') != 1 or metadata.get('workspace_schema_sha256') != schema_hash(target):
            raise ValueError('The update does not match this computer or its release.')
        # A newer version may save records in a newer format. It backs up each workspace before it first saves there
        # (workspace_storage.protect_format), so the update itself needs nothing from the person.
        interpreter = bundled_python(target)
        probe = "import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import yaml,jsonschema,workspace_ui"
        subprocess.run([str(interpreter), '-I', '-B', '-c', probe, str(target / 'scripts')],
                       check=True, capture_output=True, timeout=45, **hidden_process())


def reuse_runtime(current, target, fingerprint):
    if (target / RUNTIME).exists() or (target / RUNTIME).is_symlink() or runtime_fingerprint(target) != fingerprint:
        raise ValueError('The smaller update needs a different runtime.')
    shutil.copytree(current / RUNTIME, target / RUNTIME, symlinks=True)


def hidden_process():
    return {'creationflags': subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {'start_new_session': True}


def bundled_python(root):
    root = Path(root).resolve()
    name = read(root / 'BUNDLED-RUNTIME.json').get('interpreter', '')
    path = (root / safe_name(name)).resolve()
    if not name or not path.is_relative_to(root / '.aura-runtime') or not path.is_file():
        raise ValueError('The app’s bundled Python is missing. Download the complete app again.')
    return path


def launch_target(product):
    """The user's original launcher follows only its explicitly managed app chain."""
    product = Path(product).resolve()
    saved = read(state_dir() / 'updates/settings.json')
    active = saved.get('active')
    if active and str(product) in saved.get('launch_roots', []) and Path(active).resolve() != product:
        target = Path(active).resolve()
        try:
            bundled_python(target)
            if (target / 'scripts/open_aura.py').is_file():
                return target
        except ValueError:
            pass
    return None


def handoff(updater, workspace, business, port, extra):
    """Listener is closed first. Commit the launch pointer only after a healthy start."""
    import workspace_startup
    target, previous = Path(updater.prepared).resolve(), updater.product
    target_version = (target / 'VERSION').read_text(encoding='utf-8').strip()
    previous_version = (previous / 'VERSION').read_text(encoding='utf-8').strip()
    if updater.status != 'restarting':
        updater.phase('restarting', 'Restarting AURA…')
    startup = workspace_startup.status()
    def launch(root):
        interpreter = bundled_python(root)
        if os.name == 'nt' and interpreter.with_name('pythonw.exe').exists():
            interpreter = interpreter.with_name('pythonw.exe')
        argv = [str(interpreter), '-X', 'utf8', '-E', '-s', '-B', str(root / 'scripts/open_aura.py'),
                '--workspace', str(workspace), '--port', str(port), '--no-open', *extra]
        if business:
            argv += ['--business-id', business]
        env = dict(os.environ, AURA_UPDATE_HANDOFF='1')
        log = updater.store / 'launch.log'
        with log.open('ab') as output:
            process = subprocess.Popen(argv, env=env, stdin=subprocess.DEVNULL, stdout=output, stderr=output, **hidden_process())
        for _ in range(120):
            if process.poll() is not None:
                break
            try:
                with urlopen('http://127.0.0.1:' + str(port) + '/', timeout=.5) as response:
                    page = response.read(1024 * 1024).decode()
                token = re.search(r'name="aura-token" content="([^"]+)"', page).group(1)
                request = Request('http://127.0.0.1:' + str(port) + '/api/state', headers={'X-Aura-Token': token})
                with urlopen(request, timeout=2) as response:
                    state = json.load(response)
                if (Path(state['product']).resolve() == root and Path(state['workspace']).resolve() == Path(workspace).resolve()
                        and state['version'] == (root / 'VERSION').read_text(encoding='utf-8').strip()):
                    return process
            except (OSError, ValueError, KeyError, AttributeError):
                pass
            time.sleep(.25)
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=10)
        raise ValueError('The updated app could not open.')
    try:
        launch(target)
    except Exception:
        try:
            launch(previous)
            updater.save(error='The update could not open. Your previous version has been restored.',
                         failed_version=(read(updater.path).get('release') or {}).get('version'),
                         last_update=updater.result('restored', target_version))
        except Exception:
            updater.save(error='AURA couldn’t reopen. Open your original download. Your workspace files are unchanged.',
                         last_update=updater.result('failed', target_version))
            raise
        finally:
            updater.cancel_pending()
        return
    saved = read(updater.path)
    roots = list(dict.fromkeys([*saved.get('launch_roots', []), str(previous), str(target)]))
    skipped_version = previous_version if version(target_version) < version(previous_version) else target_version
    updater.save(active=str(target), previous=str(previous), launch_roots=roots, error='', settled_from='', home_note='',
                 last_update=updater.result('rolled_back' if target_version != skipped_version else 'updated', target_version),
                 skipped=skipped_version)
    if startup.get('enabled'):
        try:
            workspace_startup.configure(True, target, workspace, business, extra, interpreter=bundled_python(target))
        except (OSError, ValueError, subprocess.SubprocessError):
            updater.save(error='AURA updated. Open Settings → Startup & updates and save once to update automatic startup.')
    updater.cancel_pending()


# One AURA folder. An update is prepared and started from a verified copy in AURA's settings folder; the folder the
# person opens AURA from (their download) is then brought to that same version, so it is the one current AURA for
# them, for AI apps working in it, and for its launcher. The version it held is kept as the one to go back to.

def _versions(store):
    return (Path(store) / 'versions').resolve()


def home_folders(saved, store):
    """The folders the person opens AURA from, as opposed to AURA's own update copies."""
    versions = _versions(store)
    return [Path(r).resolve() for r in saved.get('launch_roots', [])
            if not Path(r).resolve().is_relative_to(versions) and (Path(r) / 'UPDATE-INTEGRITY.json').is_file()]


def _replace(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    staged = target.with_name(target.name + '.aura~')
    shutil.copy2(source, staged)
    os.replace(staged, target)


def mirror(source, home):
    """Make `home` hold exactly the verified files of `source`. Only files named in AURA's own file lists are written
    or removed; anything else in the folder stays. Unchanged files (usually the whole bundled Python) are skipped."""
    source, home = Path(source), Path(home)
    new, old = read(source / 'UPDATE-INTEGRITY.json'), read(home / 'UPDATE-INTEGRITY.json')
    files, links = new.get('files') or {}, new.get('links') or {}
    if not files:
        raise ValueError('The running version has no file list.')
    # The bundled Python first: if another program is still using it, nothing else has changed yet.
    for name in sorted(files, key=lambda n: not n.startswith(RUNTIME + '/')):
        target = home / safe_name(name)
        if target.is_file() and not target.is_symlink() and sha(target) == files[name]:
            continue
        if target.is_symlink():
            target.unlink()
        _replace(source / safe_name(name), target)
    for name, value in links.items():
        target = home / safe_name(name)
        if target.is_symlink() and os.readlink(target) == value:
            continue
        if target.is_symlink() or target.is_file():
            target.unlink()
        target.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(value, target)
    for name in set(old.get('files') or {}) | set(old.get('links') or {}):
        if name in files or name in links:
            continue
        path = home / safe_name(name)
        if path.is_symlink() or path.is_file():
            path.unlink()
        parent = path.parent
        while parent != home and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent
    _replace(source / 'UPDATE-INTEGRITY.json', home / 'UPDATE-INTEGRITY.json')
    if modified(home) or (home / 'VERSION').read_text(encoding='utf-8') != (source / 'VERSION').read_text(encoding='utf-8'):
        raise ValueError('The AURA folder did not match the running version after the update.')


def settle(updater, wait=120):
    """Run by the version that just started after an update or a return to the previous version. Whatever can't be
    done now leaves AURA running from its verified copy, and is tried again at the next start."""
    product, store = updater.product, updater.store
    if not product.is_relative_to(_versions(store)):
        return None
    from workspace_startup import VisualInstance
    guard = VisualInstance(store / 'installer')
    guard.path = store / 'install.json'
    deadline = time.monotonic() + wait
    # The version that handed over finishes recording the update, then lets go of this lock.
    while not guard.acquire():
        if time.monotonic() > deadline:
            return None
        time.sleep(1)
    updater.settling = True
    try:
        saved = read(updater.path)
        homes = [h for h in home_folders(saved, store) if h != product]
        if saved.get('active') != str(product) or not homes:
            return None
        previous = Path(saved['previous']).resolve() if saved.get('previous') else None
        current = (product / 'VERSION').read_text(encoding='utf-8').strip()
        done, notes = [], []
        for home in homes:
            if modified(home):
                notes.append(f'Your AURA folder {home} has changes of your own, so it was left as it was. '
                             f'AURA {current} runs from {product}.')
                continue
            if home == previous:
                # Keep the version this folder holds to go back to, before the folder changes.
                kept = _versions(store) / ('v' + (home / 'VERSION').read_text(encoding='utf-8').strip() + '-kept-' +
                                           format(time.time_ns() % 16 ** 6, '06x'))
                staging = kept.with_name(kept.name + '.partial')
                shutil.copytree(home, staging, symlinks=True, ignore=shutil.ignore_patterns('__pycache__', '.businessos'))
                if modified(staging):
                    shutil.rmtree(staging, ignore_errors=True)
                    raise ValueError('The copy of the previous version could not be verified.')
                staging.rename(kept)
                previous = kept
            for attempt in range(24):
                try:
                    mirror(product, home)
                    break
                except PermissionError:
                    # Another program (often the version that just closed) still has a file open.
                    if attempt == 23:
                        raise
                    time.sleep(5)
            done.append(home)
        changes = {'home_note': ' '.join(notes)}
        if done:
            roots = list(dict.fromkeys([*saved.get('launch_roots', []), *map(str, done)]))
            changes.update(active=str(done[0]), settled_from=str(product), launch_roots=roots,
                           previous=str(previous) if previous else saved.get('previous'))
        updater.save(**changes)
        if done:
            import workspace_startup
            startup = workspace_startup.status()
            if startup.get('enabled') and startup.get('workspace') and Path(startup.get('product') or '.').resolve() != done[0]:
                workspace_startup.configure(True, done[0], startup['workspace'], interpreter=bundled_python(done[0]))
        return done
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' AURA will finish bringing its folder to this version at the next start: ' +
              str(error)[:300], flush=True)
        return None
    finally:
        updater.settling = False
        guard.close()


def prune(updater, keep_previous=True):
    """AURA's own update copies, kept to what is needed: the running version, the active one and (normally) one to go
    back to. A copy that something on this computer still starts is kept; leftovers a day old are cleared."""
    store = updater.store
    versions = _versions(store)
    if not versions.is_dir():
        return []
    from workspace_startup import VisualInstance, shortcut_status, status
    guard = VisualInstance(store / 'installer')
    guard.path = store / 'install.json'
    if not guard.acquire():
        return []
    try:
        saved = read(updater.path)
        keep = {updater.product.resolve(), *(Path(p).resolve() for p in (saved.get('active'), status().get('product'),
                                                                          shortcut_status().get('product')) if p)}
        try:
            import workspace_os_schedules
            # A task on the computer's scheduler names the AURA folder whose helper runs it.
            keep |= {Path(task['runner'][1]).resolve().parents[1] for task in workspace_os_schedules.definitions()
                     if len(task.get('runner') or []) > 1}
        except (OSError, ValueError, KeyError, TypeError, IndexError):
            return []
        if keep_previous and saved.get('previous'):
            keep.add(Path(saved['previous']).resolve())
        removed = []
        for folder in versions.iterdir():
            if folder.is_symlink() or not folder.is_dir() or folder.resolve() in keep:
                continue
            if folder.name.endswith('.partial') and time.time() - folder.stat().st_mtime < DAY:
                continue
            shutil.rmtree(folder, ignore_errors=True)
            if not folder.exists():
                removed.append(str(folder))
        for folder in [*store.glob('preparing-*'), *store.glob('u-*')]:
            if folder.is_dir() and not folder.is_symlink() and time.time() - folder.stat().st_mtime > DAY:
                shutil.rmtree(folder, ignore_errors=True)
        if removed:
            changes = {'launch_roots': [r for r in saved.get('launch_roots', []) if r not in removed]}
            if saved.get('previous') in removed:
                changes['previous'] = None
            updater.save(**changes)
        return removed
    finally:
        guard.close()
