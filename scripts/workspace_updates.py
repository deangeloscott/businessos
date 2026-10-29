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


def schema_hash(root):
    digest = hashlib.sha256()
    for path in sorted([*Path(root).glob('core/**/*.schema.json'), *Path(root).glob('systems/**/*.schema.json')]):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(path.read_bytes())
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
        candidates.append({'version': tag[1:], 'tag': tag, 'notes': str(row.get('body') or '')[:18000],
                           'url': PAGE + '/tag/' + tag, 'asset': asset if valid else None,
                           'published': row.get('published_at', '')})
    return max(candidates, key=lambda r: version(r['version']), default=None)


def verified_asset(asset, tag, target):
    if not re.fullmatch(r'v\d+\.\d+\.\d+', str(tag)):
        return False
    name = 'viraltrac-aura-' + tag + '-' + target + ('.zip' if target.startswith('windows') else '.tar.gz')
    return (asset.get('name') == name and re.fullmatch(r'sha256:[a-f0-9]{64}', asset.get('digest') or '') and
            asset.get('browser_download_url') == DOWNLOADS + tag + '/' + name and
            isinstance(asset.get('size'), int) and 0 < asset['size'] <= MAX_DOWNLOAD)


def fetch_json(url):
    with urlopen(Request(url, headers={'User-Agent': 'ViralTrac-AURA', 'Accept': 'application/vnd.github+json'}), timeout=20) as response:
        raw = response.read(2 * 1024 * 1024 + 1)
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError('The release list is too large.')
    return json.loads(raw)


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

    def state(self):
        with self.lock:
            saved = read(self.path)
            current = (self.product / 'VERSION').read_text().strip()
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
                    'pending': self.apply_when_idle, 'notice': bool(visible),
                    'unread': bool(visible and saved.get('read_version') != release['version']),
                    'can_install': bool(not source and available and release.get('asset')),
                    'manual_reason': 'This is a source checkout. Update it through Git.' if (self.product / '.git').exists() else
                        'Download a bundled AURA app to use one-click updates.' if not runtime else
                        'A verified download for this computer is not available yet.' if available and not release.get('asset') else '',
                    'rollback': Path(previous).name if not source and saved.get('active') == str(self.product) and previous and Path(previous).is_dir() else None,
                    'releases_url': PAGE}

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
            if self.status in {'downloading', 'verifying', 'restarting'}:
                return
            self.status, self.message = 'checking', 'Checking for updates…'
        try:
            # Cache the latest published bundle for every installed copy on this
            # computer; each view compares it with its own running version.
            result = release_choice(fetch_json(RELEASES), '0.0.0', native_platform())
            self.save(checked_at=time.time(), attempted_at=time.time(), release=result, error='')
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
            if self.status in {'downloading', 'verifying', 'restarting'} and action != 'read':
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
                if not state['can_install']:
                    raise ValueError(state['manual_reason'] or 'No newer update is available.')
                self.start(self.prepare)
                self.status, self.message = 'downloading', 'Downloading the update…'
            elif action == 'rollback':
                if not state['rollback']:
                    raise ValueError(state['manual_reason'] or 'The previous version is only available from your current updated app.')
                if self.operation and self.operation.is_alive():
                    raise ValueError('Wait for the current update check to finish.')
                previous = read(self.path).get('previous')
                if not previous or not Path(previous).is_dir():
                    raise ValueError('The previous app version is no longer in its saved folder.')
                if schema_hash(Path(previous)) != schema_hash(self.product):
                    raise ValueError('The previous version needs a different workspace format. Restore a backup before using it.')
                if modified(Path(previous)):
                    raise ValueError('The previous app files have changed. Open that copy separately to review your changes.')
                bundled_python(Path(previous))
                self.acquire_install()
                self.prepared = Path(previous)
                self.apply_when_idle = True
                self.status = 'ready'
                self.message = 'The previous version will open when AURA is idle.'
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
        if self.status == 'ready':
            self.status, self.message = 'idle', ''
        if self.install_lock:
            self.install_lock.close()
            self.install_lock = None

    def prepare(self):
        temporary = None
        try:
            # One installer across independent windows/processes. OS releases locks on crash.
            self.acquire_install()
            state = self.state()
            if not state['can_install']:
                raise ValueError(state['manual_reason'] or 'There is no update to install.')
            if modified(self.product):
                raise ValueError('Your app files have been customized. Download the new version separately to keep your changes.')
            self.status, self.message = 'downloading', 'Downloading the update…'
            release = state['release']
            asset = release['asset']
            if release.get('tag') != 'v' + release['version'] or not verified_asset(asset, release.get('tag'), native_platform()):
                raise ValueError('The saved release details are incomplete. Check for updates again.')
            self.store.mkdir(parents=True, exist_ok=True)
            if shutil.disk_usage(self.store).free < asset['size'] + MAX_UNPACKED:
                raise ValueError('There isn’t enough free space. Free up 4 GB and try again.')
            temporary = Path(tempfile.mkdtemp(prefix='preparing-', dir=self.store))
            archive = temporary / asset['name']
            with urlopen(Request(asset['browser_download_url'], headers={'User-Agent': 'ViralTrac-AURA'}), timeout=60) as response, archive.open('wb') as output:
                final = urlsplit(response.geturl())
                if final.scheme != 'https' or final.hostname not in {'github.com', 'release-assets.githubusercontent.com', 'objects.githubusercontent.com'}:
                    raise ValueError('The download did not come from GitHub’s release service.')
                total = 0
                while block := response.read(1024 * 1024):
                    total += len(block)
                    if total > asset['size'] or total > MAX_DOWNLOAD:
                        raise ValueError('The download size does not match the release.')
                    output.write(block)
            self.status, self.message = 'verifying', 'Checking the download…'
            if archive.stat().st_size != asset['size'] or 'sha256:' + sha(archive) != asset['digest']:
                raise ValueError('The download could not be verified. Try downloading it again.')
            unpacked = temporary / 'unpacked'
            unpacked.mkdir()
            target = extract(archive, unpacked)
            metadata = read(target / 'BUNDLED-RUNTIME.json')
            if (metadata.get('platform') != native_platform() or metadata.get('aura_version') != release['version'] or
                    (target / 'VERSION').read_text().strip() != release['version'] or modified(target)):
                raise ValueError('The update does not match this computer or its release.')
            if metadata.get('update_protocol') != 1 or metadata.get('workspace_schema_sha256') != schema_hash(target) or schema_hash(target) != schema_hash(self.product):
                raise ValueError('This version needs a workspace upgrade. Back up your workspace and follow the release notes.')
            interpreter = bundled_python(target)
            probe = "import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import yaml,jsonschema,workspace_ui"
            subprocess.run([str(interpreter), '-I', '-B', '-c', probe, str(target / 'scripts')],
                           check=True, capture_output=True, timeout=45, **hidden_process())
            versions = self.store / 'versions'
            versions.mkdir(exist_ok=True)
            if versions.is_symlink() or versions.resolve().parent != self.store.resolve():
                raise ValueError('The update folder points somewhere else. Use Downloads to install this version separately.')
            destination = versions / (release['tag'] + '-' + native_platform() + '-' + asset['digest'][7:19] + '-' + str(time.time_ns()))
            target.rename(destination)
            self.prepared = destination
            self.apply_when_idle = True
            self.save(error='', failed_version=None)
            self.status, self.message = 'ready', 'Update ready. AURA will restart when idle.'
        except Exception as exc:
            self.status = 'error'
            self.apply_when_idle = False
            self.message = (str(exc) if isinstance(exc, ValueError) else
                'The download was interrupted. Check your internet connection and try again.' if isinstance(exc, (URLError, TimeoutError)) else
                'AURA couldn’t save the update. Check access to your local app folder and try again.' if isinstance(exc, PermissionError) else
                'The downloaded app couldn’t start. Your current version is unchanged. Try again or use Downloads.' if isinstance(exc, subprocess.SubprocessError) else
                'The update could not be prepared. Your current version is unchanged. Try again.')
            try:
                self.save(error=self.message, failed_version=(self.state().get('release') or {}).get('version'))
            except OSError:
                pass
            self.cancel_pending()
        finally:
            if temporary and not temporary.is_symlink() and temporary.resolve().parent == self.store.resolve():
                shutil.rmtree(temporary, ignore_errors=True)


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
    startup = workspace_startup.status()
    def launch(root):
        interpreter = bundled_python(root)
        if os.name == 'nt' and interpreter.with_name('pythonw.exe').exists():
            interpreter = interpreter.with_name('pythonw.exe')
        argv = [str(interpreter), '-E', '-s', '-B', str(root / 'scripts/open_aura.py'),
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
                        and state['version'] == (root / 'VERSION').read_text().strip()):
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
                         failed_version=(read(updater.path).get('release') or {}).get('version'))
        except Exception:
            updater.save(error='AURA couldn’t reopen. Open your original download. Your workspace files are unchanged.')
            raise
        finally:
            updater.cancel_pending()
        return
    saved = read(updater.path)
    roots = list(dict.fromkeys([*saved.get('launch_roots', []), str(previous), str(target)]))
    target_version = (target / 'VERSION').read_text().strip()
    previous_version = (previous / 'VERSION').read_text().strip()
    skipped_version = previous_version if version(target_version) < version(previous_version) else target_version
    updater.save(active=str(target), previous=str(previous), launch_roots=roots, error='',
                 skipped=skipped_version)
    if startup.get('enabled'):
        try:
            workspace_startup.configure(True, target, workspace, business, extra, interpreter=bundled_python(target))
        except (OSError, ValueError, subprocess.SubprocessError):
            updater.save(error='AURA updated. Open Settings → Startup & updates and save once to update automatic startup.')
    updater.cancel_pending()
