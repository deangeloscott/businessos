"""Shared context, goal continuity and composer boundaries without model calls."""
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from unittest.mock import patch
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))


def wait(check):
    end=time.monotonic()+12
    while time.monotonic()<end:
        if check():return
        time.sleep(.01)
    raise AssertionError('Timed out waiting for fixture work')


RETRY=r'''
import sys,json,threading
lock=threading.Lock();timer=None;waiting=False
def emit(value):
 with lock:print(json.dumps(value),flush=True)
def finish():
 global waiting
 waiting=False
 emit({'type':'auto_retry_end','success':True,'attempt':1})
 emit({'type':'message_start','message':{'role':'assistant'}})
 emit({'type':'message_end','message':{'role':'assistant','content':[{'type':'text','text':'Finished remaining work.'}],'usage':{'input':8,'output':3}}})
 emit({'type':'agent_settled'})
for line in sys.stdin:
 m=json.loads(line);kind=m.get('type')
 if kind=='get_state':emit({'id':m['id'],'type':'response','success':True,'data':{'sessionId':'native-goal','isStreaming':False,'isRetrying':waiting}})
 elif kind=='prompt':
  waiting=True
  emit({'id':m['id'],'type':'response','success':True})
  emit({'type':'message_end','message':{'role':'assistant','stopReason':'error','errorMessage':'429 quota exhausted','content':[]}})
  emit({'type':'auto_retry_start','attempt':1,'maxAttempts':2,'delayMs':800,'errorMessage':'429 quota exhausted'})
  timer=threading.Timer(.8,finish);timer.start()
 elif kind=='abort_retry':
  if timer:timer.cancel()
  waiting=False;emit({'type':'auto_retry_end','success':False,'attempt':1});emit({'type':'agent_settled'})
'''


def main():
    from setup import setup
    from _common import workspace_scope,write_json_atomic
    import workspace_context as context
    import workspace_goals as goals
    import workspace_activity as activity
    import workspace_agents as agents
    import workspace_assistants as assistants
    import workspace_schedules as schedules
    from workspace_ui import Workspace,handler_for
    from workspace_execution import Execution
    with tempfile.TemporaryDirectory(prefix='aura-composer-') as temp,patch.dict(os.environ):
        base=Path(temp);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        bid=setup(organization='Composer studio')['business_id']
        goal=goals.save(bid,{'name':'Launch offer','target':'Published offer and usable research','horizon':'This quarter','status':'active'})
        assert goals.find(bid,goal['id'])['target']=='Published offer and usable research'
        file=root/'attachments'/bid/'work'/'research.txt';file.parent.mkdir(parents=True,exist_ok=True);file.write_text('Relevant findings',encoding='utf-8')
        program="import sys;from pathlib import Path;text=sys.stdin.read();Path('received.txt').write_text(text,encoding='utf-8');print('Saved useful progress and the next step.')"
        app=Workspace(agent={'name':'Fixture','argv':[sys.executable,'-u','-c',program]})
        app.preferences['connection']={'kind':'configured','model':'fixture','effort':''}
        profile=assistants.save(app.preferences,bid,{'name':'Jeff','instructions':'Research useful evidence.'})
        picks=context.inventory(app,bid,'Launch','goal');assert picks['items'][0]['id']==goal['id']
        resolved=context.resolve(app,bid,[{'kind':'file','id':file.relative_to(root).as_posix(),'label':'Forged label'}],goal['id'])
        assert 'Forged label' not in json.dumps(resolved) and str(file) in resolved['text'] and 'Goal context:' in resolved['text']
        assert len(context.resolve(app,bid,[{'kind':'goal','id':goal['id']}],goal['id'])['references'])==1
        try:context.resolve(app,bid,[{'kind':'assistant','id':profile['id']}]);raise AssertionError('Implicit assistant dispatch accepted')
        except ValueError:pass
        with workspace_scope(base/'different'):
            try:context.resolve(app,bid,[{'kind':'goal','id':goal['id']}]);raise AssertionError('Cross-workspace goal resolved')
            except ValueError:pass
        with patch.object(app,'library_items',return_value={'items':[{'key':'library:versions','kind':'Skill','title':'Custom skill','variants':[]}]}):
            for n in ('one','two'):
                path=base/n/'SKILL.md';path.parent.mkdir();path.write_text(n)
            variants=[{'key':n,'kind':'Skill','sources':[{'path':str(base/n/'SKILL.md')}]} for n in ('one','two')]
            app.library_items.return_value['items'][0]['variants']=variants
            first=context.resolve(app,bid,[{'kind':'library','id':'library:versions','variant':'one'}]);assert '\none' in first['text']
            try:context.resolve(app,bid,[{'kind':'library','id':'library:versions'}]);raise AssertionError('Ambiguous skill version chosen')
            except ValueError:pass
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));threading.Thread(target=server.serve_forever,daemon=True).start()
        def call(path,data=None,expected=200):
            req=Request(f'http://127.0.0.1:{server.server_port}'+path,data=json.dumps(data).encode() if data is not None else None,
                headers={'Content-Type':'application/json','X-Aura-Token':app.token,'X-Aura-Workspace':str(root)})
            try:
                with urlopen(req,timeout=15) as response:code=response.status;value=json.load(response)
            except HTTPError as error:code=error.code;value=json.load(error)
            assert code==expected,(path,code,value);return value
        try:
            refs=[{'kind':'file','id':file.relative_to(root).as_posix()}]
            job=call('/api/chat',{'business':bid,'chat_id':'','text':'Research the offer','references':refs,'goal_id':goal['id']},202)
            wait(lambda:app.jobs[job['id']]['status']!='working');assert app.jobs[job['id']]['status']=='complete',app.jobs[job['id']]
            assert 'Goal context:' in (root/'received.txt').read_text() and 'Research the offer' in (root/'received.txt').read_text()
            shown=call('/api/conversation?business='+bid+'&chat_id='+job['chat_id']);message=shown['messages'][0]
            assert message['text']=='Research the offer' and len(message['references'])==2
            # Handoff prepares one pinned public result, without inference or transcript copying.
            before_jobs=set(app.jobs);before_chats=len(app.preferences['chats'])
            draft=call('/api/chats/handoff?business='+bid+'&id='+job['chat_id'])
            assert set(app.jobs)==before_jobs and len(app.preferences['chats'])==before_chats
            assert len(draft['references'])==1 and not draft['text'] and draft['goal_id']==goal['id']
            pinned=context.resolve(app,bid,draft['references']);assert 'Saved useful progress' in pinned['text'] and 'Research the offer' not in pinned['text']
            handoff_path=app.chat_display_path(job['chat_id']);saved_bytes=handoff_path.read_bytes()
            try:
                changed=json.loads(saved_bytes);changed[-1]['text']='A different reply';handoff_path.write_text(json.dumps(changed),encoding='utf-8')
                try:context.resolve(app,bid,draft['references']);raise AssertionError('Stale handoff reused changed content')
                except ValueError:pass
            finally:handoff_path.write_bytes(saved_bytes)
            try:context.handoff(app,'another-business',job['chat_id']);raise AssertionError('Cross-business handoff accepted')
            except ValueError:pass
            # Native image bytes stay in one scoped file, not in job or chat JSON.
            import base64
            from workspace_native_requests import save_image
            image={'type':'image','mimeType':'image/png','data':base64.b64encode(b'\x89PNG\r\n\x1a\nfixture').decode()}
            media=save_image(image,bid);assert media==save_image(image,bid) and (root/media['path']).is_file()
            assert 'data' not in media
            try:save_image({**image,'data':base64.b64encode(b'<script>bad</script>').decode()},bid);raise AssertionError('Non-image output saved as an image')
            except ValueError:pass
            reused=call('/api/context/message',{'business':bid,'chat_id':job['chat_id'],'index':0,'digest':context.message_key(message)})
            assert reused['text']=='Research the offer' and reused['goal_id']==goal['id'] and reused['new_chat_goal_id']==goal['id']
            call('/api/context/message',{'business':bid,'chat_id':job['chat_id'],'index':0,'digest':'stale'},400)
            call('/api/chat',{'business':bid,'chat_id':job['chat_id'],'text':'Bad context','references':42},400)
            overview=call('/api/goals?business='+bid+'&id='+goal['id']);assert overview['chats'][0]['id']==job['chat_id']
            assert overview['goal']['status']=='active','A completed turn must not complete its goal'
            command=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_goals.py'),'link-chat','--workspace',str(root),'--business-id',bid,'--chat',job['chat_id'],'--id',goal['id'],'--url',f'http://127.0.0.1:{server.server_port}','--json'],capture_output=True,text=True,check=True)
            assert json.loads(command.stdout)['chats'][0]['goal_id']==goal['id']
            from remember import remember
            asset=remember(bid,{'objects':[{'object_type':'Asset','content':{'asset_type':'text','business_role':'Research','version':'1','status':'active','location_reference':file.relative_to(root).as_posix(),'extensions':{'custom':{'keep':True}}}}]})['objects'][0]['id']
            call('/api/goals',{'business':bid,'action':'link_asset','goal_id':goal['id'],'asset_id':asset})
            call('/api/goals',{'business':bid,'action':'link_asset','goal_id':'','asset_id':asset})
            from workspace_ui import records
            saved_asset=next(r['data'] for r in records(bid)[0] if r['ref']==asset)
            assert saved_asset['extensions']['custom']['keep'] and not saved_asset['extensions']['businessos'].get('goal_ref')
            # Result selection pins a particular public reply, even when the same chat does new work.
            selected=context.inventory(app,bid,'Research','result')['items'][0]
            activity.record(bid,{'id':'later-turn','chat_id':job['chat_id'],'agent':'Fixture','status':'complete'},{'title':'Different work','agent':'configured'})
            pinned=context.resolve(app,bid,[selected]);assert 'Saved useful progress' in pinned['text']
            # Matching native message IDs retain the original receipt after history refresh.
            restored=[{'role':'user','text':message['text'],'request_id':job['id']},{'role':'assistant','text':'Saved useful progress'}]
            context.retain_receipts(restored,shown['messages']);assert restored[0]['references']==message['references'] and restored[1]['request_id']==job['id']
            saved_media=[{'role':'user','text':'Show the result','request_id':'image-turn'},{'role':'assistant','text':'Image ready.','request_id':'image-turn','native_media':[media]}]
            replay=[{'role':'user','text':'Show the result','request_id':'image-turn'},{'role':'assistant','text':'Image ready.'}]
            context.retain_receipts(replay,saved_media);assert replay[-1]['native_media']==[media]
            replay[-1]['native_media']=[{**media,'path':'new-native-image.png'}];context.retain_receipts(replay,saved_media)
            assert replay[-1]['native_media'][0]['path']=='new-native-image.png','Fresh native output must take precedence over a saved image'
            replay[-1]={'role':'assistant','text':'A changed result'};context.retain_receipts(replay,saved_media)
            assert not replay[-1].get('native_media'),'An old image was attached to a different native reply'
            # Old objectives remain workspace goals; chat efforts are explicitly scoped.
            legacy=remember(bid,{'objects':[{'object_type':'Objective','content':{'name':'Existing business objective','status':'active'}}]})['objects'][0]['id']
            assert goals.scope(goals.find(bid,legacy))=='workspace' and not goals.metadata(goals.find(bid,legacy))
            local=call('/api/goals',{'business':bid,'action':'save','name':'Finish the proposal','scope':'chat','chat_id':job['chat_id'],'workspace_goal_id':goal['id']})['goal']
            assert goals.scope(local)=='chat'
            assert local['id'] not in {g['id'] for g in call('/api/goals?business='+bid)['items']}
            assert not context.inventory(app,bid,'Finish the proposal','goal')['items'],'Chat goals must not appear in workspace reuse choices'
            call('/api/goals',{'business':bid,'action':'link_chat','chat_id':job['chat_id'],'goal_id':local['id']})
            combined=context.resolve(app,bid,[],local['id'])
            assert {r['id'] for r in combined['references']}=={local['id'],goal['id']} and combined['text'].count('Goal context:')==2
            local_message={'role':'user','text':'Continue the proposal','goal_id':local['id'],'references':combined['references']}
            history_path=app.chat_display_path(job['chat_id']);history_bytes=history_path.read_bytes()
            try:
                history_path.write_text(json.dumps([local_message]),encoding='utf-8')
                reuse_local=context.reusable(app,bid,job['chat_id'],0)
                assert reuse_local['new_chat_goal_id']==goal['id'] and not reuse_local['references'],'Reusing a prompt must transfer only its shared goal, without duplicating goal receipts'
                goals.remove(bid,local['id'])
                assert context.reusable(app,bid,job['chat_id'],0)['new_chat_goal_id']=='','A deleted effort must not silently transfer its goal connection'
                goals.remove(bid,local['id'],restore=True)
            finally:history_path.write_bytes(history_bytes)
            policy={'mode':'native','until':time.time()+600};old_basis=goals.continuation_basis(bid,local)
            selected_chat=next(c for c in app.preferences['chats'] if c['id']==job['chat_id']);selected_chat['continuation']=dict(policy)
            call('/api/goals',{'business':bid,'action':'save','id':goal['id'],'status':'paused'})
            assert 'continuation' not in selected_chat and goals.guard(bid,local['id'],old_basis,policy)
            call('/api/goals',{'business':bid,'action':'save','id':goal['id'],'status':'active'})
            assert goals.guard(bid,local['id'],old_basis,policy),'Reopening a goal must not restore old continuation approval'
            call('/api/goals',{'business':bid,'action':'save','id':local['id'],'status':'completed'})
            assert goals.find(bid,goal['id'])['status']=='active','Completing an effort must not complete its workspace outcome'
            assert local['id'] in {g['id'] for g in call('/api/goals?business='+bid+'&scope=chat&show=completed')['items']}
            # Lifecycle/assignment changes do not imply that a linked artifact is wrong.
            from correction_impacts import correction_event
            before=goals.find(bid,local['id'])
            with patch('correction_impacts.inbound_references',return_value=[{'object_type':'Asset','object_ref':asset}]):
                assert correction_event(bid,before,{**before,'status':'paused','extensions':{'businessos':{'goal':{'scope':'chat','revision':999}}}},None,'event', 'now') is None
                assert correction_event(bid,before,{**before,'target':'A materially different outcome'},None,'event','now'),'An actual outcome correction must still surface possible review impacts'
            overview=call('/api/goals?business='+bid+'&id='+goal['id'])
            assert overview['chat_goals'][0]['id']==local['id'] and overview['chat_goals'][0]['status']=='completed'
            history=call('/api/goals?business='+bid+'&scope=all&show=all&chat_id='+job['chat_id'])
            assert {local['id'],goal['id']} <= {g['id'] for g in history['items']},'Chat history must include the shared goal actually used by the chat'
            history_cli=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_goals.py'),'list','--workspace',str(root),'--business-id',bid,'--chat',job['chat_id'],'--scope','all','--show','all','--url',f'http://127.0.0.1:{server.server_port}','--json'],capture_output=True,text=True,check=True)
            assert {g['id'] for g in json.loads(history_cli.stdout)['items']}=={g['id'] for g in history['items']},'CLI history must read the same goal relationships as the UI'
            # Compatible older interfaces use the same lifecycle, not a second save path.
            selected_chat['continuation']=dict(policy)
            stale=overview['goal_basis']
            renamed=call('/api/save',{'business':bid,'kind':'goal','ref':goal['id'],'name':'Research the offer together'})
            assert renamed['objects'][0]['id']==goal['id'] and 'continuation' not in selected_chat
            call('/api/goals',{'business':bid,'action':'save','id':goal['id'],'name':'Stale overwrite','basis':stale},400)
            assert goals.find(bid,goal['id'])['name']=='Research the offer together'
            # UI, CLI entry and generated knowledge agree about ordinary goal context.
            from _common import object_index
            import enter
            from generate_knowledge_layer import generate
            paused=goals.save(bid,{'name':'Paused shared outcome','status':'paused'})
            gone=goals.save(bid,{'name':'Deleted shared outcome'});goals.remove(bid,gone['id'])
            index=object_index(bid)
            baseline={r['object_ref'] for r in enter._baseline_context(bid,index=index)}
            assert goal['id'] in baseline and not {local['id'],paused['id'],gone['id']}&baseline
            assert local['id'] not in {r['object_ref'] for r in enter._saved_work_candidates('Finish the proposal',index)}
            generate(bid);priorities=(root/'knowledge'/bid/'_generated'/'Priorities.md').read_text(encoding='utf-8')
            assert 'Research the offer together' in priorities and not any(name in priorities for name in ('Finish the proposal','Paused shared outcome','Deleted shared outcome'))
            # An unsent goal binds once to the first real chat and retains a correct receipt.
            draft_goal=call('/api/goals',{'business':bid,'action':'save','name':'An independent effort','scope':'chat'})['goal']
            draft_job=call('/api/chat',{'business':bid,'chat_id':'','text':'Do this effort','goal_id':draft_goal['id']},202)
            wait(lambda:app.jobs[draft_job['id']]['status']!='working')
            bound=goals.find(bid,draft_goal['id']);assert goals.metadata(bound)['chat_id']==draft_job['chat_id']
            receipt=app.jobs[draft_job['id']]['references'][0];assert receipt['revision']==context.digest(bound)
            call('/api/goals',{'business':bid,'action':'link_chat','chat_id':draft_job['chat_id'],'goal_id':local['id']},400)
            jobs_before=len(app.jobs)
            call('/api/chat',{'business':bid,'chat_id':draft_job['chat_id'],'text':'Wrong effort','goal_id':local['id']},400)
            assert len(app.jobs)==jobs_before,'A foreign chat goal must be rejected before execution'
            # Removing a link keeps the earlier effort discoverable; deletion is recoverable.
            call('/api/goals',{'business':bid,'action':'link_chat','chat_id':job['chat_id'],'goal_id':goal['id']})
            assert job['chat_id'] in {c['id'] for c in call('/api/goals?business='+bid+'&id='+local['id'])['chats']}
            display_before=app.chat_display_path(job['chat_id']).read_bytes()
            call('/api/goals',{'business':bid,'action':'delete','id':goal['id']})
            call('/api/save',{'business':bid,'kind':'goal','ref':goal['id'],'name':'Cannot resurrect deleted goals'},400)
            assert selected_chat['goal_id']=='' and file.is_file() and app.chat_display_path(job['chat_id']).read_bytes()==display_before
            assert goal['id'] in {g['id'] for g in call('/api/goals?business='+bid+'&show=deleted')['items']}
            assert goals.review_reason(bid,local['id']),'Deleted connected goals must block automatic continuation'
            check=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_goals.py'),'check','--workspace',str(root),'--business-id',bid,'--id',goal['id'],'--json'],capture_output=True,text=True,check=True)
            assert not json.loads(check.stdout)['eligible']
            restored_goal=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_goals.py'),'restore','--workspace',str(root),'--business-id',bid,'--id',goal['id'],'--url',f'http://127.0.0.1:{server.server_port}','--json'],capture_output=True,text=True,check=True)
            assert not json.loads(restored_goal.stdout)['deleted'] and not goals.deleted(goals.find(bid,goal['id']))
            assert not selected_chat.get('continuation') and job['chat_id'] in {c['id'] for c in call('/api/goals?business='+bid+'&id='+goal['id'])['chats']}
            file.unlink();call('/api/context/resolve',{'business':bid,'references':refs},400)
            call('/api/goals',{'business':bid,'action':'continuation','chat_id':job['chat_id'],'mode':'native','until':time.time()+3600},400)
            result=call('/api/goals',{'business':bid,'action':'save','id':goal['id'],'status':'paused'})
            assert result['goal']['status']=='paused'
            assert goals.guard(bid,goal['id'],goals.fingerprint(goal),{'mode':'native','until':time.time()+3600})
            with urlopen(f'http://127.0.0.1:{server.server_port}/workspace-compose.js') as response:assert response.status==200
        finally:server.shutdown();server.server_close()
        # Goal/task links require confirmed native instructions, and can be removed.
        native=[]
        def create_task(data,*args):
            task=dict(data,id='hermes:goal-task',native_id='goal-task',owner='hermes',status='active')
            native.append(task);return task
        def change_task(*args):
            payload=app.schedule_job['payload'];old=native[0]
            native[0]={**old,'description':'Native task without a goal' if payload.get('remove_goal') else old['description']+'\nUpdated unrelated setting'}
            return {'reply':json.dumps({'state':'saved','native_id':'goal-task'}),'native_id':'manage-session'}
        app.preferences.setdefault('connected_apps',{})['hermes']={'model':'test:model'}
        with patch('workspace_ui.installed_agents',return_value=[{'id':'hermes','name':'Fixture','argv':['fixture','chat']}]), \
             patch.object(app,'agent_options',return_value={'models':[{'id':'test:model'}]}), \
             patch.object(app,'agent_efforts',return_value={'efforts':[]}), \
             patch.object(schedules,'inventory',side_effect=lambda **kwargs:{'items':list(native)}), \
             patch.object(schedules,'create',side_effect=create_task),patch.object(agents,'run',side_effect=change_task):
            app.schedule_action(bid,{'action':'create','app':'hermes','name':'Goal review','description':'Review saved research.','when':'every 1h','model':'test:model','goal_id':goal['id']})
            wait(lambda:app.schedule_job['status']!='working');assert app.schedule_job['status']=='complete',app.schedule_job
            assert app.preferences['goal_tasks'][bid]['hermes:goal-task']==goal['id']
            assert '[Aura goal]' in native[0]['description'] and '--basis' in native[0]['description']
            app.schedule_action(bid,{'action':'request','id':'hermes:goal-task','goal_id':'','remove_goal':True,'request':'Unlink goal'})
            wait(lambda:app.schedule_job['status']!='working');assert app.schedule_job['status']=='complete',app.schedule_job
            assert not app.preferences['goal_tasks'][bid]
            # A native reply that changes something unrelated must not create a goal link.
            app.schedule_action(bid,{'action':'request','id':'hermes:goal-task','goal_id':goal['id'],'request':'Link goal'})
            wait(lambda:app.schedule_job['status']!='working');assert app.schedule_job['status']=='error'
            assert not app.preferences['goal_tasks'][bid]
        # Exercise real RPC streams. Aura never toggles native shared retry settings
        # and never sends a second prompt to continue the assignment.
        goals.save(bid,{'id':goal['id'],'status':'active'});goal=goals.find(bid,goal['id']);script=base/'retry.py';script.write_text(RETRY,encoding='utf-8')
        for mode in ('manual','native','changed'):
            execution=Execution();execution.interactive=True;execution.continuation={'mode':'native' if mode!='manual' else 'manual','until':time.time()+10}
            basis=goals.fingerprint(goal);execution.continuation_guard=lambda:goals.guard(bid,goal['id'],basis,execution.continuation)
            execution.claim_continuation=lambda:'';execution.release_continuation=lambda:None;updates=[];execution.continuation_changed=updates.append
            outcome={}
            def run():
                try:outcome.update(agents.run([sys.executable,'-u',str(script),'--print'],'pi',root,dict(os.environ),'Continue the remaining assignment',None,'fixture','',lambda **v:None,execution))
                except Exception as error:outcome['error']=error
            thread=threading.Thread(target=run);thread.start()
            if mode=='changed':
                wait(lambda:any('retry_at' in u for u in updates));goals.save(bid,{'id':goal['id'],'status':'paused'})
            thread.join(8)
            if thread.is_alive():execution.stop();thread.join(3)
            assert not thread.is_alive()
            if mode=='native':assert outcome.get('reply')=='Finished remaining work.',outcome
            else:assert 'error' in outcome and any(u.get('continuation_note') for u in updates),outcome
        command=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_goals.py'),'check','--workspace',str(root),'--business-id',bid,'--id',goal['id'],'--json'],capture_output=True,text=True,check=True)
        assert json.loads(command.stdout)['eligible'] is False
        if shutil.which('node'):subprocess.run(['node',str(ROOT/'tests/workspace_compose_ui.cjs'),str(ROOT/'interface/workspace-compose.js')],check=True)
    # Random IDs can follow a command-line flag: new ones never start with "-", and chats made before
    # that (about 1 in 64) still work after --chat instead of failing as an unknown option.
    import argparse,secrets,_common
    draws=iter(['-Ab3dEf','Zx9_kLm'])
    with patch.object(secrets,'token_urlsafe',lambda n=None:next(draws)):assert _common.new_id()=='Zx9_kLm'
    assert not any(_common.new_id().startswith('-') for _ in range(2000))
    parser=argparse.ArgumentParser();commands=parser.add_subparsers(dest='command',required=True)
    link=commands.add_parser('link-chat');link.add_argument('--chat');link.add_argument('--id');link.add_argument('--json',action='store_true')
    parsed=_common.parse_args_with_ids(parser,['link-chat','--chat','-T8jrxB52-cwHyyj','--id','obj_1','--json'])
    assert parsed.chat=='-T8jrxB52-cwHyyj' and parsed.id=='obj_1' and parsed.json
    import contextlib,io
    try:
        with contextlib.redirect_stderr(io.StringIO()):_common.parse_args_with_ids(parser,['link-chat','--chat','--id','obj_1'])
        raise AssertionError('a missing --chat value was accepted')
    except SystemExit:pass
    with tempfile.TemporaryDirectory() as folder:
        result=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_goals.py'),'link-chat','--workspace',folder,'--business-id','none','--chat','-T8jrxB52-cwHyyj','--id','obj_none','--json'],capture_output=True,text=True)
        assert result.returncode!=2 and 'expected one argument' not in result.stderr,result.stderr
    print('Composer and goals passed: scoped references, exact message reuse, pinned results, receipt recovery, persistent goals, native retry boundaries and CLI/API parity.')


if __name__=='__main__':main()
