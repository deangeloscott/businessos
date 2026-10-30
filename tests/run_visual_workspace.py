#!/usr/bin/env python3
"""Exercise real local HTTP edits, isolation, browser-origin protection and command handoff."""
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import re
import os
import shutil
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def main():
    prior = {key: os.environ.get(key) for key in ('BUSINESSOS_WORKSPACE', 'BUSINESSOS_WORKSPACE_CONFIG')}
    with tempfile.TemporaryDirectory(prefix='aura-view-test-') as tmp:
        base = Path(tmp)
        os.environ['BUSINESSOS_WORKSPACE'] = str(base / 'workspace')
        os.environ['BUSINESSOS_WORKSPACE_CONFIG'] = str(base / 'local-pointer.json')
        from workspace_ui import Workspace, handler_for
        from workspace_ui import setup_error, SETUP_ERRORS
        from init_business import init_business
        from _common import workspace_root
        app = Workspace(settings_file=base / 'view-preferences.json')
        for detail, category in [('HTTP 402 Payment required: insufficient credits','billing'),
                                 ('429 quota exhausted for model example','limit'),
                                 ('401 invalid API key','credentials'),
                                 ('OAuth refresh failed for openai: OpenAI OAuth token request failed (400): {"error":"invalid_grant"}','signin'),
                                 ('Permission denied for model example','model_access'),
                                 ('503 no available endpoints for model example','service'),
                                 ('Network timeout while loading model example','network'),
                                 ('model_not_found: example does not exist','model'),
                                 ("Permission denied: '/workspace/context.json'",'files'),
                                 ("Permission denied: '/workspace/model.json'",'files'),
                                 ("Permission denied for model 'example'",'model_access'),
                                 ('The app denied this request','permissions'),
                                 ('Profile permission denied','permissions'),
                                 ('The app returned an unfamiliar error','unknown')]:
            assert setup_error(detail)==SETUP_ERRORS[category], (detail,setup_error(detail))
        assert all(setup_error(message)==message for message in SETUP_ERRORS.values()), 'normalized setup errors must survive rendering unchanged'
        import workspace_codex, workspace_agents
        import workspace_chats
        brief_line='AURA_CHAT_BRIEF_0123456789abcdef '+json.dumps({'title':'Offer and landing page','summary':'Offer defined; next, refine the landing page.'})
        assert workspace_chats.clean('Useful reply.\n'+brief_line)=='Useful reply.'
        assert workspace_chats.clean('Useful reply.\nAURA_CHAT_BRIEF_0123',streaming=True)=='Useful reply.'
        assert workspace_chats.clean('Useful reply.\n  AURA_CHAT_BRIEF_0123')=='Useful reply.'
        assert workspace_chats.brief(brief_line)['summary'].startswith('Offer defined')
        assert workspace_chats.brief('AURA_CHAT_BRIEF_0123456789abcdef {broken') is None
        brief_chat={'brief_token':'0123456789abcdef','title':'Original'}
        brief_messages=[{'role':'user','text':'Define the offer'},{'role':'assistant','text':'Useful reply.'}]
        workspace_chats.update(brief_chat,brief_messages,workspace_chats.brief(brief_line))
        assert brief_chat['title']=='Offer and landing page' and not brief_chat['summary_stale']
        prior_brief=dict(brief_chat)
        changed=brief_messages+[{'role':'user','text':'Now change direction'},{'role':'assistant','text':'New plan.'}]
        old_candidate=dict(workspace_chats.brief(brief_line),basis=workspace_chats.fingerprint(brief_messages),at=brief_chat['summary_updated'])
        workspace_chats.update(brief_chat,changed,old_candidate)
        assert brief_chat['summary_stale'] and brief_chat['summary_updated']==prior_brief['summary_updated']
        brief_chat.update(title='My title',title_edited=True)
        workspace_chats.update(brief_chat,changed,workspace_chats.brief(brief_line))
        assert brief_chat['title']=='My title'
        workspace_chats.update(brief_chat,changed,old_candidate,'A newer native description.','',time.time()+1)
        assert brief_chat['summary']=='A newer native description.' and brief_chat['summary_source']=='App'
        import workspace_schedules
        from unittest.mock import patch
        # The combined schedule view is independent of the selected chat app.
        # Mutations go through a native command and are read back, never written
        # directly by the AURA adapter. This fixture cannot invoke a real job.
        codex_home, hermes_home = base / 'codex', base / 'hermes'
        automation = codex_home / 'automations' / 'daily'
        automation.mkdir(parents=True)
        (automation / 'automation.toml').write_text('id="daily"\nname="Daily review"\nstatus="ACTIVE"\nrrule="RRULE:FREQ=DAILY"\nmodel="example"\n', encoding='utf-8')
        cron = hermes_home / 'cron'
        cron.mkdir(parents=True)
        job_file = cron / 'jobs.json'
        job_file.write_text(json.dumps({'jobs':[{'id':'weekly','name':'Weekly research','enabled':True,
                            'schedule':{'expr':'0 9 * * 1'},'model':'example','model_provider':'openrouter',
                            'preserve_this':'original setting'}]}), encoding='utf-8')
        native = base / 'native-schedule-fixture.py'
        native.write_text('''import json,os,sys
from pathlib import Path
path=Path(os.environ['HERMES_HOME'])/'cron/jobs.json'
data=json.loads(path.read_text());job=data['jobs'][0]
assert sys.argv[1]=='cron' and sys.argv[3]==job['id']
action=sys.argv[2]
if action in {'pause','resume'}:job['enabled']=action=='resume'
else:
    for i in range(4,len(sys.argv),2):
        flag,value=sys.argv[i:i+2]
        field={'--name':'name','--model':'model','--provider':'model_provider','--reasoning-effort':'reasoning_effort'}.get(flag)
        if flag=='--schedule':job['schedule']={'expr':value}
        else:job[field]=value
path.write_text(json.dumps(data))
''', encoding='utf-8')
        with patch.object(workspace_schedules, 'roots', return_value=(codex_home, hermes_home)):
            native_tasks = workspace_schedules.inventory()['items']
            assert {t['owner'] for t in native_tasks} == {'hermes','codex'}
            task = next(t for t in native_tasks if t['owner']=='hermes')
            updated = workspace_schedules.update(task['id'],{'action':'edit','schedule':'0 10 * * 2','model':'new-model','provider':'openrouter'},[sys.executable,str(native)],dict(os.environ))
            assert updated['schedule']=='0 10 * * 2' and updated['model']=='new-model'
            assert workspace_schedules.update(task['id'],{'action':'pause'},[sys.executable,str(native)],dict(os.environ))['status']=='paused'
            assert workspace_schedules.update(task['id'],{'action':'resume'},[sys.executable,str(native)],dict(os.environ))['status']=='active'
            assert json.loads(job_file.read_text())['jobs'][0]['preserve_this']=='original setting'
            try:
                workspace_schedules.update(next(t['id'] for t in native_tasks if t['owner']=='codex'),{'action':'pause'},None,dict(os.environ))
                raise AssertionError('Unsupported native controls must not report success')
            except ValueError:
                pass
        # Both native event formats must retain a string error instead of
        # crashing the job or discarding the provider's cause.
        failure_program='import json,sys;sys.stdin.read();print(json.dumps({"type":"error","error":"429 quota exhausted"}));sys.exit(1)'
        for runner, command in [(lambda command:workspace_codex.run(command,base,'request',None,'model','low',lambda **values:None,dict(os.environ)),
                                 [sys.executable,'-c',failure_program,'exec','-']),
                                (lambda command:workspace_agents.run(command,'pi',base,dict(os.environ),'request',None,'model','low',lambda **values:None),
                                 [sys.executable,'-c',failure_program,'--print'])]:
            try:
                runner(command)
                raise AssertionError('A native error was incorrectly marked complete')
            except ValueError as exc:
                assert setup_error(str(exc))==SETUP_ERRORS['limit']
        # Stop both streaming transports, including a child holding stdout open.
        # Public text/tools are surfaced; private thinking events never are.
        from workspace_execution import Execution, Stopped
        for kind in ('pi', 'codex'):
            events, stopped = [], []
            active = threading.Event()
            control = Execution()
            program = '''import json,subprocess,sys,time
sys.stdin.read()
subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'])
events=[{'type':'session','id':'stopped-chat'}, {'type':'thread.started','thread_id':'stopped-chat'},
 {'type':'message_update','assistantMessageEvent':{'type':'thinking_delta','delta':'PRIVATE_THINKING'}},
 {'type':'message_update','assistantMessageEvent':{'type':'text_delta','delta':'Reading your files.'}},
 {'type':'tool_execution_start','toolName':'read'},
 {'type':'item.started','item':{'type':'command_execution'}}]
for event in events:print(json.dumps(event),flush=True)
time.sleep(30)
'''
            def update(**values):
                events.append(values)
                if values.get('progress') in {'Reading files and context', 'Running a command'}:
                    active.set()
            def run_stoppable():
                try:
                    command=[sys.executable,'-c',program,'--print' if kind=='pi' else 'exec']
                    if kind=='pi':workspace_agents.run(command,kind,base,dict(os.environ),'request',None,'model','low',update,control)
                    else:workspace_codex.run(command,base,'request',None,'model','low',update,dict(os.environ),control)
                except Stopped:stopped.append(True)
            worker=threading.Thread(target=run_stoppable,daemon=True)
            worker.start()
            assert active.wait(5), events
            control.stop();worker.join(5)
            assert not worker.is_alive() and stopped, 'Stop must end this request and its child process'
            assert 'PRIVATE_THINKING' not in json.dumps(events)
            assert any(e.get('native_id')=='stopped-chat' for e in events)
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(app))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        url = f'http://127.0.0.1:{server.server_port}'

        def call(path, data=None, token=True, origin=None, expect=200):
            headers = {'X-Aura-Token': app.token} if token else {}
            if origin:
                headers['Origin'] = origin
            if data is not None:
                headers['Content-Type'] = 'application/json'
            request = Request(url + path, data=json.dumps(data).encode() if data is not None else None, headers=headers)
            try:
                with urlopen(request, timeout=30) as response:
                    assert response.status == expect, (path, response.status)
                    body = response.read()
                    return json.loads(body) if response.headers.get_content_type() == 'application/json' else body.decode()
            except HTTPError as exc:
                assert exc.code == expect, (path, exc.code, exc.read().decode())
                return json.loads(exc.read())
        try:
            assert '__AURA_TOKEN__' not in call('/')
            call('/api/state', token=False, expect=403)
            call('/api/setup', {'name': 'Intruder'}, origin='https://another-site.example', expect=403)
            assert not (workspace_root() / 'instances' / 'intruder').exists()
            assert call('/api/state')['appearance'] == 'system'
            call('/api/preferences', {'appearance': 'dark'})
            assert call('/api/state')['appearance'] == 'dark'
            call('/api/preferences', {'appearance': 'invisible'}, expect=400)
            created = call('/api/setup', {'name': 'Visual example'})
            bid = created['business_id']
            assert call('/api/state?business=' + bid)['onboarding'] == {'seen': False}
            assert created['status'] == 'ready'
            assert call('/api/setup', {'name': 'Visual example'})['business_id'] == bid
            init_business('other-business', 'Other business')
            call('/api/save', {'business': bid, 'kind': 'business', 'name': 'Renamed example'})
            goal = call('/api/save', {'business': bid, 'kind': 'goal', 'name': 'Create a useful page'})
            ref = goal['objects'][0]['id']
            call('/api/save', {'business': bid, 'kind': 'goal', 'ref': ref, 'name': 'Create and inspect a useful page'})
            snapshot = call('/api/state?business=' + bid)
            assert any(r['title'] == 'Renamed example' for r in snapshot['records'])
            assert any(r['ref'] == ref and r['data']['name'] == 'Create and inspect a useful page' for r in snapshot['records'])
            assert not any(r['ref'] == ref for r in call('/api/state?business=other-business')['records'])
            call('/api/save', {'business': 'other-business', 'kind': 'goal', 'ref': ref, 'name': 'Overwrite'}, expect=400)

            note = workspace_root() / 'attachments' / bid / 'hello.txt'
            note.parent.mkdir(parents=True)
            note.write_text('An actual saved file.', encoding='utf-8')
            refs = call('/api/files?business=' + bid)['items']
            assert any(f['path'] == f'attachments/{bid}/hello.txt' for f in refs)
            assert call(f'/api/file?business={bid}&path=attachments/{bid}/hello.txt')['text'] == 'An actual saved file.'
            call(f'/api/file?business={bid}&path=instances/other-business/context/business.json', expect=400)
            call(f'/api/file?business={bid}&path=../local-pointer.json', expect=400)
            call(f'/api/file?business={bid}&path=.businessos/workspace.json', expect=400)
            # Explicit links expose only the selected business's chosen files;
            # linking and unlinking must never copy, edit or delete originals.
            linked_folder = base / 'Brand files'
            linked_folder.mkdir()
            (linked_folder / 'advert.txt').write_text('Original brand material.', encoding='utf-8')
            (linked_folder / '.env').write_text('PRIVATE_FIXTURE', encoding='utf-8')
            call('/api/locations', {'business':bid, 'path':str(linked_folder), 'name':'Brand ads'})
            linked = call('/api/files?business=' + bid)
            advert = next(f for f in linked['items'] if f['name'] == 'advert.txt')
            assert advert['local_path'] == str(linked_folder / 'advert.txt') and advert['location_name'] == 'Brand ads'
            assert not any(f['name'] == '.env' for f in linked['items'])
            assert call(f'/api/file?business={bid}&path='+advert['path'])['text'] == 'Original brand material.'
            call(f'/api/file?business=other-business&path='+advert['path'], expect=400)
            call(f'/api/file?business={bid}&path=linked/{advert["location"]}/../outside.txt', expect=400)
            call('/api/locations', {'business':bid,'path':str(linked_folder / '.env')}, expect=400)
            call('/api/locations', {'business':bid,'path':''}, expect=400)
            call('/api/locations', {'business':bid,'path':str(workspace_root() / 'instances' / 'other-business')}, expect=400)
            assert 'Brand ads' in app.request_text(bid, 'Use my brand files')
            assert 'Brand ads' not in app.request_text('other-business', 'Use my brand files')
            assert Workspace(settings_file=app.settings_file).preferences['file_locations'][bid]
            call('/api/locations', {'business':bid,'remove':advert['location']})
            call(f'/api/file?business={bid}&path='+advert['path'], expect=400)
            assert (linked_folder / 'advert.txt').read_text(encoding='utf-8') == 'Original brand material.'
            catalog = call('/api/library')
            assert all(r['category'] and r['group'] and r['key'] and r['kind'] in {'Workflow','Recipe','Skill','Tool','Plugin'} for r in catalog)
            assert any(r.get('subtype')=='Playbook' for r in catalog)
            assert any(r['kind']=='Workflow' and r['category']=='Research' and r['group']=='Competitors' for r in catalog)
            assert any(r['kind']=='Recipe' and r['category']=='E-commerce' for r in catalog)
            assert any(r['kind'] == 'Workflow' for r in catalog) and any(r['kind'] == 'Recipe' for r in catalog)
            assert call('/api/document?path=' + catalog[0]['path'])['text']
            assert Path(call('/api/library/item?key='+catalog[0]['key'])['location'])==ROOT/catalog[0]['path']
            call('/api/document?path=scripts/workspace_ui.py', expect=400)
            skill=next(r for r in catalog if r['kind']=='Skill' and any(s['status']=='Included with AURA' for s in r['sources']))
            assert call('/api/library/item?key='+skill['key'])['text']
            call('/api/library/item?key='+skill['key']+'&option=not-an-installed-option',expect=400)
            guide=next(r for r in catalog if r.get('subtype')=='Playbook')
            assert guide['description'] in call('/api/library/item?key='+guide['key'])['text']
            call('/api/library/item?key=../../secrets',expect=400)
            cached_choice={'id':'codex','name':'Codex','argv':['fixture-only']}
            cached_tool=__import__('workspace_library').entry('Tool','Retained tool','A previously reported capability.','codex','retained-tool','Reported by app',type='Tool')
            app.library_native={'codex':([cached_tool],'')};app.library_checked=0
            with patch('workspace_ui.installed_agents',return_value=[cached_choice]), patch('workspace_library.native',side_effect=ValueError('Fixture refresh failure')):
                failed_catalog=app.library_items(discover=True)
            kept=next(r for r in failed_catalog['items'] if r['title']=='Retained tool')
            assert all(s.get('stale') for s in kept['sources']) and failed_catalog['notes']
            app.library_checked=0
            with patch('workspace_ui.installed_agents',return_value=[cached_choice]), patch('workspace_library.native',return_value=[]):
                recovered_catalog=app.library_items(discover=True)
            assert not any(r['title']=='Retained tool' for r in recovered_catalog['items'])
            prefs={'favorites':[skill['key'],'plugin:portable-choice'],'recent':[catalog[0]['key']]}
            call('/api/preferences',{'business':bid,'library':prefs})
            assert app.state(bid)['library_preferences']==prefs
            assert not app.state('other-business')['library_preferences']['favorites']
            assert Workspace(settings_file=app.settings_file).state(bid)['library_preferences']==prefs

            # A real subprocess round trip. The test command is not an AI; this
            # verifies transport and scoping, never model/business capability.
            app.configured_agent = {'name': 'Transport test command', 'argv': [sys.executable, '-c', 'import sys; print(sys.stdin.read())']}
            connected = call('/api/connect', {'kind': 'configured'})
            assert connected['mode'] == 'agent' and connected['selected'] == 'configured'
            assert connected['workspace_write'], 'new UI connections opt into workspace editing'
            assert {'id': 'configured', 'name': 'Transport test command', 'available': True} in connected['choices']
            assert not connected['verified'], 'configuration must not claim verified access'
            manual = call('/api/connect', {'kind': 'handoff'})
            assert not manual['connected'] and manual['mode'] == 'copy'
            assert Workspace(settings_file=app.settings_file).connection()['mode'] == 'copy'
            assert call('/api/connect', {'kind': 'configured'})['connected']
            # Setup/status checks never enter either model execution path or
            # create a welcome/chat. Only explicitly connected apps are listed.
            with patch.object(workspace_agents,'run',side_effect=AssertionError('No model request allowed')), patch.object(workspace_codex,'run',side_effect=AssertionError('No model request allowed')):
                before_chats = list(app.preferences['chats'])
                for _ in range(2):
                    checked = call('/api/connection-check?business=' + bid)
                    assert checked['ready'] and checked['files_ready']
                    assert [c['id'] for c in checked['items']] == ['configured']
                assert app.job is None and app.preferences['chats'] == before_chats
                app.preferences['connected_apps']['pi'] = {'kind':'pi','model':'openai/example'}
                app.preferences['connected_apps']['codex'] = {'kind':'codex','model':'example'}
                choices = [{'id':'pi','name':'Pi','argv':[sys.executable,'--print']},
                           {'id':'codex','name':'Codex','argv':None}]
                import workspace_ui as check_view
                with patch.object(check_view,'installed_agents',return_value=choices), patch.object(app,'agent_options',return_value={'models':[{'id':'openai/example'}]}), patch.object(workspace_agents,'check_signin',return_value=None):
                    checked = call('/api/connection-check?business=' + bid)
                    statuses = {r['id']:r['status'] for r in checked['items']}
                    assert statuses['pi']=='ready' and statuses['codex']=='error'
                    assert 'hermes' not in statuses and checked['ready'], 'one app failure must not mark another app disconnected'
                del app.preferences['connected_apps']['pi'], app.preferences['connected_apps']['codex']
                app.save_preferences()
            raw = 'A literal request: $(do-not-execute) & <script>not markup</script>'
            job = call('/api/chat', {'business': bid, 'text': raw}, expect=202)
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                result = call(f'/api/chat?business={bid}&id={job["id"]}')
                if result['status'] != 'working':
                    break
                time.sleep(.05)
            assert result['status'] == 'complete' and raw in result['reply'] and f'business ID: {bid}' in result['reply']
            inbox = call('/api/notifications?business=' + bid)
            assert inbox['unread'] == 1 and inbox['items'][0]['id'] == job['id']
            assert raw not in json.dumps(inbox), 'notifications must not store reply/request contents'
            assert call('/api/notifications?business=other-business')['unread'] == 0
            assert Workspace(settings_file=app.settings_file).notifications(bid)['unread'] == 1
            call('/api/notifications', {'business': 'other-business', 'action': 'read', 'id': job['id']})
            assert call('/api/notifications?business=' + bid)['unread'] == 1
            call('/api/preferences', {'notifications': True})
            assert not call('/api/notifications', {'business': bid, 'action': 'claim'})['claimed'], 'do not replay old activity when enabling alerts'
            with app.lock:
                receipt = {'id':'notification-check', 'business_id':bid, 'status':'error', 'updated':time.time()}
                app.record_notification(receipt, None)
                app.record_notification(receipt, None)
            assert call('/api/notifications?business=' + bid)['unread'] == 2, 'completion must be deduplicated'
            call('/api/notifications?business=' + bid + '&foreground=1')
            assert not call('/api/notifications', {'business':bid, 'action':'claim'})['claimed'], 'no system alert while another tab is active'
            app.notification_focus_until = 0
            claim = call('/api/notifications', {'business':bid, 'action':'claim'})
            assert len(claim['claimed']) == 1
            assert not call('/api/notifications', {'business':bid, 'action':'claim'})['claimed'], 'only one tab can deliver an alert'
            with app.lock:
                app.record_notification({**receipt, 'id':'next-notification'}, None)
            assert not call('/api/notifications', {'business':bid, 'action':'claim'})['claimed'], 'close arrivals wait for the batching cooldown'
            app.preferences['notification_sent_at'] = time.time() - 31
            assert len(call('/api/notifications', {'business':bid, 'action':'claim'})['claimed']) == 1
            read = call('/api/notifications', {'business':bid, 'action':'read', 'id':job['id']})
            assert read['unread'] == 2
            assert call('/api/notifications', {'business':bid, 'action':'read', 'all':True})['unread'] == 0
            assert Workspace(settings_file=app.settings_file).notifications(bid)['unread'] == 0
            assert call('/api/state?business=' + bid)['records'] == snapshot['records'], 'chat must not be copied into memory'
            call(f'/api/chat?business=other-business&id={job["id"]}', expect=400)
            app.agent = {'name':'Stop fixture', 'argv':[sys.executable,'-c','import sys,time;sys.stdin.read();time.sleep(30)']}
            stopped_job=call('/api/chat',{'business':bid,'text':'Wait for my correction'},expect=202)
            call('/api/chat/stop',{'business':'other-business','id':stopped_job['id']},expect=400)
            call('/api/chat/stop',{'business':bid,'id':'stale-request'},expect=400)
            assert call(f'/api/chat?business={bid}&id={stopped_job["id"]}')['status']=='working'
            call('/api/chat/stop',{'business':bid,'id':stopped_job['id']})
            for _ in range(100):
                result=call(f'/api/chat?business={bid}&id={stopped_job["id"]}')
                if result['status']!='working':break
                time.sleep(.05)
            assert result['status']=='stopped', result
            assert not any(n['id']==stopped_job['id'] for n in call('/api/notifications?business='+bid)['items'])
            app.agent = {'name': 'Failing transport', 'argv': [sys.executable, '-c', 'raise SystemExit(3)']}
            job = call('/api/chat', {'business': bid, 'text': 'Check failure status'}, expect=202)
            for _ in range(100):
                result = call(f'/api/chat?business={bid}&id={job["id"]}')
                if result['status'] != 'working':
                    break
                time.sleep(.05)
            assert result['status'] == 'error' and 'not marked complete' in result['reply']

            # Welcome success requires actual reads of both selected files, not
            # merely an echoed prompt or a reassuring model-generated message.
            app.agent = {'name': 'Echo only', 'argv': [sys.executable, '-c', 'import sys; print(sys.stdin.read())']}
            job = call('/api/chat', {'business': bid, 'welcome': True}, expect=202)
            for _ in range(100):
                result = call(f'/api/chat?business={bid}&id={job["id"]}')
                if result['status'] != 'working':
                    break
                time.sleep(.05)
            assert result['status'] == 'error' and not result['setup']['aura_guidance']
            assert result['reply']==SETUP_ERRORS['proof'] and result['setup_error']
            assert 'AURA_SETUP' not in result['reply'] and not re.search(r'[0-9a-f]{64}', result['reply'])
            assert not call('/api/state?business=' + bid)['onboarding']['seen']
            # Failed commands must preserve their cause instead of becoming a
            # claim that the AI cannot read the workspace.
            for detail, category, exit_code in [('402 insufficient credits','billing',2),
                                                ('permission denied for model example','model_access',2)]:
                app.agent={'name':'Setup failure fixture','argv':[sys.executable,'-c',
                           'import sys; sys.stdin.read(); print('+repr(detail)+', file=sys.stderr if '+str(exit_code)+' else sys.stdout); sys.exit('+str(exit_code)+')']}
                job=call('/api/chat',{'business':bid,'welcome':True},expect=202)
                for _ in range(100):
                    result=call(f'/api/chat?business={bid}&id={job["id"]}')
                    if result['status']!='working':break
                    time.sleep(.05)
                assert result['status']=='error' and result['reply']==SETUP_ERRORS[category], result
                assert result['setup_error'] and not call('/api/state?business='+bid)['onboarding']['seen']
            reader = base / 'file-reader.py'
            reader.write_text('''import hashlib, re, sys
from pathlib import Path
text = sys.stdin.read()
paths = [re.search(label + r": ([^\\n]+)", text).group(1) for label in ("Skill file", "Business file")]
hashes = [hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths]
nonce = re.search(r"AURA_SETUP ([0-9a-f]{16})", text).group(1)
print("Welcome. The selected business files are readable.")
print("AURA_SETUP", nonce, *hashes)
''', encoding='utf-8')
            app.agent = {'name': 'File-reading test command', 'argv': [sys.executable, str(reader)]}
            job = call('/api/chat', {'business': bid, 'welcome': True}, expect=202)
            for _ in range(100):
                result = call(f'/api/chat?business={bid}&id={job["id"]}')
                if result['status'] != 'working':
                    break
                time.sleep(.05)
            assert result['status'] == 'complete' and all(result['setup'].values())
            assert 'AURA_SETUP' not in result['reply']
            state = call('/api/state?business=' + bid)
            assert state['connection']['verified'] and state['onboarding']['seen']
            assert not call('/api/state?business=other-business')['connection']['verified']
            assert call('/api/state?business=' + bid)['records'] == snapshot['records']
            restored = Workspace(settings_file=app.settings_file)
            assert restored.preferences['appearance'] == 'dark' and bid in restored.preferences['seen']
            assert 'argv' not in app.settings_file.read_text() and 'Welcome.' not in app.settings_file.read_text()
            call('/api/preferences', {'business': 'other-business', 'dismiss_setup': True})
            assert call('/api/state?business=other-business')['onboarding']['seen']

            # Native protocol fixture: exercise session IDs, real transcript
            # readback and HTTP restore without paying for model inference.
            # The separate live browser check uses actual Codex.
            import workspace_ui as view
            fixture = base / 'native-host.py'
            fixture.write_text('''import hashlib, json, re, sys
from pathlib import Path
log = Path(__file__).with_suffix('.jsonl')
def emit(value): print(json.dumps(value), flush=True)
if 'app-server' in sys.argv:
    for line in sys.stdin:
        req = json.loads(line)
        if 'id' not in req: continue
        method = req['method']
        result = {}
        if method == 'thread/read': result = {'thread': {'id': 'native-one', 'path': str(log), 'status': {'type':'idle'}}}
        if method == 'skills/list': result = {'data':[{'skills':[{'name':'viraltrac-aura','enabled':True,'path':str(Path.cwd()/'.agents/skills/viraltrac-aura/SKILL.md')}]}]}
        emit({'id':req['id'],'result':result})
else:
    text = sys.stdin.read()
    count = len(log.read_text().splitlines())//3 + 1 if log.exists() else 1
    reply = 'Native turn %d; resumed=%s' % (count, 'resume' in sys.argv)
    if 'Welcome me to my AURA workspace' in text:
        paths = [re.search(label+r': ([^\\n]+)', text).group(1) for label in ('Skill file','Business file')]
        nonce = re.search(r'AURA_SETUP ([0-9a-f]{16})', text).group(1)
        reply += '\\nAURA_SETUP '+nonce+' '+' '.join(hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths)
    brief = re.search(r'AURA_CHAT_BRIEF_([0-9a-f]{16})',text)
    if brief:
        description = 'Offer defined; next, draft the landing page.' if count==1 else 'Landing-page draft ready; next, choose the headline.'
        reply += '\\nAURA_CHAT_BRIEF_'+brief.group(1)+' '+json.dumps({'title':'Offer and landing page','summary':description})
    rows = [{'type':'turn_context','payload':{'model':'fixture-model','effort':'low'}},
            {'type':'response_item','payload':{'type':'message','role':'user','content':[{'type':'input_text','text':text.replace('\\n','\\r\\n')}]}},
            {'type':'response_item','payload':{'type':'message','role':'assistant','phase':'final_answer','content':[{'type':'output_text','text':reply}]}}]
    with log.open('a', encoding='utf-8') as stream:
        for row in rows: stream.write(json.dumps(row)+'\\n')
    emit({'type':'thread.started','thread_id':'native-one'})
    emit({'type':'item.completed','item':{'type':'agent_message','text':reply}})
    emit({'type':'turn.completed','usage':{'input_tokens':100,'output_tokens':20}})
''', encoding='utf-8')
            original_command, original_agents = view.codex_command, view.installed_agents
            command = [sys.executable, str(fixture), 'exec', '-']
            view.codex_command = lambda: command
            view.installed_agents = lambda: [{'id':'codex','name':'Codex fixture','argv':command}]
            app.option_cache['codex'] = {'models':[{'id':'fixture-model','name':'Fixture model','efforts':['low'],'default_effort':'low'}],
                                         'model':'fixture-model','effort':'low','sessions':True}
            try:
                instructions = workspace_root() / 'AGENTS.md'
                instructions.write_text('Keep this user-authored instruction.\n', encoding='utf-8')
                previous_kind = app.connection_kind
                call('/api/connect', {'kind':'codex','model':'unknown','effort':'low'}, expect=400)
                assert app.connection_kind == previous_kind and 'AURA workspace attachment' not in instructions.read_text()
                call('/api/connect', {'kind':'codex','model':'fixture-model','effort':'low'})
                assert instructions.read_text().startswith('Keep this user-authored instruction.')
                assert call('/api/state?business='+bid)['connection']['attachment']['discovered']
                for index in (1, 2):
                    job = call('/api/chat', {'business':bid, 'text':'Continue with native history'}, expect=202)
                    for _ in range(100):
                        result = call(f'/api/chat?business={bid}&id={job["id"]}')
                        if result['status'] != 'working': break
                        time.sleep(.05)
                    assert result['status'] == 'complete', result
                    assert result['native_id'] == 'native-one'
                    assert f'Native turn {index}' in result['reply']
                    assert 'AURA_CHAT_BRIEF_' not in result['reply']
                    saved_chat=call('/api/chats?business='+bid)['items'][0]
                    assert saved_chat['summary']==('Offer defined; next, draft the landing page.' if index==1 else 'Landing-page draft ready; next, choose the headline.')
                    if index==1:
                        call('/api/chats/rename',{'business':'other-business','id':saved_chat['id'],'title':'Wrong business'},expect=400)
                        call('/api/chats/rename',{'business':bid,'id':saved_chat['id'],'title':''},expect=400)
                        call('/api/chats/rename',{'business':bid,'id':saved_chat['id'],'title':'My launch work'})
                    else:assert saved_chat['title']=='My launch work', 'AI updates must preserve the chosen title'
                assert 'resumed=True' in result['reply'] and result['usage']['output_tokens'] == 20
                chats = call('/api/chats?business='+bid)['items']
                assert len(chats) == 1 and not call('/api/chats?business=other-business')['items']
                call('/api/chats/open', {'business':'other-business','id':chats[0]['id']}, expect=400)
                conversation = call('/api/conversation?business='+bid)
                assert len(conversation['messages']) == 4
                assert conversation['messages'][0]['text'] == 'Continue with native history'
                assert 'AURA_CHAT_BRIEF_' not in json.dumps(conversation['messages'])
                restarted = Workspace(settings_file=app.settings_file)
                assert len(restarted.conversation(bid)['messages']) == 4
                assert 'Native turn 2' not in app.settings_file.read_text(), 'transcripts stay in the native harness'
                before = fixture.with_suffix('.jsonl').read_bytes()
                call('/api/chats/new', {'business':bid})
                assert call('/api/conversation?business='+bid)['messages'] == []
                assert fixture.with_suffix('.jsonl').read_bytes() == before, 'New chat must not submit or rerun work'
                summary_read=call('/api/chats/detail?business='+bid+'&id='+chats[0]['id'])
                assert summary_read['chat']['summary'].startswith('Landing-page draft ready')
                assert app.active_chat(bid) is None and fixture.with_suffix('.jsonl').read_bytes()==before, 'Refreshing details must not switch chats or submit a prompt'
                call('/api/chats/detail?business=other-business&id='+chats[0]['id'],expect=400)
                alternate=dict(chats[0],id='later-chat',updated=chats[0]['updated']+1)
                app.preferences['chats'].append(alternate)
                assert call('/api/chats?business='+bid)['items'][0]['id']=='later-chat'
                app.preferences['chats'].remove(alternate)
                call('/api/chats/open', {'business':bid,'id':chats[0]['id']})
                assert call('/api/state?business='+bid)['records'] == snapshot['records']
            finally:
                view.codex_command, view.installed_agents = original_command, original_agents
            # Keys never cross read APIs or portable state; native metadata never
            # submits a prompt. This fixture reports protocol/argv, not AI work.
            secret = 'aura-fixture-key-never-use-with-a-provider'
            call('/api/connections', token=False, expect=403)
            call('/api/connections/save', {'provider':'fal','key':secret}, token=False, expect=403)
            call('/api/connections/save', {'provider':'fal','key':secret}, origin='https://another-site.example', expect=403)
            call('/api/connections/save', {'provider':'other','name':'Unsafe','env':'PYTHONPATH','key':secret}, expect=400)
            call('/api/connections/save', {'provider':'fal','key':secret,'storage':'session'})
            listing = call('/api/connections')
            assert secret not in json.dumps(listing) and secret not in app.settings_file.read_text()
            assert app.connections.environment()['FAL_KEY'] == secret
            assert secret not in call('/api/request', {'business':bid,'text':'Use useful APIs'})['text']
            assert 'fal.ai via FAL_KEY' in call('/api/request', {'business':bid,'text':'Use useful APIs'})['text']
            if os.name == 'nt':
                call('/api/connections/save', {'provider':'fal','key':secret,'storage':'computer'})
                assert secret.encode() not in app.connections.path.read_bytes()
                assert Workspace(settings_file=app.settings_file).connections.environment()['FAL_KEY'] == secret
            fixture2 = base / 'metadata-fixture.py'
            fixture2.write_text('''import json, sys, os, hashlib, re
from pathlib import Path
kind=sys.argv[1]; ident='native-'+kind
log=Path(__file__).with_suffix('.'+kind+'.json')
def emit(v): print(json.dumps(v),flush=True)
def history():return json.loads(log.read_text()) if log.exists() else []
if 'models' in sys.argv:
 print('gemini-fixture\\tGemini fixture')
elif 'sessions' in sys.argv:
 emit({'id':ident,'messages':history()})
elif 'rpc' in sys.argv or 'acp' in sys.argv or '--no-session-persistence' in sys.argv:
 for line in sys.stdin:
  req=json.loads(line)
  with Path(__file__).with_suffix('.requests').open('a') as f:f.write(json.dumps(req)+'\\n')
  if 'method' in req:
   data={} if req['method']=='initialize' else {'models':{'currentModelId':'fixture:model','availableModels':[{'modelId':'fixture:model','name':'Fixture'}]}}
   emit({'jsonrpc':'2.0','id':req['id'],'result':data});continue
  if 'request_id' in req:
   emit({'type':'control_response','response':{'request_id':req['request_id'],'subtype':'success','response':{'models':[{'value':'claude-fixture','displayName':'Claude fixture','supportedEffortLevels':['low','high']}]}}});continue
  data={}
  if req['type']=='get_available_models':data={'models':[{'provider':'fixture','id':'model','name':'Fixture'}]}
  if req['type']=='get_state':data={'sessionId':ident,'model':{'provider':'fixture','id':'model'},'thinkingLevel':'high'}
  if req['type']=='get_available_thinking_levels':data={'levels':['off','high']}
  if req['type']=='get_messages':data={'messages':history()}
  emit({'id':req['id'],'type':'response','success':True,'data':data})
else:
 text=sys.stdin.read()
 if kind=='antigravity':text=json.loads(text)['message']['content']
 payload={'key_available':os.environ.get('FAL_KEY')=='aura-fixture-key-never-use-with-a-provider','argv':sys.argv[2:]}
 reply=json.dumps(payload)
 if 'Welcome me to my AURA workspace' in text:
  paths=[re.search(label+r': ([^\\n]+)',text).group(1) for label in ('Skill file','Business file')]
  nonce=re.search(r'AURA_SETUP ([0-9a-f]{16})',text).group(1)
  reply+='\\nAURA_SETUP '+nonce+' '+' '.join(hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths)
 brief=re.search(r'AURA_CHAT_BRIEF_([0-9a-f]{16})',text)
 if brief:reply+='\\nAURA_CHAT_BRIEF_'+brief.group(1)+' '+json.dumps({'title':'Selected settings','summary':'Reviewed the selected model settings; ready for the next request.'})
 messages=history()+[{'role':'user','content':text},{'role':'assistant','content':[{'type':'text','text':reply}]}]
 log.write_text(json.dumps(messages))
 if kind in ('pi','omp'):
  emit({'type':'session','id':ident});emit({'type':'message_end','message':messages[-1]})
 elif kind=='antigravity':
  emit({'event':'init','conversation_id':ident});emit({'event':'result','result':{'conversation_id':ident,'status':'SUCCESS','response':reply}})
 elif kind=='hermes':
  emit({'type':'system','subtype':'init','session_id':ident});emit({'type':'result','session_id':ident,'text':reply,'exit_code':0})
 else:
  emit({'type':'system','subtype':'init','session_id':ident});emit({'type':'result','session_id':ident,'result':reply})
''', encoding='utf-8')
            original_agents = view.installed_agents
            kinds=('pi','omp','claude','hermes','antigravity')
            view.installed_agents = lambda: [{'id':kind,'name':kind,'argv':[sys.executable,str(fixture2),kind,*(['chat','--query-file','-'] if kind=='hermes' else ['--print'])]} for kind in kinds]
            try:
                for kind in kinds:
                    opts = call('/api/agent-options?kind='+kind+'&refresh=1')
                    model = opts['models'][0]['id']
                    efforts = call('/api/agent-efforts?kind='+kind+'&model='+model)
                    effort='high' if 'high' in efforts['efforts'] else ''
                    call('/api/connect', {'kind':kind,'model':model,'effort':'invented'}, expect=400)
                    call('/api/connect', {'kind':kind,'model':model,'effort':effort})
                    for turn in (1,2):
                        job=call('/api/chat', {'business':bid,'text':'Check selected settings, turn '+str(turn)}, expect=202)
                        for _ in range(100):
                            result=call(f'/api/chat?business={bid}&id={job["id"]}')
                            if result['status']!='working':break
                            time.sleep(.05)
                        assert result['status']=='complete', result
                        assert result['native_id']=='native-'+kind
                        payload=json.loads(result['reply'])
                        assert payload['key_available'] and '--model' in payload['argv'] and model in payload['argv']
                        if turn==2:
                            flag={'pi':'--session','omp':'--resume','claude':'--resume','hermes':'--resume','antigravity':'--conversation'}[kind]
                            assert flag in payload['argv'] and 'native-'+kind in payload['argv']
                    restored=Workspace(settings_file=app.settings_file).conversation(bid)
                    assert len(restored['messages'])==4, restored
                    assert restored['messages'][0]['text']=='Check selected settings, turn 1'
                    assert restored['chat']['summary'].startswith('Reviewed the selected model settings')
                    assert 'AURA_CHAT_BRIEF_' not in json.dumps(restored['messages'])
                    job=call('/api/chat',{'business':bid,'welcome':True},expect=202)
                    for _ in range(100):
                        result=call(f'/api/chat?business={bid}&id={job["id"]}')
                        if result['status']!='working':break
                        time.sleep(.05)
                    assert result['status']=='complete' and all(result['setup'].values()), (kind,result)
                    assert 'AURA_SETUP' not in result['reply'], 'verify the raw native reply before hiding its marker from the user'
                    assert not call('/api/chats?business=other-business')['items']
                picker={'kind':'pi','view':'favorites','favorites':['fixture/model'],'providers':['fixture'],
                        'efforts':{'fixture/model':'high','fixture/another-model':'low'}}
                call('/api/preferences',{'model_picker':picker})
                saved_picker=Workspace(settings_file=app.settings_file).state(bid)['model_picker']['pi']
                assert saved_picker['favorites']==['fixture/model']
                assert saved_picker['efforts']==picker['efforts'], 'effort choices survive a server restart per model'
                call('/api/preferences',{'model_picker':{k:v for k,v in picker.items() if k!='efforts'}})
                assert call('/api/state?business='+bid)['model_picker']['pi']['efforts']==picker['efforts']
                call('/api/preferences',{'model_picker':{**picker,'efforts':['high']}},expect=400)
                call('/api/preferences',{'model_picker':{**picker,'view':'unsupported'}},expect=400)
                requests=[json.loads(line) for line in fixture2.with_suffix('.requests').read_text().splitlines()]
                assert all(req.get('type')!='prompt' for req in requests)
                assert secret not in json.dumps(requests)
                assert call('/api/state?business='+bid)['records']==snapshot['records']
            finally:
                view.installed_agents=original_agents
                call('/api/connections/remove', {'provider':'fal'})
                assert 'FAL_KEY' not in app.connections.environment()
            original = app.static
            custom = base / 'custom-interface'
            shutil.copytree(original, custom)
            page = custom / 'index.html'
            page.write_text(re.sub(r'<title>[^<]*</title>', '<title>Custom example workspace</title>', page.read_text(encoding='utf-8')), encoding='utf-8')
            app.static = custom
            assert 'Custom example workspace' in call('/') and '__AURA_TOKEN__' not in call('/')
            assert 'Custom example workspace' not in (original / 'index.html').read_text(encoding='utf-8')
            # Combine native catalogues without merging distinct funding/access paths.
            original_agents, original_options = view.installed_agents, app.agent_options
            fixture_models = {
                'codex':[{'id':'gpt-shared','provider':'openai','access':'signin'}],
                'omp':[{'id':'openai-codex/gpt-shared','provider':'openai-codex'}],
                'pi':[{'id':'openai/gpt-shared','provider':'openai','access':'api'},
                      {'id':'openrouter/openai/gpt-shared','provider':'openrouter'},
                      {'id':'openrouter/anthropic/claude-shared','provider':'openrouter'},
                      {'id':'0local/qwen','provider':'0local'}]}
            view.installed_agents=lambda:[{'id':kind,'name':kind,'argv':[sys.executable]} for kind in ('codex','omp','pi','hermes')]
            def catalogue_options(kind, refresh=False):
                if kind=='hermes':raise ValueError('Connection timed out')
                return {'models':[dict(m,name=m['id'],efforts=['low','high'],default_effort='low') for m in fixture_models[kind]],'model':''}
            app.agent_options=catalogue_options
            try:
                combined=call('/api/model-catalog')
                shared=[m for m in combined['models'] if m['provider']=='openai']
                assert {m['access'] for m in shared}=={'signin','api','openrouter'}
                assert len(shared)==3 and len(next(m for m in shared if m['access']=='signin')['routes'])==2
                route=next(r for m in shared if m['access']=='signin' for r in m['routes'] if r['agent']=='omp')
                applied=call('/api/connect',{'kind':route['agent'],'model':route['model'],'effort':'low'})
                assert applied['selected']=='omp' and applied['model']=='openai-codex/gpt-shared'
                assert any(m['provider']=='local' for m in combined['models'])
                assert any(m['provider']=='anthropic' and m['access']=='openrouter' for m in combined['models'])
                assert len(combined['unavailable'])==1 and combined['picker']['view']=='all'
                scoped=call('/api/model-catalog?kind=codex')
                assert scoped['kind']=='codex' and len(scoped['models'])==1 and not scoped['unavailable']
                assert all(r['agent']=='codex' for m in scoped['models'] for r in m['routes']), 'app selection must constrain every model route'
                call('/api/model-catalog?kind=unsupported',expect=400)
                call('/api/preferences',{'model_picker':{'kind':'all',**combined['picker']},'preferred_app':'codex'})
                assert Workspace(settings_file=app.settings_file).preferences['model_picker']['all']['view']=='all'
                assert call('/api/state?business='+bid)['preferred_app']=='codex'
                services=call('/api/connections')['items']
                assert all(r['category']==('models' if r['id'] in {'openai','anthropic','google','xai','openrouter'} else 'tools') for r in services)
            finally:
                view.installed_agents, app.agent_options=original_agents, original_options
            print('Visual workspace HTTP, isolation, native transport/discovery, protected API credentials, welcome, and preferences passed.')
        finally:
            server.shutdown()
            server.server_close()
            for key, value in prior.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == '__main__':
    main()
