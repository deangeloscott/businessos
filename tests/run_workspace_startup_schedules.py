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
        # Native instruction edits preserve multiline text and require read-back
        # confirmation, without touching a user's actual scheduler.
        instructions = 'Review our saved goals.\nSummarize what needs attention.'
        native = dict(id='test-edit', owner='hermes', editable=True, native_id='job-1', profile='default', description='Old instructions')
        revised = dict(native, description=instructions)
        with patch.object(schedules, 'inventory', side_effect=[{'items':[native]}, {'items':[revised]}]), \
             patch.object(schedules.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as command:
            saved = schedules.update('test-edit', {'description':instructions}, ['hermes'], {})
            assert saved['description'] == instructions
            assert command.call_args.args[0] == ['hermes','cron','edit','job-1','--prompt',instructions]
        with patch.object(schedules, 'inventory', return_value={'items':[native]}), \
             patch.object(schedules.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
            try:
                schedules.update('test-edit', {'description':instructions}, ['hermes'], {})
                raise AssertionError('Unconfirmed task instruction edit was reported as saved')
            except ValueError as exc:
                assert 'could not be confirmed' in str(exc)
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
            # A separate task operation may run while a real chat is busy. It
            # must not select a connection, replace that job, or add a chat.
            from workspace_execution import Execution
            import workspace_ui as view
            jobs_path = hermes / 'cron/jobs.json'
            jobs_path.parent.mkdir(parents=True, exist_ok=True)
            jobs_path.write_text('{"jobs":[]}', encoding='utf-8')
            main_job = {'id':'main','business_id':bid,'status':'working'}
            app.job, app.execution = main_job, Execution()
            original_connection = dict(app.preferences['connection'])
            original_chats = list(app.preferences['chats'])
            original_active = dict(app.preferences['active_chats'])
            gate, started = threading.Event(), threading.Event()
            def post_task(data):
                req = Request(f'http://127.0.0.1:{server.server_port}/api/schedules/action',
                    data=json.dumps(dict(data,business=bid)).encode(),
                    headers={'Content-Type':'application/json','X-Aura-Token':app.token})
                with urlopen(req,timeout=5) as response:return json.load(response)
            def done():
                for _ in range(100):
                    if app.schedule_job['status']!='working':return app.schedule_state(bid)
                    time.sleep(.02)
                raise AssertionError('Task operation did not finish')
            def save_fake_task(name):
                jobs=json.loads(jobs_path.read_text())['jobs']
                native_id='task-'+str(len(jobs)+1)
                jobs.append({'id':native_id,'name':name,'prompt':'Check prices.',
                    'schedule':{'expr':'0 9 * * 1'},'model':'fixture','model_provider':'openai',
                    'reasoning_effort':'high','enabled':True})
                jobs_path.write_text(json.dumps({'jobs':jobs}),encoding='utf-8')
                return native_id
            def native_command(argv,env,execution=None,cwd=None):
                assert argv[:3]==['hermes','cron','create'] and '--workdir' in argv
                started.set();gate.wait(5);execution.check()
                save_fake_task(argv[argv.index('--name')+1]);return ''
            payload={'action':'create','app':'hermes','name':'Direct task','description':'Check prices.',
                     'when':'0 9 * * 1','model':'openai:fixture','effort':'high'}
            choice={'id':'hermes','name':'Hermes','argv':['hermes','chat']}
            with patch.object(view,'installed_agents',return_value=[choice]), \
                 patch.object(app,'agent_options',return_value={'models':[{'id':'openai:fixture'}]}), \
                 patch.object(app,'agent_efforts',return_value={'efforts':['high']}), \
                 patch.object(schedules,'invoke',side_effect=native_command), \
                 patch.object(view.workspace_agents,'run') as ai:
                job=post_task(payload)
                assert started.wait(2) and job['status']=='working'
                assert app.job is main_job and not app.execution.stopped.is_set()
                assert not app.update_idle(), 'An update could restart a task operation'
                gate.set();assert done()['status']=='complete'
                ai.assert_not_called()
                assert app.preferences['connection']==original_connection
                assert app.preferences['chats']==original_chats and app.preferences['active_chats']==original_active
                def isolated_agent(command,kind,root,env,prompt,native_id,model,effort,update,execution):
                    assert native_id is None and model=='openai:fixture' and effort=='high'
                    ident=save_fake_task('AI-assisted task')
                    return {'reply':json.dumps({'state':'saved','native_id':ident}),
                            'native_id':'setup-session','usage':{'input_tokens':11,'output_tokens':2}}
                ai.side_effect=isolated_agent
                post_task(dict(payload,name='AI-assisted task',when='Every Monday at 9am'))
                assert done()['status']=='complete'
                assert len(app.preferences['usage_receipts'])==1
                assert not any(k.startswith('schedule:') for k in app.preferences.get('usage_chats',{}))
                ai.return_value={'reply':'{"state":"saved","native_id":"does-not-exist"}',
                                 'native_id':'setup-session','usage':{}}
                ai.side_effect=None
                post_task(dict(payload,name='Unconfirmed task',when='Every Monday at 9am'))
                assert done()['status']=='error' and 'could not be confirmed' in app.schedule_job['message']
                ai.side_effect=ValueError('Traceback: invalid API_KEY credential 401')
                post_task(dict(payload,name='Failed task',when='Every Monday at 9am'))
                failure=done()
                assert failure['status']=='error' and 'Traceback' not in failure['message'] and 'API_KEY' not in failure['message']
                assert app.preferences['chats']==original_chats and app.preferences['active_chats']==original_active
                assert app.preferences['connection']==original_connection and app.job is main_job
                def question_agent(command,kind,root,env,prompt,native_id,model,effort,update,execution):
                    if native_id is None:
                        return {'reply':'{"state":"needs_input","message":"What time on Monday?"}',
                                'native_id':'task-question','usage':{}}
                    assert native_id=='task-question' and '9am' in prompt
                    ident=save_fake_task('Follow-up task')
                    return {'reply':json.dumps({'state':'saved','native_id':ident}),'native_id':native_id,'usage':{}}
                ai.side_effect=question_agent
                post_task(dict(payload,name='Follow-up task',when='Monday'))
                question=done();assert question['status']=='needs_input'
                post_task({'operation_id':question['id'],'request':'9am'})
                assert done()['status']=='complete'
                started.clear()
                def cancellable_agent(*args):
                    execution=args[-1];started.set()
                    assert execution.stopped.wait(5), 'Task setup stop did not reach its own execution'
                    execution.check()
                ai.side_effect=cancellable_agent
                stopping=post_task(dict(payload,name='Cancelled task',when='Monday'))
                assert started.wait(2)
                req=Request(f'http://127.0.0.1:{server.server_port}/api/schedules/stop',
                    data=json.dumps({'business':bid,'operation_id':stopping['id']}).encode(),
                    headers={'Content-Type':'application/json','X-Aura-Token':app.token})
                with urlopen(req,timeout=5) as response:assert response.status==200
                assert done()['status']=='stopped' and not app.execution.stopped.is_set()
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
            # Windows releases the final output handle just after the server
            # lock. Wait for that real condition before TemporaryDirectory exits.
            output_log=startup.state_dir()/'interface.log'
            for _ in range(50):
                try:
                    output_log.unlink(missing_ok=True)
                    break
                except PermissionError:
                    time.sleep(.1)
            else:
                raise AssertionError('Quit kept its output log open')
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
