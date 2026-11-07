"""Exercise saved assistants, native results, and parent/child transcript isolation."""
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from unittest.mock import patch
import json
import os
import sqlite3
import shutil
import subprocess
import sys
import tempfile
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))


def wait(check):
    end=time.monotonic()+10
    while time.monotonic()<end:
        if check():return
        time.sleep(.02)
    raise AssertionError('Timed out waiting for isolated work')


def main():
    import workspace_assistants as assistants
    import workspace_schedules as schedules
    import workspace_storage as storage
    import workspace_codex as codex
    import workspace_agents as agents
    import workspace_specialists as specialists
    import workspace_agent_settings as delegation_settings
    from workspace_delegation import Tracker
    from workspace_ui import Workspace,handler_for
    from setup import setup
    with tempfile.TemporaryDirectory(prefix='aura-assistants-') as temporary, patch.dict(os.environ):
        base=Path(temporary);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),
                          LOCALAPPDATA=str(base/'local'),CODEX_HOME=str(base/'codex'),HERMES_HOME=str(base/'hermes'))
        bid=setup(organization='Assistant studio')['business_id']
        native_env={**os.environ,'HOME':str(base/'home'),'USERPROFILE':str(base/'home'),'PI_CODING_AGENT_DIR':str(base/'pi')}
        for kind in specialists.APPS:
            native_env['PI_CODING_AGENT_DIR']=str(base/kind/'config')
            # Native files remain authoritative, including settings Aura does not understand.
            saved=specialists.save(kind,root,native_env,{'scope':'project','name':'Jeff','description':'Find evidence with sources.',
                                                       'instructions':'Read the relevant references.','model':'pro' if kind=='antigravity' else 'provider/model'})
            original=saved
            extra=saved['source']+'\n[features]\nmemories = false\n' if kind=='codex' else saved['source'].replace('---\n','---\n# Keep this native option\ncustom: {enabled: true}\n',1)
            saved=specialists.save(kind,root,native_env,{**saved,'source':extra})
            saved=specialists.save(kind,root,native_env,{'scope':'project','file':saved['file'],'revision':saved['revision'],
                                                      'description':'Research customer needs.','instructions':'Return evidence.\nExplain unknowns.','model':''})
            assert not saved['model'] and saved['instructions']=='Return evidence.\nExplain unknowns.'
            assert saved['settings']['features']['memories'] is False if kind=='codex' else saved['settings']['custom']['enabled'] is True
            assert '# Keep this native option' in saved['source'] if kind!='codex' else True
            try:specialists.save(kind,root,native_env,{**original,'description':'Stale replacement'});raise AssertionError('A stale native definition overwrote an external edit')
            except ValueError as error:assert 'changed' in str(error)
            try:specialists.read(kind,root,native_env,'project','../outside'+('.toml' if kind=='codex' else '.md'));raise AssertionError('Native file traversal succeeded')
            except ValueError:pass
            profile={'id':'linked','name':'Jeff','app':kind,'native_agent':{k:saved[k] for k in ('app','scope','file')}}
            assistants.validate({bid:[profile]})
            current=assistants.resolved(profile,kind,root,native_env)
            assert current['instructions']==saved['instructions'] and 'instructions' not in profile
            native_user=specialists.save(kind,root,native_env,{'scope':'user','name':'Jeff','description':'Personal agent','instructions':'Personal'})
            inventory=specialists.inventory(kind,root,native_env)
            assert any(r['scope']=='user' and r['shadowed'] for r in inventory['items'])
        # Native reported roles stay display-only; the harness owns their definitions.
        roster=specialists.reported_agents('# Available Agents\n- `scout` (READ-ONLY): Find evidence.\n- `reviewer`: Review changes.\n# Examples\n- `ignore`: example')
        assert roster=={'scout':'Find evidence.','reviewer':'Review changes.'}
        # Named routes retain native fields that Aura does not edit, including private credentials.
        native_routes={'backend':'model_map','custom':True,'backends':{'model_map':{'default':'research','extra':7,'options':[{'name':'research','model':'old','provider':'native','api_key':'private','service_tier':'priority'}]}}}
        edited=delegation_settings.route_changes(native_routes,{'mode':'model_map','models':[{'name':'research','model':'new','provider':'native','description':'Find evidence.'}],'model_default':'research'})
        route=edited['backends']['model_map']['options'][0]
        assert route['api_key']=='private' and route['service_tier']=='priority' and edited['custom'] and edited['backends']['model_map']['extra']==7
        assert native_routes['backends']['model_map']['options'][0]['model']=='old'
        try:delegation_settings.route_changes(native_routes,{'mode':'model_map','models':[]});raise AssertionError('Empty native routes activated')
        except ValueError:pass
        # TOML-looking instructions are data, not keys for the structured editor.
        source='name = "Jeff"\ndescription = "Research"\ndeveloper_instructions = """\nmodel = "keep this example"\n[features]\n"""\nmodel = "old"\n'
        changed=specialists.changed_source('codex',source,{'model':'new'})
        assert specialists.parse('codex',changed)['model']=='new' and 'model = "keep this example"' in changed
        # Only native-reported ACP settings are exposed; unrelated settings stay separate.
        reported=delegation_settings.reported([{'id':'workers','name':'Subagent model','options':[{'value':'small','name':'Small'}],'currentValue':'small'},
                                             {'id':'cache','name':'Cache','options':[{'value':'on'}],'currentValue':'on'}])
        assert len(reported['fields'])==1 and reported['fields'][0]['id']=='workers'
        # A Hermes link selects the native profile without another gateway on every message.
        native_profile={'id':'profile','name':'Research','app':'hermes','native_agent':{'app':'hermes','scope':'profile','file':'research'}}
        assistants.validate({bid:[native_profile]})
        with patch('workspace_specialists.read',side_effect=AssertionError('Unexpected metadata process')):
            linked_profile=assistants.resolved(native_profile,'hermes',root,native_env,native_only=True)
            assert linked_profile['native_primary'] and linked_profile['native_name']=='research' and linked_profile['instructions']==''
        # Profile saves reuse one native client, preserve native defaults, and verify readback.
        import workspace_hermes as hermes
        native_profile_state={'name':'research','description':'Research','soul':'Read evidence.','model':{'provider':'native','default':'worker'},'skills':[],
                              'toolsets':[{'name':'files','enabled':True}],'toolsets_pinned':False,'mcp_servers':[]}
        native_calls=[]
        def profile_call(method,**params):
            native_calls.append((method,params))
            if method=='profiles.create':
                assert params['mirror_credentials'] is False and params['no_alias'] and params['no_skills'] is False
                native_profile_state.update(soul=params['soul'],description=params['description']);return {'ok':True}
            if method=='profiles.describe':return json.loads(json.dumps(native_profile_state))
            if method=='profiles.configure':
                native_profile_state['soul']=params.get('soul',native_profile_state['soul'])
                if params.get('enabled_toolsets')==[]:native_profile_state['toolsets_pinned']=False
                return {'ok':True}
            raise AssertionError(method)
        saved_profile=hermes._save_profile(profile_call,{'name':'research','description':'Research','instructions':'Native instructions','model':''})
        saved_profile=hermes._save_profile(profile_call,{'file':'research','revision':saved_profile['revision'],'instructions':'Changed instructions','enabled_toolsets':[]})
        assert saved_profile['instructions']=='Changed instructions' and saved_profile['model']=='native:worker'
        try:hermes._save_profile(profile_call,{'file':'research','revision':'stale','instructions':'Wrong'});raise AssertionError('Stale profile overwrote native instructions')
        except ValueError:pass
        # Hermes treats string settings literally; JSON quoting would change the model ID.
        hermes_values={'model':'','provider':''}
        def hermes_config(command,args,cwd,env):
            if args[:1]==['--profile']:
                assert args[1]=='research';args=args[2:]
            if args[:2]==['plugins','list']:return '[]'
            if args[:2]==['config','get']:return json.dumps(hermes_values)
            assert args[:2]==['config','set']
            hermes_values[args[2].split('.')[-1]]=args[3]
            return ''
        with patch('workspace_context_settings.run',side_effect=hermes_config):
            before=delegation_settings.describe(['native-fixture'],'hermes',root,native_env)
            after=delegation_settings.save(['native-fixture'],'hermes',root,native_env,{'delegation.model':'provider/model'},before['revision'])
            assert hermes_values['model']=='provider/model'
            scoped=delegation_settings.describe(['native-fixture'],'hermes',root,native_env,profile='research')
            assert scoped['revision']!=after['revision'],'A settings revision lost its native profile scope'
            delegation_settings.save(['native-fixture'],'hermes',root,native_env,{'delegation.provider':'custom'},scoped['revision'],profile='research')
            assert hermes_values['provider']=='custom'
        program="import sys;from pathlib import Path;Path('received.txt').write_text(sys.stdin.read(),encoding='utf-8');print('Finished the requested work.')"
        app=Workspace(agent={'name':'Local fixture','argv':[sys.executable,'-c',program]},settings_file=base/'prefs.json')
        app.preferences['connection']={'kind':'configured','model':'original-model','effort':''}
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));threading.Thread(target=server.serve_forever,daemon=True).start()
        def call(path,data=None,status=200):
            request=Request(f'http://127.0.0.1:{server.server_port}'+path,
                data=json.dumps(data).encode() if data is not None else None,
                headers={'X-Aura-Token':app.token,'X-Aura-Workspace':str(root),'Content-Type':'application/json'})
            try:
                with urlopen(request) as response:
                    assert response.status==status
                    return json.load(response)
            except HTTPError as exc:
                assert exc.code==status,(exc.code,exc.read())
                return {}
        try:
            with patch.object(app,'native_choice',return_value={'id':'omp','name':'OMP','argv':['native-fixture']}):
                linked=call('/api/agents',{'business':bid,'name':'Researcher','description':'Research with sources.',
                                         'instructions':'Return evidence and unknowns.','app':'omp','publish_native':'on'})['items'][0]
                assert linked['native_agent']=={'app':'omp','scope':'project','file':'Researcher.md'} and not linked['instructions']
                definition=call('/api/native-agents?business='+bid+'&kind=omp&action=read&scope=project&file=Researcher.md')
                assert definition['instructions']=='Return evidence and unknowns.'
                definition['description']='Find primary sources.'
                call('/api/native-agents',{'business':bid,'kind':'omp','action':'save',**{k:definition[k] for k in ('scope','file','revision','description')}})
                call('/api/native-agents',{'business':bid,'kind':'omp','action':'save',**{k:definition[k] for k in ('scope','file','revision','description')}},400)
                assert call('/api/agents?business='+bid)['items'][0]['id']==linked['id']
                call('/api/agents',{'business':bid,'id':linked['id'],'name':'Research partner'})
                call('/api/agents',{'business':bid,'action':'remove','id':linked['id']})
                assert Path(definition['path']).exists(),'Removing a profile removed the native definition'
            saved=call('/api/assistants',{'business':bid,'name':'Jeff','instructions':'Research carefully.','model':'assistant-model'})['items'][0]
            assert assistants.profiles(storage.view_preferences(root),bid)[0]['id']==saved['id']
            call('/api/assistants',{'business':bid,'name':[]},400)
            call('/api/assistants',{'business':'another-business','name':'Wrong'},400)
            started=call('/api/chat',{'business':bid,'chat_id':'','text':'Find the next step.','assistant_id':saved['id']},202)
            wait(lambda:app.jobs[started['id']]['status']!='working')
            with app.lock:pass
            job=app.jobs[started['id']];assert job['status']=='complete' and job['model']=='assistant-model',job
            text=(root/'received.txt').read_text(encoding='utf-8')
            assert 'Research carefully.' in text and 'Jeff' in text and str(root) in text
            chat=next(c for c in app.preferences['chats'] if c['id']==started['chat_id'])
            assert chat['assistant_id']==saved['id'] and app.preferences['connection']['model']=='original-model'
            chat['subagents']=[{'id':'earlier-child','name':'Research','status':'complete','result':'Useful evidence'}]
            call('/api/assistants',{'business':bid,'id':saved['id'],'name':'Janice','instructions':'Check the evidence.'})
            next_turn=call('/api/chat',{'business':bid,'chat_id':chat['id'],'text':'Continue.'},202)
            wait(lambda:app.jobs[next_turn['id']]['status']!='working')
            with app.lock:pass
            assert 'Check the evidence.' in (root/'received.txt').read_text(encoding='utf-8')
            assert app.conversation(bid,chat['id'])['chat']['subagents'][0]['id']=='earlier-child'
            # Native output stays where the scheduler put it; selection is constrained to its own history.
            jobs=base/'hermes/cron/jobs.json';jobs.parent.mkdir(parents=True)
            jobs.write_text(json.dumps({'jobs':[{'id':'weekly','name':'Weekly review','prompt':'Review work','schedule':{'expr':'0 9 * * 1'},'workdir':str(root)}]}))
            outputs=base/'hermes/cron/output/weekly';outputs.mkdir(parents=True)
            for day in ('01','02'):(outputs/f'2026-11-{day}_09-00-00.md').write_text('Report '+day)
            task=next(t for t in schedules.inventory(workspaces=[root])['items'] if t['owner']=='hermes')
            with patch.object(app,'recent_workspaces',return_value=[{'path':str(base/'another-workspace')}]), patch('workspace_ui.workspace_schedules.inventory',return_value={'items':[],'notes':[]}) as inventory:
                call('/api/schedules?scope=workspace')
                assert inventory.call_args.kwargs['workspaces']==[root],'Assistant assignment must only offer tasks eligible in the selected workspace'
            call('/api/assistants',{'business':bid,'action':'assign_task','id':saved['id'],'task_id':task['id']})
            native_task_before=jobs.read_bytes()
            other=call('/api/assistants',{'business':bid,'name':'Research helper','instructions':'Review sources.'})['items'][-1]
            moved=call('/api/assistants',{'business':bid,'action':'assign_task','id':other['id'],'task_id':task['id']})
            assert [p['id'] for p in moved['items'] if task['id'] in p['task_ids']]==[other['id']]
            assert jobs.read_bytes()==native_task_before,'Moving responsibility must preserve the native task'
            call('/api/assistants',{'business':bid,'action':'assign_task','id':saved['id'],'task_id':task['id']})
            call('/api/assistants',{'business':bid,'action':'remove','id':other['id']})
            history=call('/api/schedules/history?id='+task['id'])
            assert len(history['items'])==2 and history['items'][0]['id'].startswith('2026-11-02')
            older=call('/api/schedules/result?id='+task['id']+'&run_id=2026-11-01_09-00-00.md')
            assert older['text']=='Report 01'
            call('/api/schedules/result?id='+task['id']+'&run_id=../private.md',status=400)
            before=jobs.read_bytes()
            call('/api/assistants',{'business':bid,'action':'remove','id':saved['id']})
            assert not call('/api/assistants?business='+bid)['items'] and jobs.read_bytes()==before
            assert call('/api/conversation?business='+bid+'&chat_id='+chat['id'])['messages']
            assert outputs.joinpath('2026-11-02_09-00-00.md').exists()
            # The same JSON helpers are available without the UI.
            command=[sys.executable,str(ROOT/'scripts/workspace_schedules.py'),'result','--id',task['id'],'--workspace',str(root)]
            result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',check=True)
            assert json.loads(result.stdout)['text']=='Report 02'
            import workspace_collections as collections
            collection=collections.create(bid,{'key':'agent-reference','name':'Agent research','purpose':'Reuse relevant saved findings'})
            collections.apply(bid,collection['id'],{'revision':collection['revision'],'run_id':'agent-reference-proof','items':[{'id':'finding','title':'DATASET_BODY_MUST_NOT_BE_IN_TASK_PROMPT'}]})
            result=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_assistants.py'),'save','--business',bid,'--input','-'],
                input=json.dumps({'name':'CLI assistant','instructions':'Keep it simple.','context_refs':[{'kind':'collection','id':collection['id']}]}),capture_output=True,text=True,encoding='utf-8',check=True)
            cli_profile=json.loads(result.stdout)
            assert call('/api/assistants?business='+bid)['items'][0]['id']==cli_profile['id']
            created=[]
            def native_create(data,command,env,workspace,execution):
                created.append(data)
                native=json.loads(jobs.read_text())
                native['jobs'].append({'id':'assistant-task','name':data['name'],'prompt':data['description'],
                                       'schedule':{'expr':data['schedule']},'workdir':str(workspace)})
                jobs.write_text(json.dumps(native))
                return next(t for t in schedules.inventory(workspaces=[root])['items'] if t['native_id']=='assistant-task')
            with patch('workspace_ui.installed_agents',return_value=[{'id':'hermes','name':'Hermes fixture','argv':['fixture','chat']}]), \
                 patch.object(app,'agent_options',return_value={'models':[{'id':'test:model'}]}), \
                 patch.object(app,'agent_efforts',return_value={'efforts':[]}), patch.object(schedules,'create',side_effect=native_create):
                app.schedule_action(bid,{'action':'create','app':'hermes','name':'Assistant review','description':'Summarize relevant work.',
                                         'when':'every 1h','model':'test:model','assistant_id':cli_profile['id']})
                wait(lambda:app.schedule_job['status']!='working')
                assert app.schedule_job['status']=='complete',app.schedule_job
            assert 'Keep it simple.' in created[0]['description'] and bid in created[0]['description']
            assert collection['id'] in created[0]['description'] and 'workspace_collections.py' in created[0]['description']
            assert 'DATASET_BODY_MUST_NOT_BE_IN_TASK_PROMPT' not in created[0]['description']
            assert app.schedule_job['task_id'] in assistants.find(storage.view_preferences(root),bid,cli_profile['id'])['task_ids']
            # Portable profiles survive a view round trip; another workspace cannot see them.
            portable=storage.view_preferences(root);assert assistants.profiles(portable,bid)[0]['name']=='CLI assistant'
            other=base/'other';storage.save_view(other,{})
            assert not storage.view_preferences(other).get('assistants')
        finally:server.shutdown();server.server_close()
        # Read native Codex run metadata without touching a real desktop database.
        dbpath=base/'codex/sqlite/codex.db';dbpath.parent.mkdir(parents=True)
        with sqlite3.connect(dbpath) as db:
            db.execute('CREATE TABLE automations (id,name,prompt,status,next_run_at,last_run_at,cwds,rrule,model,reasoning_effort,updated_at)')
            db.execute('INSERT INTO automations VALUES (?,?,?,?,?,?,?,?,?,?,?)',('daily','Daily review','Review','ACTIVE',0,0,json.dumps([str(root)]),'FREQ=DAILY','model','low',1))
            db.execute('CREATE TABLE automation_runs (thread_id,automation_id,status,thread_title,inbox_title,inbox_summary,created_at,archived_assistant_message)')
            db.execute('INSERT INTO automation_runs VALUES (?,?,?,?,?,?,?,?)',('native-run','daily','completed','Daily result','','Summary',123,'Full saved result'))
        db.close()
        task=next(t for t in schedules.inventory(workspaces=[root])['items'] if t['owner']=='codex')
        assert schedules.result(task['id'],[root])['text']=='Full saved result'
        assert schedules.history(task['id'],[root])['items'][0]['native_id']=='native-run'
        with sqlite3.connect(dbpath) as db:db.execute('DROP TABLE automation_runs')
        db.close()
        try:schedules.history(task['id'],[root]);raise AssertionError('Unreadable result metadata looked empty')
        except ValueError as exc:assert 'Could not read' in str(exc)
        with sqlite3.connect(dbpath) as db:db.execute('ALTER TABLE automations RENAME COLUMN name TO unsupported_name')
        db.close()
        unavailable=schedules.inventory(workspaces=[root])
        assert any('Could not read' in note for note in unavailable['notes'])
        with patch.object(Path,'stat',side_effect=PermissionError('denied')):
            try:schedules.result_path(base/'hermes','weekly',strict=True);raise AssertionError('Unreadable reports looked empty')
            except ValueError as exc:assert 'Could not read' in str(exc)
        # Real subprocess streams: child replies/session IDs cannot overwrite the parent.
        def stream(events):return 'import json,sys;sys.stdin.read();events='+repr(events)+'\nfor event in events:print(json.dumps(event),flush=True)'
        updates=[]
        events=[{'type':'thread.started','thread_id':'parent'},
                {'type':'item.completed','item':{'type':'collab_tool_call','tool':'spawn_agent','sender_thread_id':'parent','receiver_thread_ids':['child'],'prompt':'Research','agents_states':{'child':{'status':'running'}}}},
                {'type':'item.completed','item':{'type':'collab_tool_call','tool':'wait','receiver_thread_ids':['child'],'agents_states':{'child':{'status':'completed','message':'Evidence collected'}}}},
                {'type':'item.completed','item':{'type':'agent_message','text':'Parent reply'}}]
        out=codex.run([sys.executable,'-c',stream(events),'exec'],root,'Request',None,'main','low',lambda **v:updates.append(v),dict(os.environ),child_model='worker')
        assert out['native_id']=='parent' and out['reply']=='Parent reply'
        children=[v['subagents'] for v in updates if 'subagents' in v][-1]
        assert children[0]['status']=='complete' and children[0]['result']=='Evidence collected'
        updates=[]
        events=[{'type':'system','session_id':'parent'},
                {'type':'assistant','message':{'content':[{'type':'tool_use','id':'task-1','name':'Agent','input':{'description':'Research','prompt':'Find evidence','model':'worker'}}]}},
                {'type':'assistant','session_id':'child-session','parent_tool_use_id':'task-1','message':{'content':[{'type':'text','text':'Child-only reply'}]}},
                {'type':'user','message':{'content':[{'type':'tool_result','tool_use_id':'task-1','content':'Evidence found'}]}},
                {'type':'result','session_id':'parent','result':'Parent reply'}]
        out=agents.run([sys.executable,'-c',stream(events),'--print'],'claude',root,dict(os.environ),'Request',None,'main','',lambda **v:updates.append(v))
        assert out['native_id']=='parent' and out['reply']=='Parent reply'
        assert not any(v.get('native_id')=='child-session' or v.get('reply')=='Child-only reply' for v in updates)
        assert [v['subagents'] for v in updates if 'subagents' in v][-1][0]['status']=='complete'
        updates=[]
        events=[{'type':'system','session_id':'hermes-parent'},
                {'type':'tool_use','name':'delegate_task','tool_call_id':'delegate-1','input':{'tasks':[{'goal':'Find evidence'}]}},
                {'type':'tool_result','name':'delegate_task','tool_call_id':'delegate-1','output':json.dumps({'results':[{'task_index':0,'status':'completed','summary':'Evidence found','model':'worker'}]})},
                {'type':'result','session_id':'hermes-parent','status':'SUCCESS','response':'Parent reply'}]
        out=agents.run([sys.executable,'-c',stream(events),'chat'],'hermes',root,dict(os.environ),'Request',None,'main','',lambda **v:updates.append(v))
        assert out['reply']=='Parent reply' and out['native_id']=='hermes-parent'
        child=[v['subagents'] for v in updates if 'subagents' in v][-1][1]
        assert child['model']=='worker' and child['task']=='Find evidence' and child['result']=='Evidence found' and child['status']=='complete'
        tracker=Tracker(None)
        tracker.observe('claude',{'type':'assistant','message':{'content':[{'type':'tool_use','id':'background','name':'Agent','input':{'run_in_background':True}}]}})
        tracker.observe('claude',{'type':'system','subtype':'task_started','task_id':'native-task','tool_use_id':'background'})
        tracker.observe('claude',{'type':'user','message':{'content':[{'type':'tool_result','tool_use_id':'background','content':'Started in background'}]}})
        assert tracker.items['background']['status']=='working'
        tracker.observe('claude',{'type':'system','subtype':'task_notification','task_id':'native-task','status':'completed','summary':'Done'})
        assert len(tracker.items)==1 and tracker.items['background']['status']=='complete'
        # OMP's native background task and wait result refer to the same worker.
        tracker=Tracker(None)
        tracker.observe('omp',{'type':'tool_execution_end','toolCallId':'spawn','result':{'details':{'progress':[{'index':0,'id':'job','agent':'scout','status':'pending','resolvedModelIdentity':'native-worker'}]}}})
        tracker.observe('omp',{'type':'tool_execution_end','toolCallId':'wait','result':{'details':{'jobs':[{'id':'job','status':'completed','resultText':'Evidence found','resolvedModelIdentity':'native-worker'}]}}})
        assert tracker.items['spawn']['status']=='complete' and tracker.items['spawn:0']['model']=='native-worker' and tracker.items['spawn:0']['result']=='Evidence found'
        # Extension progress remains working until the native tool reports completion.
        tracker=Tracker(None)
        tracker.observe('claude',{'type':'assistant','message':{'content':[{'type':'tool_use','id':'model-proof','name':'Agent','input':{'model':'requested-alias'}}]}})
        assert tracker.items['model-proof']['requested_model']=='requested-alias' and not tracker.items['model-proof'].get('model')
        tracker.observe('claude',{'type':'assistant','parent_tool_use_id':'model-proof','message':{'model':'reported-model-id','content':[]}})
        assert tracker.items['model-proof']['model']=='reported-model-id'
        tracker=Tracker(None)
        tracker.observe('pi',{'type':'tool_execution_start','toolName':'subagent','toolCallId':'tool','args':{'task':'Research'}})
        detail={'details':{'results':[{'agent':'Scout','task':'Find evidence','model':'worker','exitCode':-1,'messages':[]}]}}
        tracker.observe('pi',{'type':'tool_execution_update','toolCallId':'tool','partialResult':detail})
        assert tracker.items['tool:0']['status']=='working'
        detail['details']['results'][0].update(exitCode=0,messages=[{'role':'assistant','content':[{'type':'text','text':'Found evidence'}]}])
        tracker.observe('pi',{'type':'tool_execution_end','toolCallId':'tool','result':detail})
        assert tracker.items['tool:0']['status']=='complete' and tracker.items['tool:0']['result']=='Found evidence'
        tracker.observe('pi',{'type':'tool_execution_update','result':{'details':{'results':123}}})
        # Historical Codex events restore actual native names/models and outcomes.
        transcript=base/'native.jsonl'
        rows=[{'type':'event_msg','timestamp':'2026-11-01T12:00:00Z','payload':{'type':'collab_agent_spawn_end','new_thread_id':'child','new_agent_nickname':'Scout','model':'worker','status':'running','prompt':'Research'}},
              {'type':'event_msg','timestamp':'2026-11-01T12:01:00Z','payload':{'type':'collab_waiting_end','statuses':{'child':{'completed':'Done'}}}}]
        transcript.write_text('\n'.join(json.dumps(r) for r in rows),encoding='utf-8')
        with patch.object(codex,'rpc',return_value={'id':'parent','path':str(transcript)}):
            restored=codex.history(['fixture'],root,'parent')['subagents'][0]
            assert restored['name']=='Scout' and restored['model']=='worker' and restored['status']=='complete'
            assert restored['updated']-restored['started']==60
        # Bounds apply to finished history, never to currently active workers.
        tracker=Tracker(None)
        for index in range(70):tracker.put('done-'+str(index),status='complete',result='Done')
        assert len(tracker.items)==50 and 'done-69' in tracker.items and 'done-0' not in tracker.items
        for index in range(55):tracker.put('active-'+str(index),status='working')
        assert all('active-'+str(index) in tracker.items for index in range(55)) and len(tracker.items)==105
        tracker.put('active-0',status='complete')
        assert len(tracker.items)==104 and 'active-54' in tracker.items
        updates=[];tracker=Tracker(lambda **values:updates.append(values))
        tracker.observe('hermes',{'type':'tool_use','name':'delegate_task','tool_call_id':'batch',
                                 'input':{'tasks':[{'goal':'Task '+str(i)} for i in range(55)]}})
        assert len(updates)==1 and len(updates[0]['subagents'])==56,'One native frame caused repeated full snapshots'
    node=shutil.which('node')
    if node:subprocess.run([node,str(ROOT/'tests/workspace_work_ui.cjs'),str(ROOT/'interface/workspace-work.js')],check=True)
    print('Assistants and native work passed: portable profiles, shared CLI/API, retained histories, native results, and parent/child isolation.')


if __name__=='__main__':main()
