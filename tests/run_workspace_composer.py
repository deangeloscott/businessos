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
            reused=call('/api/context/message',{'business':bid,'chat_id':job['chat_id'],'index':0,'digest':context.message_key(message)})
            assert reused['text']=='Research the offer' and reused['goal_id']==goal['id']
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
    print('Composer and goals passed: scoped references, exact message reuse, pinned results, receipt recovery, persistent goals, native retry boundaries and CLI/API parity.')


if __name__=='__main__':main()
