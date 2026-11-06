"""Hermes native gateway: identity, goals, commands, approvals and reconnection."""
import json,os,sys,tempfile,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))

FIXTURE=r'''
import json,sys,os
def emit(v):print(json.dumps({'jsonrpc':'2.0',**v}),flush=True)
def event(t,p):emit({'method':'event','params':{'type':t,'session_id':'runtime','payload':p}})
goal=None;turn=0;offset=0;model_provider='local';effort=''
emit({'method':'event','params':{'type':'gateway.ready','payload':{}}})
for line in sys.stdin:
 m=json.loads(line);op=m.get('method');p=m.get('params') or {};i=m.get('id')
 def reply(v):emit({'id':i,'result':v})
 if op=='client.capabilities':reply({})
 elif op=='model.options':reply({'model':'fixture','provider':'local','providers':[{'slug':'local','models':['fixture']},{'slug':'remote','models':['fixture']}]})
 elif op in {'session.create','session.resume'}:
  assert p.get('profile')=='fixture','The native profile was lost'
  if op=='session.resume':assert p['session_id']=='stored'
  offset=100 if op=='session.resume' and p.get('eager_build') else 0
  if os.environ.get('AURA_FIXTURE_CHANGED_GOAL'):goal={'title':'Finish fixture','status':'active','contract':{'changed':True}}
  if op=='session.create':assert p['model']=='fixture' and p['provider']=='remote';model_provider=p['provider']
  reply({'session_id':'runtime','stored_session_id':'stored','info':{'model':'fixture','provider':model_provider,**({'usage':{'input':offset,'output':offset//2}} if offset or op=='session.create' else {'lazy':True})}})
 elif op=='config.set':
  assert p['scope']=='session'
  if p['key']=='model':assert p['value']=='fixture --provider remote';model_provider='remote';effort=''
  else:assert p['key']=='reasoning' and p['value']=='high';effort=p['value']
  reply({})
 elif op=='commands.catalog':reply({'pairs':[['/goal','Native goal'],['/tools','Native tools']]})
 elif op=='session.control.read':reply({'control':{'goal':goal}})
 elif op=='slash.exec':
  assert p['session_id']=='runtime' and p['command'].startswith('/goal ')
  assert '\n\nWork' not in p['command'],'Aura context was stored as the native goal'
  goal={'title':p['command'][6:].split('\n')[0],'status':'active'}
  reply({'type':'send','message':'Native first turn'})
 elif op=='prompt.submit':
  assert model_provider=='remote','The selected provider was silently replaced by the profile default'
  assert effort=='high','Changing models lost the selected effort'
  turn+=1;reply({})
  emit({'id':'approval-'+str(turn),'method':'approval','params':{'session_id':'runtime','description':'Read fixture','command':'read','choices':['once','deny']}})
 elif str(i).startswith('approval-'):
  assert m['result']=={'choice':'once'}
  event('message.complete',{'text':f'Turn {turn}, PID {os.getpid()}','status':'complete','usage':{'input':offset+10*turn,'output':offset//2+5*turn}})
  if goal:
   event('session.control.update',{'control':{'goal':goal}})
   goal={**goal,'status':'completed'}
   event('session.control.update',{'control':{'goal':goal}})
 elif op=='session.control':
  goal={**goal,'status':'paused'} if p['action']=='goal.pause' else None
  reply({'control':{'goal':goal}})
'''

def main():
 from workspace_execution import Execution
 from workspace_native_sessions import Sessions
 from workspace_hermes import run,goal_state,saved_control,model_route
 from workspace_native_settings import selections
 from workspace_native_goals import observe
 from types import SimpleNamespace
 from unittest.mock import patch
 request={'id':'goal','objective':'Finish fixture\nDone when: complete','protocol':'hermes-gateway'};chat={};app=SimpleNamespace(save_preferences=lambda:None)
 with patch('workspace_goals.find',side_effect=ValueError('No canonical write in this observation check')):
  observe(app,'studio',chat,request,{'status':'active','objective':'Finish fixture','native_basis':'native-one','bound_to':request['objective']})
  assert not request.get('native_changed') and request['native_objective']=='Finish fixture'
  observe(app,'studio',chat,request,{'status':'complete','objective':'Finish fixture','native_basis':'native-two'})
  assert request['native_changed'] and chat['native_goal']['status']=='needs_review','Changed native criteria completed the old assignment'
 assert goal_state({'goal':{'status':'achieved','title':'done'}})['status']=='complete'
 assert model_route({'model':'qwen:27b','provider':'local','providers':[{'slug':'local','is_current':True,'is_user_defined':True,'models':['qwen:27b']}]},'custom:qwen:27b')=={'model':'qwen:27b','provider':'local'}
 rows=[{'id':'native-feature','name':'Native feature','type':'select','options':[{'value':'on'},{'value':'off'}]}]
 assert selections(rows,{'native-feature':'on'})=={'native-feature':'on'}
 try:selections(rows,{'native-feature':'made-up'})
 except ValueError:pass
 else:raise AssertionError('Unadvertised native setting accepted')
 from workspace_native_goals import support
 connection={'argv':[],'native_options':{'gateway_argv':[sys.executable,'native.py'],'session':{'profile':'fixture'}}}
 assert support('hermes',connection)['supported']
 assert not support('hermes',connection,'accept_edits')['supported'],'ACP permissions incorrectly advertised native goal controls'
 assert not support('hermes',{**connection,'native_options':{**connection['native_options'],'config':{'tier':'priority'}}})['supported']
 with patch('workspace_agents.Metadata') as metadata:
  host=metadata.return_value
  host.call.side_effect=[{'session_id':'runtime','stored_session_id':'stored'},{'control':{'goal':{'title':'Finish fixture','status':'active'}}},{'control':{'goal':None}}]
  assert saved_control([],connection['native_options'],ROOT,dict(os.environ),'stored','Finish fixture','clear')['status']=='cleared'
  assert host.call.call_args_list[0].kwargs['profile']=='fixture','Saved native controls used another profile'
 with tempfile.TemporaryDirectory(prefix='aura-hermes-gateway-') as td:
  root=Path(td);script=root/'native.py';script.write_text(FIXTURE,encoding='utf-8');pool=Sessions();updates=[];key=(str(root),'studio','hermes');pid=None
  try:
   for turn in (1,2,3,4):
    if turn>=3:assert pool.release_idle(key)
    execution=Execution();execution.interactive=True;execution.native_options={'gateway_argv':[sys.executable,'-u',str(script)],'session':{'profile':'fixture',**({'eager_build':True} if turn==4 else {})}}
    execution.native_goal={'id':'goal','objective':'Finish fixture\nDone when: fixture has a result','protocol':'hermes-gateway'} if turn==1 else None
    result={}
    def update(**values):updates.append(values)
    def work():
     try:result.update(pool.run(key,{},'Work',None if turn==1 else 'stored',execution,update,lambda:run([],root,dict(os.environ),'Work',None if turn==1 else 'stored','remote:fixture','high',update,execution),root))
     except Exception as error:result['error']=error
    worker=threading.Thread(target=work);worker.start();until=time.monotonic()+10
    while not any(r['status']=='pending' for r in execution.requests.snapshot()) and worker.is_alive() and time.monotonic()<until:time.sleep(.01)
    pending=next((r for r in execution.requests.snapshot() if r['status']=='pending'),None)
    assert pending,result
    assert not pool.release_idle(key)
    execution.requests.answer(pending['id'],{'choice':['once']});worker.join(10)
    assert not worker.is_alive() and 'error' not in result,result
    assert result['native_id']=='stored' and result['reply'].startswith(f'Turn {1 if turn>=3 else turn}, PID ')
    assert result['usage']=={'input_tokens':10,'output_tokens':5},('Cumulative native usage was counted twice',result)
    if turn==2:assert pid==execution.process.pid
    pid=execution.process.pid
    if turn==1:assert any(v.get('native_goal',{}).get('status')=='completed' for v in updates)
   assert any(v.get('native_commands') for v in updates)
   session=pool.items[key];session.goal_active=True;session.last_activity-=601
   assert pool.expire_idle()==0
   session.goal_active=False;session.background=True
   assert pool.expire_idle()==0
   session.background=False
   session.native_work=True
   assert pool.expire_idle()==0,'Native loops and heartbeats must survive idle cleanup'
   session.native_work=False
   assert pool.expire_idle()==1 and execution.process.poll() is not None
   # A native criteria change between processes must not be overwritten by /goal.
   execution=Execution();execution.native_options={'gateway_argv':[sys.executable,'-u',str(script)],'session':{'profile':'fixture'}}
   execution.native_goal={'id':'goal','objective':'Finish fixture','protocol':'hermes-gateway','native_basis':'previous-contract'}
   try:run([],root,dict(os.environ,AURA_FIXTURE_CHANGED_GOAL='1'),'Work','stored','remote:fixture','',lambda **v:None,execution)
   except ValueError as error:assert 'criteria changed' in str(error),error
   else:raise AssertionError('Changed native goal criteria were overwritten')
  finally:pool.close()
 print('Hermes native gateway passed: exact identity/profile, goal contract guards, native approval, retained process, resumed usage and idle cleanup.')

if __name__=='__main__':main()
