#!/usr/bin/env python3
"""Run a published Windows app through its real updater and back to the previous version."""
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def small_update(archive):
    """The smaller app-only download built beside the full one (most updates use it)."""
    suffix = archive.name[len(archive.stem):] if archive.suffix == '.zip' else '.tar.gz'
    found = sorted(archive.parent.glob(archive.name[:-len(suffix)] + '-app-*' + suffix))
    return found[0] if len(found) == 1 else None


def serve(old, archive, port):
    sys.path.insert(0, str(old / 'scripts'))
    import workspace_startup
    import workspace_updates

    live_open = workspace_updates.urlopen
    release = workspace_updates.read(workspace_updates.state_dir() / 'updates/settings.json')['release']
    files = {release['asset']['browser_download_url']: archive}
    small = small_update(archive)
    if small and release.get('app_asset'):
        files[release['app_asset']['browser_download_url']] = small

    def candidate_open(request, *args, **kwargs):
        url = getattr(request, 'full_url', '')
        if url in files:
            stream = files[url].open('rb')
            stream.geturl = lambda: url
            return stream
        return live_open(request, *args, **kwargs)

    # The candidate is still private to this build. Only its archive transport
    # is substituted. All checks, staging and application use the released app.
    workspace_updates.urlopen = candidate_open
    workspace_startup.status = lambda: {'enabled': False}
    launcher = old / 'scripts/open_aura.py'
    sys.argv = [str(launcher), '--port', str(port), '--no-open']
    runpy.run_path(str(launcher), run_name='__main__')


def smoke(archive, previous_file=None):
    sys.path.insert(0, str(ROOT / 'scripts'))
    import workspace_updates as updates

    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    previous = updates.release_choice(
        [row for row in updates.fetch_json(updates.RELEASES) if updates.version(row['tag_name']) < updates.version(version)],
        '0.0.0', 'windows-x64')
    assert previous and previous['asset'], 'No older published Windows bundle is available.'
    asset = previous['asset']
    with tempfile.TemporaryDirectory(prefix='AURA Windows upgrade ') as mark:
        root = Path(mark).resolve()
        old_archive = Path(previous_file).resolve() if previous_file else root / asset['name']
        if not previous_file:
            request = Request(asset['browser_download_url'], headers={'User-Agent': 'ViralTrac-AURA'})
            with urlopen(request, timeout=30) as stream, old_archive.open('wb') as output:
                shutil.copyfileobj(stream, output)
        assert old_archive.stat().st_size == asset['size'] and 'sha256:' + updates.sha(old_archive) == asset['digest']
        unpack = root / 'old'
        unpack.mkdir()
        old = updates.extract(old_archive, unpack)
        assert not updates.modified(old)
        tag = 'v' + version
        candidate = {'name': archive.name, 'size': archive.stat().st_size, 'digest': 'sha256:' + updates.sha(archive),
                     'browser_download_url': updates.DOWNLOADS + tag + '/' + archive.name}
        assert updates.verified_asset(candidate, tag, 'windows-x64')
        release = {'version': version, 'tag': tag, 'asset': candidate}
        small = small_update(archive)
        if small:
            # The path most updates take: the app files only, reusing the installed runtime when it matches.
            release['app_asset'] = {'name': small.name, 'size': small.stat().st_size, 'digest': 'sha256:' + updates.sha(small),
                                    'browser_download_url': updates.DOWNLOADS + tag + '/' + small.name}
            assert updates.verified_asset(release['app_asset'], tag, 'windows-x64', app_only=True)
        local = root / 'settings'
        updates.write(local / 'updates/settings.json', {'policy': 'manual', 'release': release})
        workspace = root / 'workspace'
        env = dict(os.environ, AURA_STATE_DIR=str(local), BUSINESSOS_WORKSPACE=str(workspace),
                   BUSINESSOS_WORKSPACE_CONFIG=str(root / 'selection.json'), AURA_WORKSPACES_HOME=str(root / 'workspaces'),
                   LOCALAPPDATA=str(root / 'local'), APPDATA=str(root / 'roaming'), PYTHONDONTWRITEBYTECODE='1')
        env.pop('AURA_UPDATE_HANDOFF', None)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        base = f'http://127.0.0.1:{port}'

        def api(route, data=None):
            with urlopen(base + '/', timeout=2) as response:
                token = re.search(r'name="aura-token" content="([^"]+)"', response.read().decode()).group(1)
            body = json.dumps(data).encode() if data is not None else None
            with urlopen(Request(base + route, data=body, headers={'X-Aura-Token': token, 'Origin': base,
                         'Content-Type': 'application/json'}), timeout=5) as response:
                return json.load(response)

        def await_version(expected, pointer=False):
            deadline = time.monotonic() + 90
            last_seen = {}
            while time.monotonic() < deadline:
                try:
                    state = api('/api/state')
                    saved = updates.read(local / 'updates/settings.json')
                    active = saved.get('active')
                    last_seen = {'version':state.get('version'), 'error':saved.get('error'), 'last_update':saved.get('last_update')}
                    here = {Path(p) for p in (active, saved.get('settled_from')) if p}
                    if state['version'] == expected and (not pointer or Path(state['product']) in here):
                        return state
                    if saved.get('failed_version') == expected and saved.get('error'):
                        raise RuntimeError('AURA could not prepare or activate ' + expected + ': ' + saved['error'])
                except (OSError, ValueError, AttributeError):
                    pass
                time.sleep(.25)
            raise RuntimeError('AURA did not activate and answer as version ' + expected + ': ' + json.dumps(last_seen))

        with (root / 'launcher.log').open('w+', encoding='utf-8') as log:
            server = subprocess.Popen([str(updates.bundled_python(old)), '-B', '-X', 'utf8', __file__, '--serve',
                                       str(old), str(archive), str(port)], env=env, stdout=log, stderr=log)
            try:
                await_version(previous['version'])
                setup = api('/api/setup', {'name': 'Upgrade smoke fixture'})
                marker = workspace / 'keep.txt'
                marker.write_text('Preserve this workspace across upgrades.\n', encoding='utf-8')
                before = updates.sha(marker)
                api('/api/updates', {'action': 'install'})
                state = await_version(version, pointer=True)
                # The folder the person opens AURA from now holds the new version itself, and the version it held is
                # kept to go back to.
                deadline = time.monotonic() + 180
                while time.monotonic() < deadline:
                    saved = updates.read(local / 'updates/settings.json')
                    if saved.get('active') and Path(saved['active']).resolve() == old.resolve():
                        break
                    time.sleep(.5)
                else:
                    raise RuntimeError('The AURA folder was not brought to the new version: ' + json.dumps(saved))
                assert (old / 'VERSION').read_text(encoding='utf-8').strip() == version and not updates.modified(old)
                assert Path(saved['previous']).is_dir() and (Path(saved['previous']) / 'VERSION').read_text(encoding='utf-8').strip() == previous['version']
                download = (saved.get('last_update') or {}).get('download') or {}
                path_taken = 'the smaller app-only download' if small and download.get('total') == small.stat().st_size else 'the full download'
                assert Path(state['workspace']).resolve() == workspace, 'The upgraded app opened a different workspace.'
                assert state['business_id'] == setup['business_id'], 'The upgraded app did not open the saved business.'
                assert updates.sha(marker) == before
                api('/api/updates', {'action': 'rollback'})
                restored = await_version(previous['version'], pointer=True)
                assert restored['business_id'] == setup['business_id'] and updates.sha(marker) == before
            except Exception:
                log.seek(0)
                print(log.read()[-5000:])
                for background in (local/'interface.log',local/'updates/launch.log'):
                    if background.is_file():print(background.read_text(encoding='utf-8',errors='replace')[-5000:])
                raise
            finally:
                try:
                    api('/api/lifecycle', {'action': 'quit'})
                    for _ in range(30):
                        try:
                            with socket.create_connection(('127.0.0.1', port), timeout=.2):
                                pass
                        except OSError:
                            break
                        time.sleep(.1)
                except (OSError, AttributeError):
                    pass
                if server.poll() is None:
                    server.terminate()
                server.wait(timeout=10)
    print(f'Published Windows {previous["version"]} upgraded to {version} using {path_taken}, brought its own folder to '
          f'{version}, and rolled back with its workspace intact.')


if __name__ == '__main__':
    if sys.argv[1] == '--serve':
        serve(Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]))
    else:
        smoke(Path(sys.argv[1]).resolve(), sys.argv[2] if len(sys.argv) > 2 else None)
