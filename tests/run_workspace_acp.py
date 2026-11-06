"""ACP conversation identity, native decisions, forms and resumable turns."""
import json,os,sys,tempfile,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
FIXTURE=r'''
import json,sys,os,base64
turn=0;ready=False;granted=False;initializations=0;mode='default'
def emit(v):print(json.dumps({'jsonrpc':'2.0',**v}),flush=True)
def result():
 emit({'method':'session/update','params':{'sessionId':'native-acp','update':{'sessionUpdate':'usage_update','used':75,'size':1000}}})
 emit({'method':'session/update','params':{'sessionId':'native-acp','update':{'sessionUpdate':'agent_message_chunk','content':{'type':'text','text':f'Native {turn} from {os.getpid()}'}}}})
 emit({'id':'aura-prompt','result':{'stopReason':'end_turn'}})
 emit({'method':'session/update','params':{'sessionId':'native-acp','update':{'sessionUpdate':'available_commands_update','availableCommands':[{'name':'native-command','description':'Native command'}]}}})
for line in sys.stdin:
 m=json.loads(line);op=m.get('method');i=m.get('id');p=m.get('params') or {}
 if op=='initialize':
  initializations+=1;assert initializations==1
  if p['clientCapabilities']:assert p['clientCapabilities']['elicitation']=={'form':{},'url':{}}
  emit({'id':i,'result':{'protocolVersion':1,'agentCapabilities':{'loadSession':True,'promptCapabilities':{'image':True}}}})
 elif op in {'session/new','session/load'}:
  if op=='session/load':
   emit({'method':'session/update','params':{'sessionId':'native-acp','update':{'sessionUpdate':'current_mode_update','currentModeId':'default'}}})
   emit({'method':'session/update','params':{'sessionId':'native-acp','update':{'sessionUpdate':'config_option_update','configOptions':[{'id':'model','category':'model','type':'select','currentValue':'native-model','options':[{'value':'native-model','name':'Native model'}]}]}}})
   emit({'method':'session/update','params':{'sessionId':'native-acp','update':{'sessionUpdate':'user_message_chunk','content':{'type':'text','text':'Earlier work'}}}})
   emit({'method':'session/update','params':{'sessionId':'native-acp','update':{'sessionUpdate':'agent_message_chunk','content':{'type':'text','text':'Saved native reply'}}}})
   emit({'method':'session/update','params':{'sessionId':'native-acp','update':{'sessionUpdate':'agent_message_chunk','content':{'type':'image','mimeType':'image/png','data':base64.b64encode(b'\x89PNG\r\n\x1a\nfixture').decode()}}}})
  emit({'id':i,'result':{'sessionId':'native-acp','models':{'currentModelId':'native-model','availableModels':[{'modelId':'native-model','name':'Native model'}]},'modes':{'currentModeId':'default','availableModes':[{'id':'default','name':'Ask'},{'id':'full','name':'Native full mode'},{'id':'review','name':'Review mode'}]}}})
 elif op=='session/set_mode':mode=p['modeId'];assert mode in {'full','review'};emit({'id':i,'result':{}})
 elif op=='session/prompt':
  assert mode==('full' if turn==0 else 'review'),'The explicit native mode was skipped or renamed'
  turn+=1
  if granted:result()
  else:emit({'id':'native-permission','method':'session/request_permission','params':{'sessionId':'native-acp','toolCall':{'toolCallId':'one','title':'Read the selected file','rawInput':{'path':'selected.txt'}},'options':[{'optionId':'allow-session','name':'Allow for this session','kind':'allow_always'},{'optionId':'deny','name':'Decline','kind':'reject_once'}]}})
 elif i=='native-permission':
  assert m['result']=={'outcome':{'outcome':'selected','optionId':'allow-session'}}
  granted=True
  emit({'id':'native-form','method':'elicitation/create','params':{'sessionId':'native-acp','mode':'form','message':'Choose output','requestedSchema':{'type':'object','properties':{'name':{'type':'string'}},'required':['name']}}})
 elif i=='native-form':assert m['result']=={'action':'accept','content':{'name':'Guide'}};result()
'''

def main():
    from workspace_acp import run
    from workspace_native_sessions import Sessions
    from workspace_execution import Execution
    with tempfile.TemporaryDirectory(prefix='aura-acp-') as td:
        root=Path(td);script=root/'agent.py';script.write_text(FIXTURE,encoding='utf-8')
        pool=Sessions();key=(str(root),'studio','acp');updates=[];pid=None
        try:
            for turn in (1,2):
                execution=Execution();execution.interactive=True;execution.permission='full' if turn==1 else 'review';out={}
                def update(**v):updates.append(v)
                def work():
                    try:out.update(pool.run(key,{},'Work','native-acp',execution,update,
                        lambda:run([sys.executable,'-u',str(script)],'acp',root,dict(os.environ),'Work','native-acp','native-model','',update,execution),root))
                    except Exception as error:out['error']=error
                thread=threading.Thread(target=work);thread.start();seen=set();end=time.monotonic()+8
                while thread.is_alive() and time.monotonic()<end:
                    for row in execution.requests.snapshot():
                        if row['status']!='pending' or row['id'] in seen:continue
                        seen.add(row['id'])
                        answers={'decision':['allow-session']} if row['native_id']=='native-permission' else {'action':['Submit'],json.dumps(('name',)):['Guide']}
                        execution.requests.answer(row['id'],answers)
                    time.sleep(.01)
                assert not thread.is_alive() and 'error' not in out,out
                pid=pid or execution.process.pid
                assert out['reply']==f'Native {turn} from {pid}' and out['native_id']=='native-acp'
                assert out['usage']=={'context':{'tokens':75,'window':1000}},out
            assert any(v.get('native_controls')=={'steer':False,'interrupt':True} for v in updates)
            end=time.monotonic()+2
            while not any(v.get('native_commands') for v in updates) and time.monotonic()<end:time.sleep(.01)
            assert any(v.get('native_commands') for v in updates),'Idle native updates were lost'
        finally:pool.close()
        # A future agent uses the same native protocol, catalog and UI connection API.
        from unittest.mock import patch
        from http.server import ThreadingHTTPServer
        from urllib.request import Request,urlopen
        from setup import setup
        from workspace_ui import Workspace,handler_for
        with patch.dict(os.environ,{'BUSINESSOS_WORKSPACE':str(root/'workspace'),'BUSINESSOS_WORKSPACE_CONFIG':str(root/'pointer.json'),'AURA_STATE_DIR':str(root/'state')}):
            bid=setup(organization='Custom ACP studio')['business_id']
            app=Workspace(agent={'name':'Custom native agent','argv':[sys.executable,'-u',str(script)],'native_protocol':'acp'})
            server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));threading.Thread(target=server.serve_forever,daemon=True).start()
            try:
                assert app.agent_options('configured')['models'][0]['id']=='native-model'
                assert app.connection()['native_sessions'] and app.connection()['choices'][0]['native']
                req=Request(f'http://127.0.0.1:{server.server_port}/api/connect',data=json.dumps({'kind':'configured','model':'native-model','effort':''}).encode(),headers={'Content-Type':'application/json','X-Aura-Token':app.token,'X-Aura-Workspace':app.workspace_path})
                with urlopen(req,timeout=15) as response:connected=json.load(response)
                assert connected['model']=='native-model' and connected['model_controls']
                app.preferences['chats'].append({'id':'custom-chat','business_id':bid,'workspace':app.workspace_path,'agent':'configured','native_id':'native-acp','status':'complete','model':'native-model','effort':''})
                refreshed=app.conversation(bid,'custom-chat',refresh=True)
                assert refreshed['messages'][-1]['text']=='Saved native reply' and not refreshed.get('history_note'),refreshed
                image=refreshed['messages'][-1]['native_media'][0]
                assert 'native_images' not in refreshed['messages'][-1] and (Path(app.workspace_path)/image['path']).is_file()
                assert app.conversation(bid,'custom-chat',refresh=True)['messages'][-1]['native_media']==[image]
            finally:app.native_sessions.close();server.shutdown();server.server_close()
    print('ACP passed: native initialization, same-process follow-ups, exact permission choices and typed forms without inference.')

if __name__=='__main__':main()
