"""Regression proofs for demonstrated native transport failures; no model calls."""
from pathlib import Path
import json,os,sys,tempfile,threading,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

FIXTURE=r'''
import json,sys,threading,time,os
from pathlib import Path
kind=sys.argv[1];release=Path(sys.argv[2]);background=True
if kind=='claude':
 assert sys.argv[sys.argv.index('--agent')+1]=='jeff'
 assert os.environ['CLAUDE_CODE_SUBAGENT_MODEL']=='child-default'
if kind=='omp':
 assert json.loads(Path(sys.argv[sys.argv.index('--config')+1]).read_text())=={'modelRoles':{'task':'child-default'}}
output_lock=threading.Lock()
def emit(value):
 with output_lock:print(json.dumps(value),flush=True)
for line in sys.stdin:
 m=json.loads(line);method=m.get('method');typ=m.get('type');ident=m.get('id')
 if kind.startswith('codex'):
  if method=='initialize':emit({'id':ident,'result':{}})
  elif method=='thread/start':
   if m['params'].get('config',{}).get('agents.default_subagent_model'):
    assert m['params']['config']=={'model_verbosity':'low','agents.default_subagent_model':'child-default'}
   emit({'id':ident,'result':{'thread':{'id':'parent'}}})
  elif method=='thread/resume':emit({'id':ident,'result':{'thread':{'id':m['params']['threadId']}}})
  elif method in {'review/start','thread/compact/start'}:
   assert (kind=='codex-review')==(method=='review/start')
   emit({'id':ident,'result':{}})
   item={'id':'result','type':'exitedReviewMode','review':'Native review complete.'} if method=='review/start' else {'id':'result','type':'contextCompaction'}
   emit({'method':'item/completed','params':{'threadId':'parent','item':item}})
   emit({'method':'turn/completed','params':{'threadId':'parent','turn':{'id':'turn','status':'completed'}}})
  elif method=='turn/start':
   emit({'id':ident,'result':{'turn':{'id':'turn'}}})
   emit({'method':'thread/started','params':{'thread':{'id':'child','parentThreadId':'parent'}}})
   emit({'method':'item/started','params':{'threadId':'parent','item':{'id':'new-delegate','type':'subAgentActivity','kind':'started','agentThreadId':'child','agentPath':'/root/research','model':'native-worker'}}})
   emit({'method':'item/started','params':{'threadId':'parent','item':{'id':'delegate','type':'collabAgentToolCall','receiverThreadIds':['child'],'agentsStates':{'child':{'status':'running'}}}}})
   emit({'method':'item/completed','params':{'threadId':'parent','item':{'id':'reply','type':'agentMessage','phase':'final_answer','text':'x'*100123}}})
   emit({'method':'turn/completed','params':{'threadId':'parent','turn':{'id':'turn','status':'completed'}}})
   emit({'id':'child-approval','method':'item/commandExecution/requestApproval','params':{'threadId':'child','reason':'Child needs access','availableDecisions':['accept','acceptForSession','decline']}})
  elif ident=='child-approval':
   assert m['result']=={'decision':'acceptForSession'}
   emit({'method':'turn/completed','params':{'threadId':'child','turn':{'id':'child-turn','status':'completed'}}})
   emit({'method':'item/completed','params':{'threadId':'parent','item':{'id':'new-complete','type':'subAgentActivity','kind':'completed','agentThreadId':'child','agentPath':'/root/research'}}})
   def finish():
    while not release.exists():time.sleep(.01)
    emit({'method':'item/completed','params':{'threadId':'parent','item':{'id':'bg','type':'commandExecution','status':'completed'}}})
   threading.Thread(target=finish,daemon=True).start()
  elif method=='thread/backgroundTerminals/list':emit({'id':ident,'result':{'data':[] if kind!='codex' or release.exists() else [{'processId':'background','itemId':'bg','command':'work','cwd':'.'}]}})
 elif kind=='claude':
  if typ=='control_request':emit({'type':'control_response','response':{'subtype':'success','request_id':m['request_id'],'response':{}}})
  elif typ=='user':
   emit({'type':'system','subtype':'init','session_id':'parent'})
   emit({'type':'system','subtype':'session_state_changed','state':'running'})
   emit({'type':'system','subtype':'task_started','task_id':'child','task_type':'background_shell','description':'Native background task'})
   emit({'type':'result','session_id':'parent','result':'Parent reply.'})
   emit({'type':'control_request','request_id':'approval','request':{'subtype':'can_use_tool','tool_name':'Bash','input':{'command':'work'},'permission_suggestions':[{'type':'addRules','destination':'session','rules':[]}]}})
  elif typ=='control_response':
   assert m['response']['response']['updatedPermissions'][0]['destination']=='session'
   emit({'type':'system','subtype':'task_notification','task_id':'child','status':'completed'})
   emit({'type':'result','session_id':'parent','result':'Child finished too.'})
   emit({'type':'system','subtype':'session_state_changed','state':'idle'})
 else:
  if typ=='get_state':emit({'type':'response','id':ident,'success':True,'data':{'sessionId':'native','isStreaming':False}})
  elif typ=='set_subagent_subscription':
   assert m['level']=='progress' and 'mode' not in m
   emit({'type':'response','id':ident,'success':True,'data':{'level':'progress'}})
  elif typ=='prompt':emit({'type':'extension_ui_request','method':'input','id':'secret','title':'Native key','secret':True})
  elif typ=='extension_ui_response':
   assert m['value']=='ephemeral-secret' and 'cancelled' not in m
   emit({'type':'extension_ui_request','method':'notify','id':'notice','message':'Native notice'})
   emit({'type':'extension_ui_request','method':'open_url','id':'url','launchUrl':'https://example.com/sign-in'})
   emit({'type':'extension_ui_request','method':'set_editor_text','id':'editor','text':'Prepared draft'})
   emit({'type':'message_end','message':{'role':'assistant','content':[{'type':'text','text':'Native complete.'}]}})
   emit({'type':'session_settled'})
'''

def wait(check):
    until=time.monotonic()+8
    while time.monotonic()<until:
        if check():return
        time.sleep(.01)
    raise AssertionError('Native interaction fixture timed out')

def main():
    from workspace_execution import Execution
    from workspace_interactions import question,answers_for
    from workspace_native_requests import codex_request,attachments,notice
    import workspace_codex,workspace_agents
    from workspace_ui import Workspace
    custom=Workspace.__new__(Workspace);custom.configured_agent={'connections':{'codex':{'native_options':{'thread':{'dynamicTools':[]}},'native_requests':{'argv':['native-provider']}}}}
    custom.select_agent({'id':'codex','name':'Native','argv':['native-client','exec','-']})
    assert custom.agent['native_options']['thread']=={'dynamicTools':[]} and custom.agent['native_requests']['argv']==['native-provider']
    custom.select_agent({'id':'configured','name':'Custom','argv':['native-client'],'native_protocol':'codex'})
    assert custom.agent['native_protocol']=='codex' and workspace_codex.base_command(custom.agent['argv'])==['native-client']
    assert workspace_agents.base_command(['another-native-client'])==['another-native-client']
    q=question('direction','Which direction?',['North']);assert q['text']=='Which direction?' and q['allow_text'] is False
    execution=Execution();sent=[]
    schema={'type':'object','properties':{'name':{'type':'string'},'enabled':{'type':'boolean'},'count':{'type':'integer'}},'required':['name']}
    codex_request({'id':1,'method':'mcpServer/elicitation/request','params':{'mode':'form','message':'Save preferences','requestedSchema':schema}},execution,sent.append)
    row=execution.requests.snapshot()[-1]
    execution.requests.answer(row['id'],{'action':['Submit'],json.dumps(('name',)):['Studio'],json.dumps(('enabled',)):['Yes'],json.dumps(('count',)):['3']})
    assert sent[-1]['result']=={'action':'accept','content':{'name':'Studio','enabled':True,'count':3}}
    codex_request({'id':2,'method':'mcpServer/elicitation/request','params':{'mode':'form','requestedSchema':schema}},execution,sent.append)
    row=execution.requests.snapshot()[-1];execution.requests.answer(row['id'],{'action':['Decline']});assert sent[-1]['result']=={'action':'decline'}
    notices=[]
    codex_request({'id':3,'method':'mcpServer/elicitation/request','params':{'mode':'url','message':'Sign in','url':'https://example.com'}},execution,sent.append,lambda **v:notices.append(v))
    row=execution.requests.snapshot()[-1];execution.requests.answer(row['id'],{'action':['Continue']});assert sent[-1]['result']=={'action':'accept'} and notices[-1]['native_notices'][0]['url']=='https://example.com'
    amendment={'acceptWithExecpolicyAmendment':{'execpolicy_amendment':['git','status']}}
    codex_request({'id':4,'method':'item/commandExecution/requestApproval','params':{'availableDecisions':['accept',amendment,'decline']}},execution,sent.append)
    row=execution.requests.snapshot()[-1];execution.requests.answer(row['id'],{'decision':['Approve and save this command rule']});assert sent[-1]['result']['decision']==amendment
    codex_request({'id':5,'method':'item/permissions/requestApproval','params':{'permissions':{'fileSystem':{'read':['/work']}}}},execution,sent.append)
    row=execution.requests.snapshot()[-1];execution.requests.answer(row['id'],{'decision':['Approve this session']});assert sent[-1]['result']['scope']=='session'
    codex_request({'id':6,'method':'currentTime/read'},execution,sent.append);assert abs(sent[-1]['result']['currentTimeAt']-time.time())<2
    notice(execution,lambda **v:None,'Working',key='native-status')
    notice(execution,lambda **v:None,'Finished',key='native-status')
    assert len([r for r in execution.notices if r.get('key')=='native-status'])==1
    notice(execution,lambda **v:None,'',key='native-status');assert not any(r.get('key')=='native-status' for r in execution.notices)
    with tempfile.TemporaryDirectory(prefix='aura-native-interop-') as td:
        root=Path(td);script=root/'native.py';script.write_text(FIXTURE,encoding='utf-8')
        handler=root/'provider.py';handler.write_text("import json,sys;from pathlib import Path\nevent=json.load(sys.stdin)\nassert Path.cwd().name=="+repr(root.name)+"\nprint(json.dumps({'result':{'output':event['params']['value']}}))",encoding='utf-8')
        execution.native_handler={'argv':[sys.executable,str(handler)]};execution.native_cwd=root
        codex_request({'id':7,'method':'item/tool/call','params':{'value':'provider-result'}},execution,sent.append)
        wait(lambda:any(r['id']==7 for r in sent));assert next(r for r in sent if r['id']==7)['result']=={'output':'provider-result'}
        wait(lambda:not execution.helpers)
        execution.native_handler=None
        codex_request({'id':8,'method':'attestation/generate'},execution,sent.append,lambda **v:notices.append(v))
        assert sent[-1]['error']['code']==-32601,'A missing authentication provider must never produce a fabricated proof'
        image=root/'selected.png';image.write_bytes(b'only-selected-image')
        for command,expected in (('compact','Conversation compacted.'),('review','Native review complete.')):
            native=Execution();native.interactive=True
            reply=workspace_codex.run([sys.executable,'-u',str(script),'codex-'+command,str(root/'unused'),'exec'],root,'/'+command,None,'fixture','',lambda **v:None,dict(os.environ),native)
            assert reply['reply']==expected
        for kind in ('codex','claude','pi','omp'):
            media=attachments([{'kind':'file','path':str(image)}],kind);assert len(media)==1
            if kind=='codex':assert media[0]=={'type':'localImage','path':str(image)}
            assert attachments([{'kind':'record','path':str(image)}],kind)==[]
            live=Execution();live.interactive=True;live.child_model='child-default';live.native_agent='jeff';live.native_options={'thread':{'config':{'model_verbosity':'low'}}} if kind=='codex' else {};updates=[];result={};release=root/(kind+'-release')
            def run():
                try:
                    argv=[sys.executable,'-u',str(script),kind,str(release),'exec' if kind=='codex' else '--print']
                    result.update(workspace_codex.run(argv,root,'Work',None,'fixture','',lambda **v:updates.append(v),dict(os.environ),live,child_model='child-default') if kind=='codex' else workspace_agents.run(argv,kind,root,dict(os.environ),'Work',None,'fixture','',lambda **v:updates.append(v),live))
                except Exception as error:result['error']=error
            worker=threading.Thread(target=run);worker.start()
            try:
                wait(lambda:any(r['status']=='pending' for r in live.requests.snapshot()) or not worker.is_alive())
                assert worker.is_alive(),result
                pending=next(r for r in live.requests.snapshot() if r['status']=='pending')
                answer={'decision':['Approve for this session']} if kind=='codex' else {'decision':['Approve and apply the suggested native rule']} if kind=='claude' else {'answer':['ephemeral-secret']}
                live.requests.answer(pending['id'],answer)
                if kind=='codex':
                    wait(lambda:any(u.get('background_processes') for u in updates));assert worker.is_alive(),'Parent completion killed background work';release.touch()
                worker.join(8);assert not worker.is_alive() and 'error' not in result,(kind,result)
                if kind=='codex':assert len(result['reply'])==100123 and result['native_id']=='parent'
                elif kind=='claude':assert result['reply']=='Child finished too.'
                else:
                    assert any(u.get('native_notices') for u in updates) and any(u.get('native_editor',{}).get('text')=='Prepared draft' for u in updates)
                    assert 'ephemeral-secret' not in json.dumps(updates) and 'ephemeral-secret' not in json.dumps(live.requests.snapshot())
            finally:
                if worker.is_alive():live.stop();worker.join(8)
    if os.name=='nt':
        # npm shims for packages that ship a native program (current Claude Code) launch it
        # directly, not through a PowerShell script that execution policy may block.
        from unittest.mock import patch
        import workspace_ui
        with tempfile.TemporaryDirectory() as td:
            bin_dir=Path(td);exe=bin_dir/'node_modules/@anthropic-ai/claude-code/bin/claude.exe'
            exe.parent.mkdir(parents=True);exe.write_bytes(b'')
            (bin_dir/'claude.cmd').write_text('@ECHO off\r\n"%dp0%\\node_modules\\@anthropic-ai\\claude-code\\bin\\claude.exe"   %*\r\n')
            (bin_dir/'claude.ps1').write_text('# npm PowerShell shim\r\n')
            found=lambda name:str(bin_dir/'claude.cmd') if name=='claude' else None
            with patch('workspace_ui.shutil.which',side_effect=found):
                claude=next(a for a in workspace_ui.installed_agents() if a['id']=='claude')
            assert claude['argv'][0]==str(exe),claude
    print('Native interop passed: child approvals, background lifetime, native rules/forms, secret input, extension notices and images; no model calls.')

if __name__=='__main__':main()
