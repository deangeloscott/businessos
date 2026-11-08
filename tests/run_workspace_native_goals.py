"""Native goal boundaries: transport, continuation, completion evidence and custom adapters."""
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from unittest.mock import patch
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from workspace_execution import Execution
from workspace_native_io import codex_run
from workspace_agents import run
from workspace_native_goals import spec,custom_run

FIXTURE=r'''
import json,sys,os
def emit(value):print(json.dumps(value),flush=True)
def reply(request,data):
    emit({'id':request['id'],**({'result':data} if 'method' in request else {'type':'response','success':True,'data':data})})
for line in sys.stdin:
    r=json.loads(line);op=r.get('method',r.get('type',r.get('action')))
    if op=='initialize':reply(r,{})
    elif op=='thread/start':reply(r,{'thread':{'id':'native'}})
    elif op=='thread/backgroundTerminals/list':reply(r,{'data':[]})
    elif op=='thread/goal/get':reply(r,{'goal':{'objective':'Other native work','status':'active'} if os.getenv('FOREIGN_GOAL') else None})
    elif op=='thread/goal/set':
        if r['params'].get('status')=='paused':
            reply(r,{'goal':{'objective':'Finish the guide','status':'paused'}})
            emit({'method':'turn/completed','params':{'threadId':'native','turn':{'status':'completed'}}})
            continue
        assert r['params']['objective']=='Finish the guide'
        assert r['params']['tokenBudget']==1000 and r['params']['origin']=='user'
        reply(r,{'goal':{'objective':'Finish the guide','status':'active'}})
    elif op=='turn/start':
        assert r['params']['input'][0]['text']=='Aura context and user request'
        reply(r,{'turn':{'id':'t1'}})
        emit({'method':'item/completed','params':{'threadId':'native','item':{'type':'agentMessage','id':'a','text':'First step'}}})
        if os.getenv('CLEAR_CHECK'):
            emit({'method':'thread/goal/cleared','params':{'threadId':'native'}})
            emit({'method':'turn/completed','params':{'threadId':'native','turn':{'status':'completed'}}})
            continue
        if os.getenv('PAUSE_CHECK'):continue
        emit({'method':'turn/completed','params':{'threadId':'native','turn':{'status':'completed'}}})
        emit({'method':'turn/started','params':{'threadId':'native','turn':{'id':'t2'}}})
        emit({'method':'item/completed','params':{'threadId':'native','item':{'type':'agentMessage','id':'b','text':'Verified result'}}})
        emit({'method':'thread/goal/updated','params':{'threadId':'native','goal':{'status':'complete','objective':'Finish the guide'}}})
        emit({'method':'turn/completed','params':{'threadId':'native','turn':{'status':'completed'}}})
    elif op=='get_state':reply(r,{'sessionId':'native','goal':{'objective':'Other native work','status':'active'} if os.getenv('FOREIGN_GOAL') else None})
    elif op=='goal':
        if r['op']=='pause':
            reply(r,{'goal':{'status':'paused'}});emit({'type':'session_settled'});continue
        assert r['op']=='create' and r['token_budget']==1000
        assert 'Aura context and user request' in r['objective']
        config=sys.argv[sys.argv.index('--config')+1]
        assert json.load(open(config))['goal']['continuationModes']==['rpc']
        reply(r,{'goal':{'status':'active','objective':r['objective']}})
        emit({'type':'message_end','message':{'role':'assistant','content':[{'type':'text','text':'First step'}]}})
        if os.getenv('CLEAR_CHECK'):
            emit({'type':'goal_updated','goal':None});emit({'type':'session_settled'});continue
        if os.getenv('PAUSE_CHECK'):continue
        emit({'type':'agent_end'})
        emit({'type':'message_end','message':{'role':'assistant','content':[{'type':'text','text':'Verified result'}]}})
        emit({'type':'goal_updated','goal':{'status':'completed'}})
        emit({'type':'session_settled'})
    elif op=='run':
        emit({'type':'session','id':'native'})
        emit({'type':'goal','status':'active'})
        emit({'type':'reply','text':'Verified result'})
        emit({'type':'goal','status':'completed'})
        emit({'type':'result','status':'complete'})
'''


def main():
    goal={'id':'obj_test','name':'Finish the guide','status':'active','extensions':{'businessos':{'goal':{'scope':'chat'}}}}
    assert spec(goal,{},'codex',{})['token_budget'] is None
    for kind in ('pi','hermes','configured'):
        try:spec(goal,{},kind,{})
        except ValueError:pass
        else:raise AssertionError('Unsupported native modes must not be substituted with a prompt')
    try:spec({**goal,'extensions':{}},{},'codex',{})
    except ValueError:pass
    else:raise AssertionError('Workspace goals must never start an autonomous chat loop')
    with tempfile.TemporaryDirectory(prefix='aura-goal-protocol-') as folder:
        root=Path(folder);fixture=root/'native.py';fixture.write_text(FIXTURE,encoding='utf-8')
        from workspace_native_goals import saved_control
        from unittest.mock import Mock
        native_client=Mock();native_client.call.return_value={'goal':{'objective':'Finish the guide for a different project'}}
        with patch('workspace_agents.Metadata',return_value=native_client):
            try:saved_control({'argv':['fixture']},'omp',root,{},'native','Finish the guide','pause')
            except ValueError:pass
            else:raise AssertionError('An objective prefix is not the same native goal')
        assert native_client.call.call_count==1
        operations=[]
        def codex_client(method,params):
            operations.append(method)
            return {'goal':{'objective':'Different completed goal','status':'complete'}}
        with patch('workspace_codex.rpc',side_effect=lambda argv,callback,*a,**k:callback(codex_client)):
            try:saved_control({'argv':['fixture']},'codex',root,{},'native','Finish the guide','complete')
            except ValueError:pass
            else:raise AssertionError('A foreign completed goal cannot confirm this assignment')
        assert operations==['thread/resume','thread/goal/get']
        from workspace_native_goals import claude_status
        event={'type':'system','subtype':'goal_status','session_id':'native','condition':'Finish the guide','met':True,'tokens':120,'durationMs':2500}
        assert claude_status(event,'Finish the guide','native')['status']=='completed'
        assert claude_status(event,'Finish the guide','other') is None
        assert claude_status({**event,'type':'assistant'},'Finish the guide') is None
        assert claude_status({**event,'met':'true'},'Finish the guide') is None
        assert claude_status({**event,'condition':'Different goal'},'Finish the guide')['status']=='needs_review'
        native_claude=root/'claude.py'
        native_claude.write_text("""import json,sys,os
for line in sys.stdin:
 event=json.loads(line)
 if event.get('type')=='control_request':
  print(json.dumps({'type':'control_response','response':{'request_id':event['request_id'],'subtype':'success','response':{'commands':[{'name':'goal'}]}}}),flush=True)
 elif event.get('type')=='user':
  if os.getenv('FIXTURE_GOAL_UNKNOWN'):
   for item in [{'type':'system','subtype':'init','session_id':'native'},{'type':'assistant','message':{'content':[{'type':'text','text':'Result to review'}]}},{'type':'result','subtype':'success','result':'Result to review','session_id':'native'}]:print(json.dumps(item),flush=True)
   continue
  if os.getenv('FIXTURE_GOAL_ERROR'):
   for item in [{'type':'system','subtype':'goal_status','condition':'Finish the guide','met':False,'sentinel':True},{'type':'result','is_error':True,'subtype':'error_during_execution','errors':['Native quota exhausted']}]:print(json.dumps(item),flush=True)
   continue
  for item in [
   {'type':'system','subtype':'init','session_id':'native'},
   {'type':'system','subtype':'goal_status','condition':'Finish the guide','met':False,'sentinel':True},
   {'type':'assistant','message':{'content':[{'type':'text','text':'First step'}]}},
   {'type':'result','subtype':'success','result':'First step','session_id':'native'},
   {'type':'attachment','attachment':{'type':'goal_status','condition':'Finish the guide','met':False,'reason':'Continue with verification.'}},
   {'type':'assistant','message':{'content':[{'type':'text','text':'Verified result'}]}},
   {'type':'result','subtype':'success','result':'Verified result','session_id':'native'},
   {'type':'attachment','attachment':{'type':'goal_status','condition':'Finish the guide','met':True,'reason':'The requested artifact was verified.'}}
  ]: print(json.dumps(item),flush=True)
""",encoding='utf-8')
        observed=[];execution=Execution();execution.interactive=True
        execution.native_goal=spec(goal,{},'claude',{})
        result=run([sys.executable,str(native_claude)],'claude',root,os.environ.copy(),'Aura context and user request',None,'fixture','',lambda **v:observed.append(v),execution)
        assert result['reply']=='Verified result'
        assert [v['native_goal']['status'] for v in observed if 'native_goal' in v]==['active','active','completed'], observed
        failed=Execution();failed.interactive=True;failed.native_goal=spec(goal,{},'claude',{});errors=[]
        try:run([sys.executable,str(native_claude)],'claude',root,{**os.environ,'FIXTURE_GOAL_ERROR':'1'},'Aura context',None,'fixture','',lambda **v:errors.append(v),failed)
        except ValueError:pass
        else:raise AssertionError('A native goal error must not become a successful reply')
        assert any(v.get('native_goal',{}).get('status')=='needs_review' for v in errors)
        # A retained process must report missing evidence before it becomes idle,
        # rather than waiting until the process eventually closes.
        from workspace_native_sessions import Sessions
        sessions=Sessions();pending=Execution();pending.interactive=True;pending.native_goal=spec(goal,{},'claude',{});unknown=[]
        update=lambda **v:unknown.append(v)
        try:
            result=sessions.run(('proof','business','chat'),{'goal':pending.native_goal},'Aura context',None,pending,update,
                lambda:run([sys.executable,str(native_claude)],'claude',root,{**os.environ,'FIXTURE_GOAL_UNKNOWN':'1'},'Aura context',None,'fixture','',update,pending),root)
            assert result['reply']=='Result to review'
            assert any(v.get('native_goal',{}).get('status')=='needs_review' for v in unknown)
        finally:sessions.close()


        for kind in ('codex','omp','configured'):
            observed=[];execution=Execution();execution.interactive=True
            agent={'native_goal':{'protocol':'aura-goal-v1','argv':[sys.executable,str(fixture)],'token_budget':True}} if kind=='configured' else {}
            execution.native_goal=spec(goal,{'token_budget':1000},kind,agent)
            update=lambda **value:observed.append(value)
            if kind=='codex':result=codex_run([sys.executable,str(fixture),'exec','-'],root,'Aura context and user request',None,'fixture','low',update,os.environ.copy(),execution)
            elif kind=='omp':result=run([sys.executable,str(fixture),'--print'],kind,root,os.environ.copy(),'Aura context and user request',None,'fixture','low',update,execution)
            else:result=custom_run(agent['native_goal']['argv'],root,os.environ.copy(),'Aura context and user request',None,execution,update)
            assert result['reply']=='Verified result',kind
            statuses=[v['native_goal']['status'] for v in observed if 'native_goal' in v]
            assert statuses==['active','complete' if kind=='codex' else 'completed'],(kind,statuses)
            assert execution.goal_control is None
        for kind in ('codex','omp'):
            for scenario in ('PAUSE_CHECK','FOREIGN_GOAL','CLEAR_CHECK'):
                execution=Execution();execution.interactive=True;execution.native_goal=spec(goal,{'token_budget':1000},kind,{})
                observed=[];paused=False
                def update(**value):
                    nonlocal paused
                    observed.append(value)
                    if scenario=='PAUSE_CHECK' and not paused and execution.goal_control:
                        paused=True;execution.goal_control('pause')
                env={**os.environ,scenario:'1'}
                try:
                    result=codex_run([sys.executable,str(fixture),'exec','-'],root,'Aura context and user request',None,'fixture','low',update,env,execution) if kind=='codex' else run([sys.executable,str(fixture),'--print'],kind,root,env,'Aura context and user request',None,'fixture','low',update,execution)
                except ValueError as error:
                    assert scenario=='FOREIGN_GOAL' and 'different' in str(error),(kind,scenario,error)
                else:
                    assert scenario in {'PAUSE_CHECK','CLEAR_CHECK'} and result['reply']=='First step'
                    assert any(v.get('native_goal',{}).get('status')==('paused' if scenario=='PAUSE_CHECK' else 'cleared') for v in observed)
    # Canonical status comes from native evidence and must never finish the parent outcome.
    from setup import setup
    from _common import workspace_scope
    import workspace_goals as goals
    from workspace_native_goals import observe
    with tempfile.TemporaryDirectory(prefix='aura-goal-state-') as folder,patch.dict(os.environ):
        root=Path(folder)/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(Path(folder)/'pointer.json'),AURA_STATE_DIR=str(Path(folder)/'state'))
        bid=setup(organization='Native goal fixture')['business_id']
        with workspace_scope(root):
            parent=goals.save(bid,{'name':'Launch the offer','status':'active'})
            goal=goals.save(bid,{'name':'Write the guide','scope':'chat','chat_id':'chat','workspace_goal_id':parent['id'],'status':'active'})
            chat={'id':'chat','business_id':bid,'workspace':str(root),'goal_id':goal['id']}
            app=SimpleNamespace(preferences={'chats':[chat]},read_cache={},save_preferences=lambda:None)
            request=spec(goal,{},'codex',{})
            observe(app,bid,chat,request,{'status':'budgetLimited'})
            assert goals.find(bid,goal['id'])['status']=='paused'
            observe(app,bid,chat,request,{'status':'active'})
            assert goals.find(bid,goal['id'])['status']=='active'
            observe(app,bid,chat,request,{'status':'complete'})
            assert goals.find(bid,goal['id'])['status']=='completed'
            assert goals.find(bid,parent['id'])['status']=='active'
            fresh=goals.save(bid,{'name':'Review the guide','scope':'chat','chat_id':'chat','status':'active'})
            chat['goal_id']=fresh['id'];request=spec(fresh,{},'codex',{})
            goals.save(bid,{'id':fresh['id'],'status':'paused'})
            observe(app,bid,chat,request,{'status':'complete'})
            assert goals.find(bid,fresh['id'])['status']=='paused','Late native completion must not undo a user pause'
            fresh=goals.save(bid,{'id':fresh['id'],'status':'active'})
            request=spec(fresh,{},'codex',{})
            observe(app,bid,chat,request,{'status':'active','objective':'A different native assignment'})
            observe(app,bid,chat,request,{'status':'complete'})
            assert goals.find(bid,fresh['id'])['status']=='active','A different native goal must not complete the saved assignment'
            assert chat['native_goal']['status']=='needs_review'
            # Editing the old saved goal must not control an unrelated native assignment.
            from workspace_native_goals import control
            app.workspace_path=str(root);chat.update(agent='codex',native_id='native-chat')
            with patch('workspace_native_goals.saved_control') as native_change:
                app.running_jobs=lambda:[]
                control(app,bid,fresh,'pause');native_change.assert_not_called()
                app.running_jobs=lambda:[{'chat_id':'chat','workspace':str(root),'id':'live'}]
                control(app,bid,fresh,'clear');native_change.assert_not_called()
            from workspace_ui import Workspace,handler_for
            fixture=Path(folder)/'custom.py';fixture.write_text(FIXTURE,encoding='utf-8')
            agent={'name':'Different harness','argv':[sys.executable,str(fixture)],'native_goal':{'protocol':'aura-goal-v1','argv':[sys.executable,str(fixture)],'token_budget':True}}
            live=Workspace(agent=agent,settings_file=Path(folder)/'local/preferences.json')
            live.preferences['connection']={'kind':'configured','model':'','effort':''}
            live.preferences['connected_apps']['configured']=dict(live.preferences['connection'])
            owner=live.workspace_chat(bid,'context')['id']
            native=goals.save(bid,{'name':'Finish the guide','scope':'chat','chat_id':owner,'status':'active'})
            goals.link_chat(live.preferences,bid,owner,native['id']);live.save_preferences()
            server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(live));threading.Thread(target=server.serve_forever,daemon=True).start()
            def call(route,data=None):
                req=Request('http://127.0.0.1:'+str(server.server_port)+route,data=json.dumps({'business':bid,**data}).encode() if data is not None else None,headers={'X-Aura-Token':live.token,'Content-Type':'application/json'})
                return json.load(urlopen(req,timeout=15))
            try:
                moved=call('/api/chats/organize',{'id':owner,'pinned':True,'project':'研究 🚀'})['chat']
                assert moved['pinned'] and moved['project']=='研究 🚀'
                try:call('/api/chats/organize',{'id':owner,'pinned':False,'project':'bad\nproject'})
                except HTTPError as error:assert error.code==400
                else:raise AssertionError('Invalid project labels must be rejected atomically')
                unchanged=next(c for c in live.preferences['chats'] if c['id']==owner)
                assert unchanged['pinned'] and unchanged['project']=='研究 🚀'
                # Projects survive without chats, rename all their memberships, and
                # removal ungroups without deleting a chat or its source folder.
                created=call('/api/projects',{'action':'create','name':'Empty project','folder':str(root)})
                assert any(p['name']=='Empty project' and p['folder']==str(root.resolve()) for p in created['projects'])
                assert any(p['name']=='Empty project' for p in call('/api/chats?business='+bid)['projects'])
                if os.name=='nt':
                    with patch('workspace_chat_organization.os.startfile') as opened:
                        assert call('/api/projects',{'action':'open','name':'Empty project'})['opened']
                        opened.assert_called_once_with(str(root.resolve()))
                renamed=call('/api/projects',{'action':'edit','name':'研究 🚀','new_name':'Launch research'})
                assert next(c for c in live.preferences['chats'] if c['id']==owner)['project']=='Launch research'
                assert any(p['name']=='Launch research' for p in renamed['projects'])
                try:call('/api/projects',{'action':'edit','name':'Launch research','new_name':'EMPTY PROJECT'})
                except HTTPError as error:assert error.code==400
                else:raise AssertionError('Duplicate project names must not merge chats silently')
                assert next(c for c in live.preferences['chats'] if c['id']==owner)['project']=='Launch research'
                call('/api/projects',{'action':'remove','name':'Launch research'})
                assert next(c for c in live.preferences['chats'] if c['id']==owner)['project']==''
                assert root.is_dir()
                call('/api/chats/organize',{'id':owner,'project':'研究 🚀'})
                persisted=Workspace(agent=agent,settings_file=live.settings_file)
                from workspace_chat_organization import projects
                assert any(p['name']=='Empty project' for p in projects(persisted,bid))
                assert projects(persisted,'another-business')==[]
                with workspace_scope(Path(folder)/'another-workspace'):
                    assert projects(persisted,bid)==[]
                with patch.dict(live.configured_agent,{'argv':[sys.executable,'-c',"print('Saved project membership.')"]}):
                    started=live.start_chat(bid,'Project fixture',[],chat_id='',project='Empty project')
                    end=time.monotonic()+10
                    while live.jobs[started['id']]['status']=='working' and time.monotonic()<end:time.sleep(.02)
                    assert live.jobs[started['id']]['status']=='complete',live.jobs[started['id']]
                    assert next(c for c in live.preferences['chats'] if c['id']==started['chat_id'])['project']=='Empty project'
                result=call('/api/goals',{'action':'native_start','id':native['id'],'token_budget':1000})
                end=time.monotonic()+15
                while live.jobs[result['job']['id']]['status']=='working' and time.monotonic()<end:time.sleep(.02)
                assert live.jobs[result['job']['id']]['status']=='complete',live.jobs[result['job']['id']]
                assert goals.find(bid,native['id'])['status']=='completed'
                assert call('/api/chats?business='+bid)['items'][0]['pinned']
                assert Workspace(agent=agent,settings_file=live.settings_file).preferences['chats'][0]['project']=='研究 🚀'
            finally:server.shutdown();server.server_close()
    # Claude Code writes its goal verdict to the session transcript; the live stream may omit it.
    from workspace_native_goals import claude_transcript_status
    with tempfile.TemporaryDirectory() as config:
        transcript=Path(config)/'projects/some-project/session-1.jsonl';transcript.parent.mkdir(parents=True)
        rows=[{'type':'attachment','sessionId':'session-1','attachment':{'type':'goal_status','met':False,'condition':'Ship it'}},
              {'type':'assistant','sessionId':'session-1','message':{'content':[{'type':'text','text':'goal_status met'}]}},
              {'type':'attachment','sessionId':'session-1','attachment':{'type':'goal_status','met':True,'condition':'Ship it','reason':'Checked.'}}]
        transcript.write_text('\n'.join(json.dumps(r) for r in rows),encoding='utf-8')
        observed=claude_transcript_status('session-1','Ship it',config)
        assert observed and observed['status']=='completed' and observed['reason']=='Checked.',observed
        assert claude_transcript_status('session-1','Something else',config)['status']=='needs_review'
        assert claude_transcript_status('missing','Ship it',config) is None
    print('Native goal transports passed: native continuation, explicit budgets, completion evidence, workspace boundary and custom-harness protocol.')


if __name__=='__main__':main()
