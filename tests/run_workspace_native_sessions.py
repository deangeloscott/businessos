"""Native process/session state survives ordinary messages; no inference."""
import json,os,sys,tempfile,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

FIXTURE=r'''
import json,sys,os
kind=sys.argv[1];turn=0;approved=False;initializations=0
def emit(v):print(json.dumps(v),flush=True)
def finish():
 text=f'Turn {turn}, native PID {os.getpid()}, permission {approved}'
 if kind=='codex':
  emit({'method':'item/completed','params':{'threadId':'native','item':{'type':'agentMessage','id':str(turn),'text':text}}})
  emit({'method':'turn/completed','params':{'threadId':'native','turn':{'id':str(turn),'status':'completed'}}})
 elif kind=='claude':emit({'type':'result','session_id':'native','result':text})
 else:
  emit({'type':'message_end','message':{'role':'assistant','content':[{'type':'text','text':text}]}})
  emit({'type':'session_settled'})
for line in sys.stdin:
 m=json.loads(line);op=m.get('method');typ=m.get('type');i=m.get('id')
 if kind=='codex':
  if op=='initialize':
   initializations+=1;assert initializations==1;emit({'id':i,'result':{}})
  elif op=='thread/start':emit({'id':i,'result':{'thread':{'id':'native'}}})
  elif op=='thread/resume':raise AssertionError('A live native thread must not be reloaded between messages')
  elif op=='turn/start':
   turn+=1;emit({'id':i,'result':{'turn':{'id':str(turn)}}})
   if approved:finish()
   else:emit({'id':'approval','method':'item/commandExecution/requestApproval','params':{'threadId':'native','availableDecisions':['acceptForSession','decline']}})
  elif op=='thread/backgroundTerminals/list':emit({'id':i,'result':{'data':[]}})
  elif i=='approval':assert m['result']['decision']=='acceptForSession';approved=True;finish()
 elif kind=='claude':
  if typ=='control_request':
   initializations+=1;assert initializations==1;emit({'type':'control_response','response':{'subtype':'success','request_id':m['request_id'],'response':{}}})
  elif typ=='user':
   turn+=1
   if approved:finish()
   else:emit({'type':'control_request','request_id':'approval','request':{'subtype':'can_use_tool','tool_name':'Bash','input':{'command':'work'}}})
  elif typ=='control_response':assert m['response']['response']['behavior']=='allow';approved=True;finish()
 else:
  if typ=='get_state':
   emit({'type':'agent_settled'})
   emit({'type':'response','id':i,'success':True,'data':{'sessionId':'native','isStreaming':False}})
  elif typ=='prompt':
   turn+=1
   if approved:finish()
   else:emit({'type':'extension_ui_request','id':'approval','method':'confirm','message':'Continue?'})
  elif typ=='extension_ui_response':assert m['confirmed'];approved=True;finish()
'''

def wait(check):
    end=time.monotonic()+8
    while time.monotonic()<end:
        if check():return
        time.sleep(.01)
    raise AssertionError('Native session fixture timed out')

def main():
    from workspace_native_sessions import Sessions
    from workspace_execution import Execution
    import workspace_codex,workspace_agents
    with tempfile.TemporaryDirectory(prefix='aura-live-session-') as td:
        root=Path(td);fixture=root/'native.py';fixture.write_text(FIXTURE,encoding='utf-8')
        for kind in ('codex','claude','pi','omp'):
            sessions=Sessions();key=(str(root),'studio',kind);updates=[]
            def request(number,native_id=None):
                execution=Execution();execution.interactive=True;execution.connection={};result={}
                argv=[sys.executable,'-u',str(fixture),kind,'exec' if kind=='codex' else '--print']
                def update(**v):updates.append(v)
                def launch():
                    return workspace_codex.run(argv,root,'Message '+str(number),native_id,'fixture','',update,dict(os.environ),execution) if kind=='codex' else workspace_agents.run(argv,kind,root,dict(os.environ),'Message '+str(number),native_id,'fixture','',update,execution)
                def run():
                    try:result.update(sessions.run(key,{'kind':kind},'Message '+str(number),native_id,execution,update,launch,root))
                    except Exception as error:result['error']=error
                worker=threading.Thread(target=run);worker.start()
                return execution,result,worker
            try:
                first,result,worker=request(1)
                wait(lambda:first.requests.snapshot() or not worker.is_alive())
                assert worker.is_alive(),result
                q=next(r for r in first.requests.snapshot() if r['status']=='pending')
                answers={'decision':['Approve for this session']} if kind=='codex' else {'decision':['Approve once']} if kind=='claude' else {'answer':['Yes']}
                first.requests.answer(q['id'],answers);worker.join(8)
                assert not worker.is_alive() and 'error' not in result,result
                pid=first.process.pid;assert first.process.poll() is None and sessions.owns_idle(key)
                second,result2,worker2=request(2,result['native_id']);worker2.join(8)
                assert not worker2.is_alive() and 'error' not in result2,result2
                assert second.process.pid==pid and first.requests is second.requests
                assert result2['reply']==f'Turn 2, native PID {pid}, permission True'
                first.stop();assert second.process.poll() is None,'An old request stopped the reused native conversation'
            finally:sessions.close()
    print('Native sessions passed: two messages, one process/initialization, retained native grants, scoped stale Stop and clean shutdown across Codex/Claude/Pi/OMP.')

if __name__=='__main__':main()
