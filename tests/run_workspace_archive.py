"""Archive/recovery parity and chat-scoped native permissions, without a model request."""
import json, os, subprocess, sys, tempfile, threading, time
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def main():
    from setup import setup
    from workspace_ui import Workspace, handler_for
    import workspace_ui, workspace_goals as goals, workspace_organization as organization, workspace_permissions as permissions
    with tempfile.TemporaryDirectory(prefix='aura-archive-') as temp, patch.dict(os.environ):
        base = Path(temp); root = base / 'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root), BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'), AURA_STATE_DIR=str(base/'state'))
        bid = setup(organization='Archive studio')['business_id']
        app = Workspace(agent={'name':'Fixture','argv':[sys.executable]})
        app.preferences['chats'].append({'id':'archived','business_id':bid,'title':'Earlier work','agent':'configured','status':'complete','archived':True,'updated':10})
        app.preferences['chats'].append({'id':'other','business_id':'other','title':'Private elsewhere','archived':True,'updated':50})
        goal = goals.save(bid, {'name':'Return to this goal','target':'Useful work','horizon':'This quarter','status':'active'})
        goals.remove(bid, goal['id']); app.save_preferences()
        ident = 'a'*32; recovery_root=base/'AURA Recovery'; copy=recovery_root/('Original-'+ident[:8]);copy.mkdir(parents=True);(copy/'kept.txt').write_text('Keep this work')
        record=organization._root(app.settings_file.parent)/'recovery'/(ident+'.json');record.parent.mkdir(parents=True,exist_ok=True)
        record.write_text(json.dumps({'id':ident,'original':str(base/'Original'),'path':str(copy),'recovery_root':str(recovery_root),'destination':str(root),'status':'available','retired':20,'days':0,'expires':None}))
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}'
        def call(path,data=None,status=200):
            try:
                with urlopen(Request(url+path,data=json.dumps(data).encode() if data is not None else None,headers={'X-Aura-Token':app.token,'X-Aura-Workspace':str(root),'Content-Type':'application/json'})) as response:
                    assert response.status==status;return json.load(response)
            except HTTPError as error:
                assert error.code==status,(error.code,error.read());return json.load(error)
        try:
            listed=call('/api/archive?business='+bid)['items'];assert {i['kind'] for i in listed}=={'chat','goal','recovery'} and 'other' not in {i['id'] for i in listed}
            def cli(*args):
                result=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/workspace_archive.py'),*args,'--workspace',str(root),'--business-id',bid,'--url',url,'--json'],capture_output=True,text=True,encoding='utf-8',check=True)
                return json.loads(result.stdout)
            assert cli('list')['items']==listed
            cli('restore','--kind','chat','--id','archived');assert not app.preferences['chats'][0]['archived']
            cli('restore','--kind','goal','--id',goal['id']);assert not goals.deleted(goals.find(bid,goal['id']))
            cli('restore','--kind','recovery','--id',ident);assert (base/'Original'/'kept.txt').read_text()=='Keep this work' and not copy.exists()
            assert call('/api/archive?business='+bid)['items']==[]
            assert permissions.arguments('antigravity','native')==[]
            assert permissions.arguments('antigravity','full')==['--dangerously-skip-permissions']
            assert json.loads(permissions.arguments('antigravity','review')[1])['toolPermission']=='request-review'
            assert permissions.describe('pi')['choices'][0]['id']=='native' and len(permissions.choices('pi'))==1
            assert all(c['description'] and c['unrestricted']==(c['id'] in permissions.FULL_ACCESS_MODES) for kind in permissions.MODES for c in permissions.choices(kind))
            app.connection_kind='antigravity';app.preferences['connection']={'kind':'antigravity','model':'fixture','effort':''};app.preferences['harness_permissions']={'antigravity':'plan'}
            observed=[]
            def run(command,kind,cwd,env,prompt,native_id,model,effort,update,execution):
                observed.append(execution.permission);return {'reply':'Useful result','usage':{}}
            with patch.object(workspace_ui.workspace_agents,'run',side_effect=run):
                for override,expected in [('full','full'),(None,'plan')]:
                    payload={'business':bid,'chat_id':'','text':'Do useful work'}
                    if override is not None:payload['permission_mode']=override
                    job=call('/api/chat',payload,202);deadline=time.monotonic()+10
                    while app.jobs[job['id']]['status']=='working' and time.monotonic()<deadline:time.sleep(.02)
                    assert app.jobs[job['id']]['status']=='complete',app.jobs[job['id']]
                    assert observed[-1]==expected and app.preferences['harness_permissions']['antigravity']=='plan'
                def permission_cli(*args):
                    result=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/workspace_permissions.py'),'--app','antigravity','--business-id',bid,'--workspace',str(root),'--url',url,'--chat',job['chat_id'],*args],capture_output=True,text=True,encoding='utf-8',check=True)
                    return json.loads(result.stdout)
                permission_cli('--save','--mode','review')
                assert permission_cli('--current')['override']=='review' and app.preferences['harness_permissions']['antigravity']=='plan'
                permission_cli('--save','--mode','inherit');assert permission_cli('--current')['mode']=='plan'
                before=len(app.preferences['chats']);call('/api/chat',{'business':bid,'chat_id':'','text':'Do work','permission_mode':'invented'},400);assert len(app.preferences['chats'])==before
            native=base/'antigravity_fixture.py'
            native.write_text("import sys,json;assert '--print' in sys.argv;assert '--mode' in sys.argv and 'plan' in sys.argv;sys.stdin.read();print('Permission required for tool command(git): denied in headless mode',file=sys.stderr);print(json.dumps({'event':'result','result':{'conversation_id':'native-fixture','status':'SUCCESS','response':'Read-only findings'}}))",encoding='utf-8')
            updates=[]
            from workspace_execution import Execution
            execution=Execution();execution.permission='plan';execution.interactive=False
            result=workspace_ui.workspace_agents.run([sys.executable,str(native),'--print'],'antigravity',root,dict(os.environ),'Read useful context',None,'fixture','',lambda **values:updates.append(values),execution)
            assert result['reply']=='Read-only findings' and any('permission_warning' in values for values in updates),'A successful reply must not hide native approval denials'
            print('Archive and permissions passed: shared API/CLI restore, business isolation, recovery contents, draft-only overrides, inherited defaults, and native Antigravity flags.')
        finally:
            server.shutdown();server.server_close()


if __name__=='__main__':main()
