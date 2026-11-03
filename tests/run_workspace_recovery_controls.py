"""Recovery stays scoped, read-only until reviewed, and independent of workstation helpers."""
from pathlib import Path
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import json,os,subprocess,sys,tempfile,threading,time

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))


def wait(check):
    end=time.monotonic()+12
    while time.monotonic()<end:
        if check():return
        time.sleep(.02)
    raise AssertionError('Recovery fixture did not finish')


def main():
    from setup import setup
    from workspace_ui import Workspace,handler_for
    import workspace_recovery as recovery
    import workspace_codex
    with tempfile.TemporaryDirectory(prefix='aura-recovery-controls-') as td,patch.dict(os.environ):
        base=Path(td);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        bid=setup(organization='Recovery studio')['business_id']
        script=base/'worker.py';script.write_text("import sys,time;from pathlib import Path;sys.stdin.read();Path('started').touch();\nwhile not Path('release').exists():time.sleep(.02)\nprint('Saved result.')",encoding='utf-8')
        app=Workspace(agent={'name':'Fixture','argv':[sys.executable,'-u',str(script)]},settings_file=base/'settings.json')
        app.preferences['connection']={'kind':'configured','model':'fixture','effort':''}
        job=app.start_chat(bid,'Keep this assignment',[],chat_id='');wait(lambda:(root/'started').exists())
        snapshot=app.settings_file.read_text(encoding='utf-8')
        restored=Workspace(agent=app.configured_agent,settings_file=app.settings_file)
        try:
            # A browser/server reconnect must never start the same work twice.
            found=recovery.check(restored,bid,job['chat_id']);assert found['recovery']['state']=='running_elsewhere',found['recovery']
            try:recovery.prepare(restored,bid,job['chat_id'],found['recovery']['revision'],True);raise AssertionError('Surviving work duplicated')
            except ValueError:pass
            try:restored.start_chat(bid,'Duplicate',[],chat_id=job['chat_id']);raise AssertionError('Direct API bypassed process ownership')
            except ValueError:pass
            # Simulate the process finishing after its UI server disappeared.
            (root/'release').touch();wait(lambda:app.jobs[job['id']]['status']!='working')
            with app.lock:pass
            app.settings_file.write_text(snapshot,encoding='utf-8')
            restored=Workspace(agent=app.configured_agent,settings_file=app.settings_file)
            finished=recovery.check(restored,bid,job['chat_id']);assert finished['chat']['status']=='complete' and finished['recovery']['state']=='complete'
            assert finished['messages'][-1]['text']=='Saved result.' and not restored.jobs
            # Request/process identity and an explicit final outcome are required.
            native={'id':'native-chat','business_id':bid,'workspace':str(root),'agent':'codex','native_id':'native-session','title':'Research','model':'fixture','effort':'low','status':'working','created':1,'updated':2,
                    'recovery':{'request_id':'aaaaaaaaaaaaaaaa','started':1,'status':'working','process':{'pid':999999999,'born':'not-this-process'}}}
            restored.preferences['chats'].append(native);restored.save_preferences()
            shown=[{'role':'user','text':'Research','request_id':'aaaaaaaaaaaaaaaa'},{'role':'assistant','text':'Native result','request_id':'aaaaaaaaaaaaaaaa'}]
            native_result={'messages':shown,'usage':{},'native_id':'native-session','native_observation':{'request_id':'old-request','state':'complete'}}
            with patch('workspace_ui.installed_agents',return_value=[{'id':'codex','name':'Fixture','argv':['fixture','exec','-']}]),patch.object(workspace_codex,'history',return_value=native_result) as read:
                uncertain=recovery.check(restored,bid,native['id']);assert uncertain['recovery']['state']=='interrupted'
                assert native['status']=='working','An earlier request’s result must not complete this one'
                native['recovery']['background_work']=True
                assert recovery.describe(native)['state']=='uncertain','A missing parent does not establish that its background work stopped'
                native['recovery'].pop('background_work')
                recovery.check(restored,bid,native['id']);assert read.call_count==1,'Repeated tabs should share the bounded metadata read'
                try:recovery.prepare(restored,bid,native['id'],'stale',True);raise AssertionError('Stale recovery accepted')
                except ValueError:pass
                prepared=recovery.prepare(restored,bid,native['id'],uncertain['recovery']['revision']);assert prepared['draft'] and native['status']=='stopped' and not restored.jobs
                recovery.check(restored,bid,native['id']);assert native['status']=='stopped','Stop/review must not resurrect work'
                native.update(status='working',updated=3);native_result['native_observation']['request_id']='aaaaaaaaaaaaaaaa';restored.read_cache.clear()
                completed=recovery.check(restored,bid,native['id']);assert completed['recovery']['state']=='complete' and native['status']=='complete'
            # A gateway may survive its local connection: outcome remains a review.
            gateway={**native,'id':'gateway-chat','agent':'hermes','status':'working','native_id':None,'updated':4}
            gateway['recovery']={**native['recovery'],'request_id':'bbbbbbbbbbbbbbbb','status':'working'}
            restored.preferences['chats'].append(gateway);restored.save_preferences()
            unknown=recovery.check(restored,bid,gateway['id']);assert unknown['recovery']['state']=='uncertain'
            try:recovery.prepare(restored,bid,gateway['id'],unknown['recovery']['revision']);raise AssertionError('Unconfirmed gateway work continued without review')
            except ValueError:pass
            with patch.object(restored,'save_preferences',side_effect=OSError('Unwritable settings')):
                try:recovery.prepare(restored,bid,gateway['id'],unknown['recovery']['revision'],True);raise AssertionError('A failed save reported successful preparation')
                except OSError:pass
            assert gateway['status']=='working','A failed save must not clear the recovery guard in memory'
            recovery.prepare(restored,bid,gateway['id'],unknown['recovery']['revision'],True)
            for kind in ('pi','omp','claude'):
                prompt='AURA message reference: aaaaaaaaaaaaaaaa\nUser request:\nResearch'
                rows=[{'role':'user','content':prompt},{'role':'assistant','content':[{'type':'text','text':'Before a tool'}],'stopReason':'toolUse'}]
                assert recovery.native_observation(rows,kind)['state']=='unfinished'
                rows.append({'role':'assistant','content':[{'type':'text','text':'Final'}],'stop_reason':'end_turn'})
                assert recovery.native_observation(rows,kind)['state']=='complete'
                rows.append({'role':'user','content':'A different assignment'})
                assert recovery.native_observation(rows,kind)['request_id']=='','Outside work must not be attributed to the old Aura assignment'
            # Public HTTP/CLI entry points use the same owner and scope protections.
            native.update(status='working',native_id=None,updated=5);native['recovery']['status']='working';restored.read_cache.clear();restored.save_preferences()
            server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(restored));threading.Thread(target=server.serve_forever,daemon=True).start()
            def call(data,expected=200):
                req=Request(f'http://127.0.0.1:{server.server_port}/api/chats/recovery',data=json.dumps(data).encode(),headers={'X-Aura-Token':restored.token,'X-Aura-Workspace':str(root),'Content-Type':'application/json'})
                try:
                    with urlopen(req,timeout=15) as r:status=r.status;value=json.load(r)
                except HTTPError as error:status=error.code;value=json.load(error)
                assert status==expected,(status,value);return value
            try:
                result=call({'action':'check','business':bid,'id':native['id']})
                call({'action':'check','business':'wrong','id':native['id']},400)
                command=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_recovery.py'),'check','--workspace',str(root),'--business-id',bid,'--chat',native['id'],'--url',f'http://127.0.0.1:{server.server_port}','--json'],capture_output=True,text=True,check=True)
                assert json.loads(command.stdout)['recovery']['state']=='uncertain'
                first=call({'action':'prepare','business':bid,'id':native['id'],'revision':result['recovery']['revision'],'reviewed':True})
                assert 'Original assignment:\nResearch' in first['draft'] and 'context' in first,'A missing native session needs the actual assignment, not a contextless Continue prompt'
                call({'action':'prepare','business':bid,'id':native['id'],'revision':result['recovery']['revision']},400)
                assert first['chat']['status']=='stopped' and not restored.jobs
            finally:server.shutdown();server.server_close()
        finally:
            for execution in app.executions.values():execution.stop()
            wait(lambda:not app.running_jobs())
    print('Recovery controls passed: surviving process identity, saved completion, matching native outcomes, Stop, uncertainty, duplicate tabs, and shared CLI/API.')


if __name__=='__main__':main()
