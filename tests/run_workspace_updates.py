#!/usr/bin/env python3
"""Updater boundaries: real staged bytes, bad archives, idle gating, and failed starts."""
from pathlib import Path
import io
import json
import os
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import zipfile

ROOT = Path(os.environ.get('AURA_TEST_PRODUCT') or Path(__file__).resolve().parents[1])
sys.path.insert(0, str(ROOT / 'scripts'))
import workspace_updates as updates


class Download(io.BytesIO):
    def geturl(self):
        return 'https://release-assets.githubusercontent.com/verified-fixture'


def product(root, ver):
    root.mkdir(parents=True)
    (root / 'VERSION').write_text(ver)
    (root / 'scripts').mkdir()
    (root / 'scripts/open_aura.py').write_text('fixture')
    interpreter = '.aura-runtime/python.exe' if os.name == 'nt' else '.aura-runtime/bin/python3'
    (root / interpreter).parent.mkdir(parents=True)
    (root / interpreter).write_bytes(b'not executable in this boundary fixture')
    updates.write(root / 'BUNDLED-RUNTIME.json', {'platform': updates.native_platform(), 'aura_version': ver,
                  'interpreter': interpreter, 'update_protocol': 1, 'workspace_schema_sha256': updates.schema_hash(root)})
    updates.write_integrity(root)
    return root.resolve()


def release(archive, ver='0.2.2'):
    name = 'viraltrac-aura-v' + ver + '-' + updates.native_platform() + ('.zip' if os.name == 'nt' else '.tar.gz')
    # A ZIP fixture works for either target; production uses the platform suffix.
    asset = {'name': name, 'digest': 'sha256:' + updates.sha(archive), 'size': archive.stat().st_size,
             'browser_download_url': updates.DOWNLOADS + 'v' + ver + '/' + name}
    return {'tag_name': 'v' + ver, 'body': '- A useful fix\n- Another improvement', 'prerelease': True,
            'assets': [asset], 'draft': False}


def reject(action, part=None):
    try:
        action()
        raise AssertionError('Unsafe operation was accepted')
    except (ValueError, tarfile.FilterError) as exc:
        if part:
            assert part in str(exc), str(exc)


with tempfile.TemporaryDirectory(prefix='AURA update boundary ') as directory:
    base = Path(directory)
    current = product(base / 'old app', '0.2.1')
    newer = product(base / 'new app', '0.2.2')
    archive = Path(shutil.make_archive(str(base / 'release'), 'zip', base, newer.name))
    raw = archive.read_bytes()
    published = release(archive)
    choice = updates.release_choice([published, dict(published, tag_name='v0.2.3-dev'), dict(published, tag_name='v9.0.0', draft=True)], '0.2.1', updates.native_platform())
    assert choice['version'] == '0.2.2' and choice['asset']
    assert updates.release_choice([published], '0.2.2', updates.native_platform()) is None
    assert not updates.release_choice([dict(published, assets=[])], '0.2.1', updates.native_platform())['asset']
    u = updates.Updater(current, base / 'state')
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda i: updates.Updater(current, base / 'state').save(**{'window-'+str(i):i}), range(8)))
    assert all(updates.read(u.path)['window-'+str(i)] == i for i in range(8))
    with patch.object(updates, 'fetch_json', return_value=[published]) as request:
        u.check()
        u.check()
        assert request.call_count == 1
    assert u.state()['unread'] and u.state()['can_install']
    u.action('read')
    assert not u.state()['unread'] and u.state()['notice']
    u.action('later')
    assert not u.state()['notice']
    u.save(later_until=0)
    u.action('skip')
    assert not u.state()['notice']
    u.save(release=dict(choice, version='0.2.3'))
    assert u.state()['notice'] and u.state()['unread']
    u.action('policy', 'manual')
    assert not u.state()['notice']
    with patch.object(updates, 'fetch_json') as request:
        u.check()
        request.assert_not_called()
    u.save(policy='notify', skipped=None, release=choice)
    # Preserve workspace bytes and local settings while preparing real archive contents.
    workspace = base / 'business'; workspace.mkdir()
    (workspace / 'important.txt').write_text('business truth')
    before = updates.sha(workspace / 'important.txt')
    with patch.object(updates, 'urlopen', side_effect=lambda *a, **k: Download(raw)), patch.object(updates.subprocess, 'run'):
        u.prepare()
    assert u.status == 'ready' and u.prepared.is_dir() and u.apply_when_idle
    assert updates.sha(workspace / 'important.txt') == before
    another = updates.Updater(current, base / 'state')
    reject(another.acquire_install, 'Another AURA window')
    u.action('later')
    assert not u.apply_when_idle
    another.acquire_install(); another.cancel_pending()
    # Corrupt bytes, edited defaults and incompatible schema never reach execution.
    bad = updates.Updater(current, base / 'bad'); bad.save(release=choice)
    tampered = dict(choice, asset=dict(choice['asset'], browser_download_url='https://github.com/other/repo/releases/download/payload'))
    bad.save(release=tampered)
    with patch.object(updates, 'urlopen') as download:
        bad.prepare(); download.assert_not_called()
    assert 'saved release details' in bad.message
    bad.save(release=choice)
    with patch.object(updates, 'urlopen', return_value=Download(b'x' * len(raw))), patch.object(updates.subprocess, 'run') as execute:
        bad.prepare(); execute.assert_not_called()
    assert bad.status == 'error' and 'verified' in bad.message and not bad.apply_when_idle
    (current / 'scripts/open_aura.py').write_text('user customization')
    with patch.object(updates, 'urlopen') as download:
        bad.prepare(); download.assert_not_called()
    assert 'customized' in bad.message
    (current / 'scripts/open_aura.py').write_text('fixture')
    (current / 'scripts/custom-work.py').write_text('preserve this addition')
    with patch.object(updates, 'urlopen') as download:
        bad.prepare(); download.assert_not_called()
    assert 'customized' in bad.message
    (current / 'scripts/custom-work.py').unlink()
    incompatible = json.loads((newer / 'BUNDLED-RUNTIME.json').read_text())
    incompatible['workspace_schema_sha256'] = 'different'
    updates.write(newer / 'BUNDLED-RUNTIME.json', incompatible); updates.write_integrity(newer)
    schema_archive = Path(shutil.make_archive(str(base / 'schema-change'), 'zip', base, newer.name))
    bad.save(release=updates.release_choice([release(schema_archive)], '0.2.1', updates.native_platform()))
    with patch.object(updates, 'urlopen', return_value=Download(schema_archive.read_bytes())), patch.object(updates.subprocess, 'run') as execute:
        bad.prepare(); execute.assert_not_called()
    assert 'workspace upgrade' in bad.message
    (current / '.git').mkdir()
    assert not bad.state()['can_install'] and 'Git' in bad.state()['manual_reason']
    (current / '.git').rmdir()
    # ZIP traversal and tar link escapes are rejected before any out-of-tree write.
    unsafe = base / 'unsafe.zip'
    with zipfile.ZipFile(unsafe, 'w') as bundle:
        bundle.writestr('../escaped.txt', 'unsafe')
    reject(lambda: updates.extract(unsafe, base / 'unsafe-output'))
    assert not (base / 'escaped.txt').exists()
    unsafe_tar = base / 'unsafe.tar.gz'
    with tarfile.open(unsafe_tar, 'w:gz') as bundle:
        link = tarfile.TarInfo('app/link'); link.type = tarfile.SYMTYPE; link.linkname = '../../outside'
        bundle.addfile(link)
    reject(lambda: updates.extract(unsafe_tar, base / 'tar-output'))
    # Exercise actual process start/readiness/rollback on a local port. No AI or workspace writes.
    serve = '''from http.server import HTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[1]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  body=(json.dumps({'product':str(root),'workspace':sys.argv[sys.argv.index('--workspace')+1],'version':(root/'VERSION').read_text()}) if self.path.startswith('/api/state') else '<meta name="aura-token" content="fixture-token">').encode()
  self.send_response(200);self.end_headers();self.wfile.write(body)
 def log_message(self,*args):pass
HTTPServer(('127.0.0.1',int(sys.argv[sys.argv.index('--port')+1])),Handler).serve_forever()
'''
    (current / 'scripts/open_aura.py').write_text(serve)
    (newer / 'scripts/open_aura.py').write_text(serve)
    launched = []
    original_popen = subprocess.Popen
    def spawn(*args, **kwargs):
        process = original_popen(*args, **kwargs); launched.append(process); return process
    def port():
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0)); return sock.getsockname()[1]
    hand = updates.Updater(current, base / 'handoff'); hand.store.mkdir()
    hand.prepared = newer.parent / 'new app' / '..' / 'new app'
    with patch.object(updates, 'bundled_python', return_value=Path(sys.executable)), patch('workspace_startup.status', return_value={'enabled': False}), patch.object(updates.subprocess, 'Popen', side_effect=spawn):
        try:
            updates.handoff(hand, workspace, '', port(), [])
            assert updates.read(hand.path)['active'] == str(newer)
            assert updates.read(hand.path)['skipped'] == '0.2.2'
            with patch.object(updates, 'state_dir', return_value=base / 'pointer'):
                updates.write(base / 'pointer/updates/settings.json', updates.read(hand.path))
                assert updates.launch_target(current) == newer
            for process in launched: process.terminate(); process.wait(timeout=10)
            launched.clear()
            (newer / 'scripts/open_aura.py').write_text('raise SystemExit(1)')
            hand = updates.Updater(current, base / 'failed-handoff'); hand.store.mkdir(); hand.prepared = newer
            updates.handoff(hand, workspace, '', port(), [])
            assert 'restored' in updates.read(hand.path)['error']
            assert not updates.read(hand.path).get('active')
            assert launched[-1].poll() is None
        finally:
            for process in launched:
                if process.poll() is None: process.terminate()
                process.wait(timeout=10)
    assert updates.sha(workspace / 'important.txt') == before
    # Authenticated HTTP actions remain local; a working chat is never interrupted by preparing an update.
    os.environ['BUSINESSOS_WORKSPACE'] = str(workspace)
    from http.server import ThreadingHTTPServer
    from workspace_ui import Workspace, handler_for
    app = Workspace(settings_file=base / 'http/preferences.json')
    app.job = {'status': 'working'}
    assert not app.update_idle()
    app.job = None; app.organization_job = {'status':'working'}
    assert not app.update_idle()
    app.organization_job = None; app.update_editing_until = time.time() + 8
    assert not app.update_idle()
    app.update_editing_until = 0
    assert app.update_idle()
    app.job = {'status':'working'}
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(app))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    address = 'http://127.0.0.1:' + str(server.server_port)
    try:
        request = Request(address + '/api/updates', data=b'{"action":"policy","policy":"manual"}', headers={'Content-Type': 'application/json', 'X-Aura-Token': app.token})
        with urlopen(request) as response: assert json.load(response)['policy'] == 'manual'
        assert app.job['status'] == 'working'
        try:
            urlopen(address + '/api/updates'); raise AssertionError('Updates must require the local token')
        except HTTPError as exc: assert exc.code == 403
    finally:
        server.shutdown(); server.server_close()
    u.cancel_pending()

print('AURA update checks, staged integrity, customization, archive safety, real handoff/fallback, workspace preservation and HTTP protections passed.')
