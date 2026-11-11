"""Repeated work stays scoped, current, recoverable and safe under retries and conflicts."""
import json,os,sys,tempfile,threading,subprocess
from pathlib import Path
from unittest.mock import patch
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from _common import workspace_scope,object_index
from setup import setup
from remember import remember
from workspace_ui import Workspace
import workspace_projects as projects
import workspace_collections as collections
import workspace_storage as storage
import workspace_chat_organization as organization


def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('An invalid, stale, or conflicting change was accepted')


def main():
    with tempfile.TemporaryDirectory(prefix='aura-project-results-') as t,patch.dict(os.environ):
        base=Path(t);root=base/'workspace'
        os.environ.update(BUSINESSOS_WORKSPACE=str(root),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),AURA_STATE_DIR=str(base/'state'))
        bid=setup(organization='Results studio')['business_id'];app=Workspace()
        folder=root/'work';folder.mkdir()
        p=organization.change_project(app,bid,{'name':'Funding','folder':str(folder)})['project'];ident=p['id']
        p=organization.change_project(app,bid,{'action':'edit','name':'Funding','new_name':'Funding opportunities'})['project']
        assert p['id']==ident and p['folder']==str(folder)
        assert projects.load()['projects'][0]['folder']=='work' and projects.load()['projects'][0]['relative']
        projects.bind(bid,'chat','producer-chat',[ident])
        os.environ['AURA_PRODUCER']=json.dumps({'business_id':bid,'workspace':str(root.resolve()),'kind':'chat','id':'producer-chat'})
        output=root/'attachments'/bid/'brief.txt';output.parent.mkdir(parents=True,exist_ok=True);output.write_text('Useful deliverable')
        saved=remember(bid,{'objects':[{'object_type':'Asset','content':{'asset_type':'document','business_role':'Funding brief','version':'1','status':'active','location_reference':output.relative_to(root).as_posix()}}]})
        obj=object_index(bid)[saved['objects'][0]['id']][0];assert ident in obj['extensions']['businessos']['work']['project_refs']
        assert projects.resources(app,bid,ident)['items'][0]['id']==obj['id']
        # Automatic provenance must cooperate with older goal/file controls.
        import workspace_goals as goals
        import workspace_assistants as assistants
        import workspace_context as context
        goal=goals.save(bid,{'name':'Find relevant funding','scope':'workspace'})
        projects.bind(bid,'chat','producer-chat',[ident],goal_id=goal['id'])
        new=collections.create(bid,{'key':'goal-linked-results','name':'Goal-linked results','purpose':'Keep relevant opportunities current'})
        aid=new['asset_id'];assert object_index(bid)[aid][0]['extensions']['businessos']['goal_ref']==goal['id']
        refs=[{'kind':'collection','id':new['id']}]
        projects.change(bid,{'action':'edit','id':ident,'context_refs':refs})
        agent=assistants.save(app.preferences,bid,{'name':'Funding partner','context_refs':refs})
        inherited=context.inherited(app,bid,project='Funding opportunities',assistant=agent)
        assert inherited==refs
        pointer=context.resolve(app,bid,inherited)
        assert new['id'] in pointer['text'] and 'Retrieve only relevant rows' in pointer['text']
        goals.link_asset(bid,aid,None)
        assert not object_index(bid)[aid][0]['extensions']['businessos'].get('goal_ref')
        current=collections.show(bid,new['id'])
        collections.apply(bid,new['id'],{'revision':current['revision'],'run_id':'after-explicit-unlink','items':[{'id':'proof','title':'Useful finding'}]})
        after=object_index(bid)[aid][0]['extensions']['businessos']
        assert not after.get('goal_ref') and after['work']['project_refs']==[ident]
        # Existing file/record editing also retains an explicit project unlink.
        previous=object_index(bid)[obj['id']][0]['extensions'];previous['businessos']['work']['project_refs']=[]
        remember(bid,{'objects':[{'object_ref':obj['id'],'replace_extensions':True,'content':{'extensions':previous}}]})
        remember(bid,{'objects':[{'object_ref':obj['id'],'content':{'version':'2'}}]})
        assert object_index(bid)[obj['id']][0]['extensions']['businessos']['work']['project_refs']==[]
        # Preserve the fixture's intended original association for later checks.
        previous['businessos']['work']['project_refs']=[ident]
        remember(bid,{'objects':[{'object_ref':obj['id'],'replace_extensions':True,'content':{'extensions':previous}}]})
        # Reusing a renamed project's former label creates a separate identity.
        another=organization.change_project(app,bid,{'name':'Funding'})['project']
        assert another['id']!=ident
        assert {p['name'] for p in projects.list_projects(bid)}=={'Funding','Funding opportunities'}
        assert projects.find(bid,ident)['folder']==str(folder)
        assert projects.resources(app,bid,ident)['items'][0]['id']==obj['id']
        assert projects.resources(app,bid,another['id'])['items']==[]
        assert projects.binding(bid,'chat','producer-chat')['project_refs']==[ident]
        organization.change_project(app,bid,{'name':'Funding','action':'remove'})
        c=collections.create(bid,{'key':'grants','name':'Grant shortlist','source_refs':['agency-a','agency-b']});cid=c['id']
        assert collections.create(bid,{'key':'grants','name':'Grant shortlist'})['existing']
        assert collections.show(bid,cid)['project_refs']==[ident]
        run={'revision':c['revision'],'run_id':'native-1','status':'complete','coverage':{'checked':['agency-a','agency-b']},
             'items':[{'id':'grant-1','title':'Research grant','fields':{'amount':5000,'topic':'Design'},'source_refs':[{'reference':'https://example.test/grant','published_at':'2026-11-01T10:00:00Z','data_as_of':'2026-10-01T00:00:00Z'}],'expires_at':'2026-12-01T00:00:00Z'}]}
        r=collections.apply(bid,cid,run);assert r['change_count']==1 and r['coverage']['status']=='complete'
        assert collections.apply(bid,cid,run)['replayed']
        rejects(lambda:collections.apply(bid,cid,{**run,'items':[]}))
        d=collections.show(bid,cid);collections.feedback(bid,cid,{'revision':d['revision'],'item_id':'grant-1','action':'dismiss'})
        d=collections.show(bid,cid);assert d['total']==0
        r=collections.apply(bid,cid,{'revision':d['revision'],'run_id':'native-2','status':'complete','coverage':{'checked':['agency-a','agency-b']},'items':run['items']})
        assert r['no_change_verified'] and collections.show(bid,cid)['total']==0
        d=collections.show(bid,cid)
        r=collections.apply(bid,cid,{'revision':d['revision'],'run_id':'native-3','status':'complete','coverage':{'expected':[],'scope':'attempted check','checked':['agency-a'],'failed':['agency-b']},'items':[]})
        assert r['coverage']['status']=='partial' and not r['no_change_verified']
        d=collections.show(bid,cid)
        changed={**run['items'][0],'fields':{'amount':6500,'topic':'Design'},'change_reason':'Funding amount increased'}
        r=collections.apply(bid,cid,{'revision':d['revision'],'run_id':'native-4','items':[changed]})
        assert collections.show(bid,cid)['total']==1 and r['changes'][0]['reason']=='Funding amount increased'
        d=collections.show(bid,cid);collections.feedback(bid,cid,{'revision':d['revision'],'item_id':'grant-1','action':'correct','correction':{'fields':{'amount':6000}},'note':'Confirmed amount with the agency'})
        d=collections.show(bid,cid);assert d['items'][0]['fields']['amount']==6000 and not d['items'][0]['correction_conflict']
        preview=collections.sharing_preview(bid,cid,'grant-1')['text']
        assert '6000' in preview and '6500' not in preview and 'Confirmed amount with the agency' not in preview
        other={**changed,'fields':{'amount':6500,'topic':'Architecture'}}
        collections.apply(bid,cid,{'revision':d['revision'],'run_id':'native-5','items':[other]})
        d=collections.show(bid,cid);assert d['items'][0]['fields']=={'amount':6000,'topic':'Architecture'} and not d['items'][0]['correction_conflict']
        collections.apply(bid,cid,{'revision':d['revision'],'run_id':'native-6','items':[{**other,'fields':{'amount':7000,'topic':'Architecture'}}]})
        d=collections.show(bid,cid);assert d['items'][0]['correction_conflict'] and d['items'][0]['fields']['amount']==6000
        assert collections.show(bid,cid,at=datetime(2026,12,2,tzinfo=timezone.utc))['total']==0
        # Same revision, concurrent producers: exactly one wins, the other rereads.
        basis=d['revision'];outcomes=[]
        def worker(n):
            with workspace_scope(root):
                try:collections.apply(bid,cid,{'revision':basis,'run_id':'parallel-'+str(n),'items':[{'id':'parallel-'+str(n),'title':'Concurrent finding'}]});outcomes.append('saved')
                except ValueError:outcomes.append('conflict')
        threads=[threading.Thread(target=worker,args=(n,)) for n in range(2)]
        for thread in threads:thread.start()
        for thread in threads:thread.join()
        assert sorted(outcomes)==['conflict','saved'],outcomes
        # A realistic collection stays paginated and source rows remain explicit.
        d=collections.show(bid,cid)
        batch=[{'id':'opportunity-'+str(i),'title':'Opportunity '+str(i),'summary':'Relevant source finding','fields':{'topic':'Design' if i%2 else 'Research'}} for i in range(1000)]
        r=collections.apply(bid,cid,{'revision':d['revision'],'run_id':'month-batch','status':'complete','coverage':{'checked':['agency-a','agency-b']},'items':batch})
        assert not collections.show(bid,cid)['history'] and collections.show(bid,cid,history=True)['history']
        assert len(json.dumps(collections.show(bid,cid,limit=5)))<30000
        assert collections.coverage({'status':'complete','coverage':{'scope':'No sources were checked'}},{})['status']=='unknown'
        assert collections.show(bid,cid,limit=10)['limit']==10 and len(collections.show(bid,cid,limit=10)['items'])==10
        assert collections.show(bid,cid,q='Research')['total']==501
        assert collections.apply(bid,cid,{'revision':d['revision'],'run_id':'month-batch','status':'complete','coverage':{'checked':['agency-a','agency-b']},'items':batch})['replayed']
        series=collections.create(bid,{'key':'weekly','name':'Weekly reports','mode':'series'})
        r=collections.apply(bid,series['id'],{'revision':series['revision'],'run_id':'week-1','items':[{'id':'2026-W45','title':'Week 45','summary':'Original report'}]})
        rejects(lambda:collections.apply(bid,series['id'],{'revision':r['revision'],'run_id':'week-2','items':[{'id':'2026-W45','title':'Week 45','summary':'Overwritten'}]}))
        # Project removal only archives relationships. All underlying work survives.
        projects.change(bid,{'action':'remove','id':ident})
        assert not projects.list_projects(bid) and output.exists() and collections.show(bid,cid)['total']>0
        projects.change(bid,{'action':'restore','id':ident});assert projects.find(bid,ident)['id']==ident
        assert '.businessos/projects.json' in [str(rel).replace('\\','/') for rel,*_ in storage.workspace_files(root,hashes=False)[0]]
        backup=storage.backup(root,base)
        restored=base/'restored';storage.restore(backup['path'],restored)
        with workspace_scope(restored):
            assert projects.find(bid,ident)['folder']==str(restored/'work')
            assert collections.show(bid,cid)['total']>=1000
            assert collections.show(bid,cid,item_id='grant-1')['item']['fields']['amount']==6000
        rejects(lambda:collections.show('another-business',cid))
        with workspace_scope(base/'other'):rejects(lambda:collections.show(bid,cid))
        cli=subprocess.run([sys.executable,str(ROOT/'scripts/workspace_collections.py'),'show','--business-id',bid,'--workspace',str(root),'--id',cid,'--limit','2'],capture_output=True,text=True,check=True)
        assert len(json.loads(cli.stdout)['items'])==2
        # Shared HTTP operations enforce authentication and reject an old
        # workspace selection; the ordinary UI uses these same helpers.
        from http.server import ThreadingHTTPServer
        from urllib.request import Request,urlopen
        from urllib.error import HTTPError
        from workspace_ui import handler_for
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        base_url='http://127.0.0.1:'+str(server.server_port)
        def request(route,payload=None,headers=None):
            req=Request(base_url+route,data=json.dumps(payload).encode() if payload is not None else None,headers={'X-Aura-Token':app.token,'Content-Type':'application/json',**(headers or {})})
            with urlopen(req,timeout=10) as response:return json.load(response)
        try:
            api_view=request('/api/collections?business='+bid+'&id='+cid+'&limit=2');assert len(api_view['items'])==2 and api_view['asset_id']
            renamed=request('/api/collections',{'business':bid,'id':cid,'action':'configure','revision':api_view['revision'],'name':'Relevant grant shortlist'})
            assert collections.read(bid,cid)['name']=='Relevant grant shortlist'
            for headers in ({'X-Aura-Token':'wrong'},{'X-Aura-Workspace':str(base/'other')}):
                try:request('/api/collections',{'business':bid,'id':cid,'action':'configure','revision':renamed['revision'],'name':'Wrong workspace'},headers);raise AssertionError('Invalid request accepted')
                except HTTPError as error:assert error.code in {400,403}
            assert collections.read(bid,cid)['name']=='Relevant grant shortlist'
        finally:server.shutdown();server.server_close();worker.join()
        print('Projects/results passed: stable portable links, proven output ownership, 1,000-item repeated work, scoped retrieval, coverage, retries, concurrent updates, corrections, expiry, snapshots and recoverable project archive.')


if __name__=='__main__':main()
