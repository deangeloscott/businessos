"""Verify opt-in login launch and read-only discovery of real scheduler formats."""
from pathlib import Path
from http.server import ThreadingHTTPServer
import json
import os
import plistlib
import sys
import tempfile
import threading
import subprocess
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def main():
    import workspace_startup as startup
    import workspace_schedules as schedules
    from workspace_ui import Workspace, handler_for
    from setup import setup
    with tempfile.TemporaryDirectory(prefix='aura-startup-schedules-') as tmp, patch.dict(os.environ):
        base = Path(tmp)
        os.environ.update(LOCALAPPDATA=str(base / 'local'), APPDATA=str(base / 'roaming'),
                          XDG_CONFIG_HOME=str(base / 'config'), BUSINESSOS_WORKSPACE=str(base / 'Café workspace'),
                          BUSINESSOS_WORKSPACE_CONFIG=str(base / 'pointer.json'))
        workspace = Path(os.environ['BUSINESSOS_WORKSPACE'])
        bid = setup(organization='Schedule café')['business_id']
        codex, hermes, gemini = base / 'codex', base / 'hermes', base / 'gemini'
        os.environ['CODEX_HOME'], os.environ['HERMES_HOME'] = str(codex), str(hermes)
        # Merely opening/checking settings never installs a login item.
        with patch.object(Path, 'home', return_value=base):
            assert startup.status()['enabled'] is False
            assert not startup.registration().exists()
            assert startup.configure(True, ROOT, workspace, bid)['enabled']
            target = startup.registration()
            if sys.platform == 'win32':
                assert target.suffix == '.lnk' and target.stat().st_size > 0
            assert startup.configure(False, ROOT, workspace)['enabled'] is False
            assert not target.exists()
            # Generate the other desktop formats without touching system startup.
            for platform in ('darwin', 'linux'):
                with patch.object(sys, 'platform', platform):
                    assert startup.configure(True, ROOT, workspace, bid)['enabled']
                    target = startup.registration()
                    if platform == 'darwin':
                        argv = plistlib.loads(target.read_bytes())['ProgramArguments']
                        assert '--no-open' in argv and str(workspace) in argv
                    else:
                        assert 'Terminal=false' in target.read_text() and '--no-open' in target.read_text()
                    target.write_bytes(target.read_bytes() + b'\nchanged elsewhere\n')
                    try:
                        startup.configure(False, ROOT, workspace)
                        raise AssertionError('Modified startup entry was removed')
                    except ValueError:
                        pass
                    target.unlink()
                    startup.configure(False, ROOT, workspace)
        pi = workspace / '.pi/schedule-prompts.json'
        pi.parent.mkdir()
        pi.write_text(json.dumps({'version':1,'jobs':[{'id':'pi-1','name':'Weekly research',
            'enabled':True,'schedule':'0 0 9 * * 1','session':'original-session'}]}))
        sidecar = gemini / 'plugins/research/sidecars/daily/sidecar.json'
        sidecar.parent.mkdir(parents=True)
        sidecar.write_text(json.dumps({'builtin':'schedule','args':['0 9 * * *','agentapi','new-conversation','Research']}))
        (gemini / 'config.json').write_text(json.dumps({'sidecars':{'research/daily':{'enabled':True}}}))
        snapshot = {p:p.read_bytes() for p in (pi,sidecar,gemini / 'config.json')}
        result = schedules.inventory(codex,hermes,[workspace,workspace],gemini)
        assert len(result['items']) == 2 and not result['notes']
        assert all(not t['editable'] for t in result['items'])
        assert {t['owner'] for t in result['items']} == {'pi','antigravity'}
        assert next(t for t in result['items'] if t['owner']=='pi')['session'] == 'original-session'
        assert all(p.read_bytes() == data for p,data in snapshot.items()), 'Discovery modified native data'
        # An enabled configuration does not claim that its scheduler is alive.
        assert all(t['status']=='enabled' and t['runtime'].startswith('Requires') for t in result['items'])
        app = Workspace(settings_file=base / 'prefs.json')
        with patch.object(schedules, 'inventory', return_value=result):
            task = result['items'][0]
            prompt = app.request_text(bid,'Move this to Tuesday.',schedule_id=task['id'])
            assert 'original-session' in prompt and 'Move this to Tuesday.' in prompt
            try:
                app.request_text(bid,'Pause it.',schedule_id='removed-task')
                raise AssertionError('Stale schedule ID was accepted')
            except ValueError:
                pass
        # The normal launcher discovers the authenticated existing interface;
        # repeated launch does not create another server or run a model.
        server = ThreadingHTTPServer(('127.0.0.1',0), handler_for(app))
        worker = threading.Thread(target=server.serve_forever,daemon=True)
        worker.start()
        first, second = startup.VisualInstance(ROOT), startup.VisualInstance(ROOT)
        try:
            assert first.acquire()
            first.publish(server.server_port,app.token)
            assert not second.acquire()
            assert second.existing() == f'http://127.0.0.1:{server.server_port}/'
            app.job = {'status':'working'}
            req = Request(f'http://127.0.0.1:{server.server_port}/api/lifecycle',
                data=b'{"action":"quit"}',
                headers={'Content-Type':'application/json','X-Aura-Token':app.token})
            try:
                urlopen(req,timeout=3)
                raise AssertionError('Quit interrupted an active request')
            except HTTPError as exc:
                assert exc.code == 400 and worker.is_alive()
            finally:
                app.job = None
        finally:
            first.close();second.close();server.shutdown();server.server_close();worker.join()
        assert not first.path.exists()
        # Exercise the actual launcher/replacement process, with private state,
        # no browser and no AI request. Restart must release the old launch lock.
        process = subprocess.Popen([sys.executable, str(ROOT / 'scripts/open_aura.py'),
            '--workspace', str(workspace), '--business-id', bid, '--no-open'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            **({'creationflags':subprocess.CREATE_NO_WINDOW} if os.name == 'nt' else {}))
        def current_instance(previous=None):
            for _ in range(100):
                try:
                    record = json.loads(first.path.read_text(encoding='utf-8'))
                    if record['token'] != previous:
                        return record
                except (OSError, ValueError, KeyError):
                    pass
                time.sleep(.1)
            raise AssertionError('The launcher did not publish a ready replacement')
        def lifecycle(record, action):
            req = Request(f"http://127.0.0.1:{record['port']}/api/lifecycle",
                data=json.dumps({'action':action,'business':bid}).encode(),
                headers={'Content-Type':'application/json','X-Aura-Token':record['token']})
            with urlopen(req,timeout=5) as response:
                return json.load(response)
        running = None
        try:
            running = current_instance()
            assert lifecycle(running,'restart')['status'] == 'restart'
            assert process.wait(timeout=10) == 0
            replacement = current_instance(running['token'])
            assert replacement['port'] == running['port']
            running = replacement
            assert lifecycle(running,'quit')['status'] == 'quit'
            for _ in range(100):
                if not first.path.exists():
                    break
                time.sleep(.1)
            assert not first.path.exists(), 'Quit left the interface running'
        finally:
            if first.path.exists() and running:
                try:
                    lifecycle(current_instance(),'quit')
                except (OSError, ValueError, AssertionError):
                    pass
            if process.poll() is None:
                process.terminate(); process.wait(timeout=5)
        print('Workspace startup and schedule discovery checks passed.')


if __name__ == '__main__':
    main()
