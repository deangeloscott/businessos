"""Boundary checks for native replies, scoped activity, and recoverable local files."""
from pathlib import Path
from unittest.mock import patch
import json
import os
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
        time.sleep(.01)
    raise AssertionError('Native fixture did not reach the expected state')


FIXTURE=r'''
import json,sys
def emit(v):print(json.dumps(v),flush=True)
kind=sys.argv[1];turns=0
for line in sys.stdin:
 m=json.loads(line);method=m.get('method');typ=m.get('type');ident=m.get('id')
 if kind=='codex':
  if method=='initialize':emit({'id':ident,'result':{}})
  elif method=='thread/start':
   assert m['params']['sandbox']=='workspace-write' and m['params']['approvalPolicy']=='on-request'
   emit({'id':ident,'result':{'thread':{'id':'native-one'},'approvalPolicy':'on-request','sandbox':{'type':'workspaceWrite'}}})
  elif method=='turn/start':
   turns+=1;assert turns==1
   emit({'id':ident,'result':{'turn':{'id':'turn-one'}}})
   emit({'id':41,'method':'item/commandExecution/requestApproval','params':{'threadId':'native-one','turnId':'turn-one','command':'echo useful','availableDecisions':['accept','decline']}})
  elif ident==41:
   assert m['result']=={'decision':'accept'}
   emit({'method':'serverRequest/resolved','params':{'requestId':41,'threadId':'native-one'}})
   emit({'id':43,'method':'item/tool/requestUserInput','params':{'threadId':'native-one','questions':[{'id':'stale','question':'Expired?'}]}})
   emit({'method':'serverRequest/resolved','params':{'requestId':43,'threadId':'native-one'}})
   emit({'id':42,'method':'item/tool/requestUserInput','params':{'threadId':'native-one','questions':[{'id':'direction','question':'Which way?','options':[{'label':'North','description':'Go north'},{'label':'South','description':'Go south'}],'isOther':True}]}})
  elif ident==42:
   assert m['result']=={'answers':{'direction':{'answers':['North']}}}
   emit({'method':'thread/tokenUsage/updated','params':{'threadId':'native-one','tokenUsage':{'last':{'inputTokens':8,'outputTokens':3,'cachedInputTokens':2},'total':{'inputTokens':108,'outputTokens':13,'cachedInputTokens':22}}}})
   emit({'method':'thread/tokenUsage/updated','params':{'threadId':'native-one','tokenUsage':{'last':{'inputTokens':2,'outputTokens':1,'cachedInputTokens':0},'total':{'inputTokens':110,'outputTokens':14,'cachedInputTokens':22}}}})
   emit({'method':'item/completed','params':{'threadId':'native-one','item':{'id':'reply','type':'agentMessage','phase':'final_answer','text':'Finished north.'}}})
   emit({'method':'turn/completed','params':{'threadId':'native-one','turn':{'id':'turn-one','status':'completed'}}})
 elif kind in {'pi','omp'}:
  if typ=='get_state':emit({'type':'response','id':ident,'success':True,'data':{'sessionId':'native-pi','isStreaming':False}})
  elif typ=='prompt':
   turns+=1;assert turns==1
   emit({'type':'response','id':ident,'success':True})
   emit({'type':'extension_ui_request','id':'pick','method':'select','title':'Choose direction','options':['North','South']})
  elif typ=='extension_ui_response':
   assert ident=='pick' and m['value']=='North'
   emit({'type':'message_end','message':{'id':'reply','role':'assistant','content':[{'type':'text','text':'Finished north.'}],'usage':{'input':8,'output':3}}})
   emit({'type':'agent_settled'})
 elif kind=='claude':
  if typ=='control_request':emit({'type':'control_response','response':{'subtype':'success','request_id':m['request_id'],'response':{}}})
  elif typ=='user':
   turns+=1;assert turns==1
   emit({'type':'system','subtype':'init','session_id':'native-claude'})
   emit({'type':'control_request','request_id':'question','request':{'subtype':'can_use_tool','tool_name':'AskUserQuestion','input':{'questions':[{'question':'Which way?','options':[{'label':'North'},{'label':'South'}],'multiSelect':False}]}}})
  elif typ=='control_response':
   assert m['response']['response']['updatedInput']['answers']=={'Which way?':'North'}
   emit({'type':'result','session_id':'native-claude','result':'Finished north.','usage':{'input_tokens':8,'output_tokens':3}})
'''


def main():
    import workspace_activity as activity
    import workspace_history as history
    import workspace_permissions as permissions
    import workspace_codex as codex
    import workspace_agents as agents
    import workspace_documents as documents
    import workspace_storage as storage
    import workspace_assistants as assistants
    from workspace_execution import Execution,Stopped
    from workspace_interactions import Requests,answers_for,question
    from _common import workspace_scope,write_json_atomic
    from setup import setup
    from remember import remember
    with tempfile.TemporaryDirectory(prefix='aura-coordination-') as temp,patch.dict(os.environ):
        base=Path(temp);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        bid=setup(organization='Continuity studio')['business_id']
        file=root/'attachments'/bid/'work'/'notes.txt';file.parent.mkdir(parents=True,exist_ok=True);file.write_text('Earlier text',encoding='utf-8')
        history.capture(file,bid);file.write_text('Newer text',encoding='utf-8')
        old=history.inventory(bid,file)['items'][0];review=history.version(bid,old['id'])
        file.write_text('Outside change',encoding='utf-8')
        try:history.restore(bid,old['id'],review['current_revision']);raise AssertionError('Newer edits were overwritten')
        except documents.Conflict:pass
        history.restore(bid,old['id'],documents.revision(file));assert file.read_text()=='Earlier text'
        assert any(r['reason']=='Before restore' for r in history.inventory(bid,file)['items'])
        file.unlink();history.restore(bid,old['id'],'missing');assert file.read_text()=='Earlier text'
        for unsafe in (root/'attachments'/bid/'secrets'/'key.txt',root/'attachments'/bid/'work'/'.env',base/'outside.txt'):
            try:history.capture(unsafe,bid,content=b'private');raise AssertionError('Private/outside file captured')
            except ValueError:pass
        with patch.object(history,'MAX_VERSIONS',2):
            for value in range(4):history.capture(file,bid,content=str(value).encode())
            assert len(history.inventory(bid,file)['items'])==2
        business=root/'instances'/bid/'context/business.json';original=json.loads(business.read_text())
        remember(bid,{'objects':[{'object_ref':original['id'],'content':{'name':'Changed studio'}}]})
        prior=next(r for r in history.inventory(bid,business)['items'] if json.loads((history.store(bid)/(r['hash']+'.bin')).read_bytes()).get('name')==original['name'])
        history.restore(bid,prior['id'],documents.revision(business));assert json.loads(business.read_text())['name']==original['name']
        # Restoring semantic extensions replaces the saved object, while ordinary
        # memory updates continue to merge independent custom fields.
        remember(bid,{'objects':[{'object_ref':original['id'],'content':{'extensions':{'custom_saved':{'value':'before'},'businessos':{'custom_saved':'before'}}}}]})
        saved_record=json.loads(business.read_text());saved_version=history.capture(business,bid)
        remember(bid,{'objects':[{'object_ref':original['id'],'content':{'extensions':{'custom_later':'after','businessos':{'custom_later':'after'}}}}]})
        assert 'custom_saved' in json.loads(business.read_text())['extensions']
        history.restore(bid,saved_version['id'],documents.revision(business))
        assert json.loads(business.read_text())['extensions']==saved_record['extensions']
        try:remember(bid,{'objects':[{'object_ref':original['id'],'content':{'name':'Invalid'},'replace_extensions':True}]});raise AssertionError('Ambiguous extension replacement accepted')
        except ValueError:pass
        # A storage failure after the file commits is a successful restore with
        # a warning. A failure to retain its current bytes must prevent the write.
        failure_file=file.parent/'restore-failure.txt';failure_file.write_text('saved');saved=history.capture(failure_file,bid);failure_file.write_text('current')
        real_capture=history.capture
        for failing_reason in ('Before restore','Restored version'):
            def fail_capture(*args,**kwargs):
                if len(args)>2 and args[2]==failing_reason:raise OSError('simulated recovery-storage failure')
                return real_capture(*args,**kwargs)
            with patch.object(history,'capture',side_effect=fail_capture):
                if failing_reason=='Before restore':
                    try:history.restore(bid,saved['id'],documents.revision(failure_file));raise AssertionError('Restored without preserving current bytes')
                    except OSError:assert failure_file.read_text()=='current'
                else:
                    restored=history.restore(bid,saved['id'],documents.revision(failure_file))
                    assert restored['restored'] and restored['warning'] and failure_file.read_text()=='saved'
                    assert restored['revision']==documents.revision(failure_file)
        with workspace_scope(base/'scale'),patch.object(history,'MAX_ENTRIES',5):
            folder=base/'scale'/'attachments'/bid/'work';folder.mkdir(parents=True)
            for i in range(40):(folder/f'item-{i}.txt').write_text(f'unchanged {i}')
            with patch.object(history,'_write',wraps=history._write) as writes:
                history.observe(bid)
                assert sum(call.args[0].name=='index.json' for call in writes.call_args_list)==1
            assert len(history.inventory(bid)['items'])==5
            with patch.object(history,'_write',wraps=history._write) as writes,patch.object(history,'_prepare',wraps=history._prepare) as reads:
                history.observe(bid);assert writes.call_count==0 and reads.call_count==0,'Unchanged files must not churn after versions expire'
                changed=folder/'item-0.txt';changed.write_text('new content')
                history.observe(bid);assert reads.call_count==1
                assert history.inventory(bid,changed)['items'][0]['hash']==__import__('hashlib').sha256(b'new content').hexdigest()
        activity.record(bid,{'id':'j','chat_id':'c','agent':'Pi','status':'working','updated':time.time()},{'title':'Research','agent':'pi'})
        assert activity.inventory(bid)['total']==1 and activity.inventory(bid,exclude_chat='c')['total']==0
        with workspace_scope(base/'other'):assert activity.inventory(bid)['total']==0
        pending_job={'id':'j','chat_id':'c','agent':'Pi','business_id':bid,'workspace':str(root),'status':'working','requests':[{'status':'pending'}]}
        activity.record(bid,pending_job,{'title':'Research','agent':'pi'})
        stale=activity.inventory(bid)['items'][0]
        assert stale['last_needs_input'] and not stale['needs_input']
        assert stale['progress']=='Previously needed input. Check the native chat for its outcome.'
        assert activity.inventory(bid,live_jobs=[pending_job])['items'][0]['needs_input']
        assert not activity.inventory(bid,live_jobs=[{**pending_job,'id':'different-turn'}])['items'][0]['needs_input']
        # A known result can fall outside the list's display limit while its
        # reference is still retained. Direct retrieval must not apply that limit.
        for i in range(101):activity.record(bid,{'id':f'old-{i}','chat_id':f'old-{i}','agent':'Pi','status':'working' if i<2 else 'complete'},{'title':f'Work {i}','agent':'pi'})
        folder=__import__('hashlib').sha256(str(root.resolve()).encode()).hexdigest()[:20]
        display=base/'state'/'chat-views'/folder/'c.json';write_json_atomic(display,[{'role':'assistant','request_id':'j','text':'Retained result'}])
        assert not any(r['chat_id']=='c' for r in activity.inventory(bid,limit=100)['items'])
        assert activity.result(bid,'c')['text']=='Retained result'
        assert permissions.arguments('claude','dontAsk')==['--permission-mode','dontAsk']
        try:permissions.arguments('pi','full');raise AssertionError('Invented Pi permission mode')
        except ValueError:pass
        for key in ('permission_mode','pending_requests','credentials'):
            try:assistants.validate({bid:[{'id':'a','name':'Jeff',key:'unsafe'}]});raise AssertionError('Portable permission accepted')
            except ValueError:pass
        root.joinpath('.businessos').mkdir(exist_ok=True)
        write_json_atomic(root/'.businessos/view.json',{'format':1,'harness_permissions':{'codex':'full'}})
        assert 'harness_permissions' not in storage.view_preferences(root)
        sent=[];broker=Requests();q=question('q','Pick',['One','Two'])
        ident=broker.add('native','Pick',[q],sent.append,lambda a:answers_for([q],a));barrier=threading.Barrier(3);results=[]
        def answer():
            barrier.wait()
            try:broker.answer(ident,{'q':['One']});results.append('sent')
            except ValueError:results.append('expired')
        threads=[threading.Thread(target=answer) for _ in range(2)]
        for t in threads:t.start()
        barrier.wait()
        for t in threads:t.join()
        assert results.count('sent')==1 and len(sent)==1
        ended=broker.add('cancelled','Gone',[q],sent.append,lambda a:a);broker.resolve('cancelled')
        try:broker.answer(ended,{'q':['One']});raise AssertionError('Cancelled request answered')
        except ValueError:pass
        script=base/'native.py';script.write_text(FIXTURE,encoding='utf-8')
        for kind in ('codex','pi','omp','claude'):
            execution=Execution();execution.interactive=True;execution.permission='workspace-write' if kind=='codex' else 'native'
            outcome={};updates=[]
            def run():
                try:
                    command=[sys.executable,'-u',str(script),kind,'exec' if kind=='codex' else '--print']
                    outcome.update(codex.run(command,root,'Work here',None,'test-model','medium',lambda **v:updates.append(v),dict(os.environ),execution) if kind=='codex' else agents.run(command,kind,root,dict(os.environ),'Work here',None,'test-model','',lambda **v:updates.append(v),execution))
                except Exception as e:outcome['error']=e
            thread=threading.Thread(target=run);thread.start();seen=set()
            deadline=time.monotonic()+10
            while thread.is_alive() and time.monotonic()<deadline:
                for row in execution.requests.snapshot():
                    if row['id'] in seen or row['status']!='pending':continue
                    seen.add(row['id'])
                    if row['native_id']==43:continue
                    answers={q['id']:['Approve once' if q['id']=='decision' else 'North'] for q in row['questions']}
                    execution.requests.answer(row['id'],answers)
                time.sleep(.01)
            if thread.is_alive():execution.stop();thread.join(5)
            assert not thread.is_alive() and 'error' not in outcome,(kind,outcome)
            assert outcome['reply']=='Finished north.' and outcome['usage']['input_tokens']==(10 if kind=='codex' else 8),(kind,outcome)
            assert all(r['status']!='pending' for r in execution.requests.snapshot())
            if kind=='codex':assert any(r['native_id']==43 and r['status']=='expired' for r in execution.requests.snapshot())
        execution=Execution();execution.interactive=True;execution.permission='workspace-write';errors=[]
        def stopping():
            try:codex.run([sys.executable,'-u',str(script),'codex','exec'],root,'Work',None,'model','medium',lambda **v:None,dict(os.environ),execution)
            except Exception as e:errors.append(e)
        thread=threading.Thread(target=stopping);thread.start();wait(lambda:execution.requests.snapshot());execution.stop();thread.join(5)
        assert not thread.is_alive() and errors and all(r['status']=='expired' for r in execution.requests.snapshot())
        # Exercise the real HTTP ownership boundary while a native process waits.
        from http.server import ThreadingHTTPServer
        from urllib.request import Request,urlopen
        from urllib.error import HTTPError
        from workspace_ui import Workspace,handler_for
        app=Workspace(agent={'name':'Codex fixture','argv':[sys.executable,'-u',str(script),'codex','exec']},settings_file=history.store(bid).parents[2]/'fixture-prefs.json')
        app.connection_kind='codex';app.preferences['connection']={'kind':'codex','model':'test-model','effort':'medium'}
        app.preferences['harness_permissions']={'codex':'workspace-write'}
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));threading.Thread(target=server.serve_forever,daemon=True).start()
        def call(path,data=None,expected=200):
            request=Request(f'http://127.0.0.1:{server.server_port}'+path,data=json.dumps(data).encode() if data is not None else None,
                headers={'Content-Type':'application/json','X-Aura-Token':app.token,'X-Aura-Workspace':str(root)})
            try:
                with urlopen(request,timeout=10) as response:code=response.status;value=json.load(response)
            except HTTPError as error:code=error.code;value=json.load(error)
            assert code==expected,(path,code,value);return value
        try:
            for name in ('workspace-continuity.js','file-editor.js'):
                with urlopen(f'http://127.0.0.1:{server.server_port}/'+name,timeout=5) as response:
                    assert response.status==200 and len(response.read())>100
            launched=call('/api/chat',{'business':bid,'chat_id':'','text':'Continue north'},202)
            wait(lambda:any(r['status']=='pending' for r in app.jobs[launched['id']].get('requests',[])))
            job=call('/api/chat?business='+bid+'&id='+launched['id']);pending=next(r for r in job['requests'] if r['status']=='pending')
            payload={'business':bid,'job_id':job['id'],'chat_id':job['chat_id'],'id':pending['id'],'answers':{'decision':['Approve once']}}
            call('/api/chat/answer',{**payload,'chat_id':'different-chat'},400)
            call('/api/chat/answer',payload);call('/api/chat/answer',payload,400)
            wait(lambda:any(r['native_id']==42 and r['status']=='pending' for r in app.jobs[job['id']].get('requests',[])))
            request=next(r for r in app.jobs[job['id']]['requests'] if r['native_id']==42)
            call('/api/chat/answer',{**payload,'id':request['id'],'answers':{'direction':['North']}})
            wait(lambda:app.jobs[job['id']]['status']=='complete')
            assert call('/api/permissions?business='+bid+'&chat_id='+job['chat_id'])['last_effective']['approvalPolicy']=='on-request'
            assert call('/api/activity?business='+bid)['items'][0]['chat_id']==job['chat_id']
            before=call('/api/history?business='+bid)
            assert before['items'] and '/api/chat/answer' not in json.dumps(before)
        finally:server.shutdown();server.server_close()
        check=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_activity.py'),'--business-id',bid,'--search','Research','--json'],capture_output=True,text=True,check=True)
        assert any(r['chat_id']=='c' for r in json.loads(check.stdout)['items'])
        import shutil
        if shutil.which('node'):
            subprocess.run(['node',str(ROOT/'tests/workspace_continuity_ui.cjs'),str(ROOT/'interface/workspace-continuity.js')],check=True)
    print('Coordination passed: same-process native replies, exactly-once/cancel safety, scoped activity, private package boundaries, guarded recovery and CLI parity.')


if __name__=='__main__':main()
