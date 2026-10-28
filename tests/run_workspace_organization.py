"""Real-file consolidation, interruption, conflicts, isolation, and recovery."""
from pathlib import Path
import json,os,shutil,sys,tempfile,time
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
import threading
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))


def main():
    import workspace_organization as org
    import workspace_catalog as catalog
    from setup import setup
    from remember import remember
    with tempfile.TemporaryDirectory(prefix='aura-organize-test-') as tmp,patch.dict(os.environ):
        base=Path(tmp);source=base/'Original';store=base/'machine';target=base/'Documents/AURA Workspaces/Organized'
        os.environ.update(BUSINESSOS_WORKSPACE=str(source),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),
            LOCALAPPDATA=str(base/'local'),AURA_WORKSPACES_HOME=str(base/'Documents/AURA Workspaces'))
        bid=setup(organization='Lantern')['business_id']
        site=source/'projects/site';site.mkdir(parents=True)
        (site/'index.html').write_text('<img src="logo.png">');(site/'logo.png').write_bytes(b'actual image fixture')
        remember(bid,{'objects':[{'object_type':'Asset','content':{'asset_type':'website','business_role':'Our site',
            'version':'1','status':'draft','location_reference':'projects/site/index.html'}}]})
        other=base/'Another copy';shutil.copytree(source,other)
        (other/'projects/site/index.html').write_text('<h1>Alternative</h1><img src="logo.png">')
        os.environ['BUSINESSOS_WORKSPACE']=str(other)
        remember(bid,{'objects':[{'object_type':'Objective','content':{'name':'A useful distinct goal'}}]})
        original={p:p.read_bytes() for p in source.rglob('*') if p.is_file()}
        review=org.plan(source,[other],target,store=store)
        assert review['counts']['needs_review']>=1, 'Changed website must remain a reviewable alternative'
        assert all(p.read_bytes()==v for p,v in original.items())
        try:org.apply(review['id'],store,cancel=lambda:True)
        except ValueError:pass
        else:raise AssertionError('Cancel ignored')
        assert not target.exists()
        result=org.apply(review['id'],store)
        assert result['status']=='complete'
        assert (target/'projects/site/index.html').read_bytes()==(source/'projects/site/index.html').read_bytes()
        imported=list((target/'attachments'/bid/'imports').glob('*/projects/site/index.html'))
        assert len(imported)==1 and (imported[0].parent/'logo.png').read_bytes()==(site/'logo.png').read_bytes()
        objectives=[json.loads(p.read_text()) for p in (target/'instances'/bid/'context/objectives').glob('*.json')]
        assert any(o['name']=='A useful distinct goal' for o in objectives)
        assert org.apply(review['id'],store)['status']=='complete','Retry created another import'
        assert all(p.read_bytes()==v for p,v in original.items())
        # A changed source invalidates the entire old review before activation.
        stale=org.plan(source,[],base/'Stale',store=store)
        (site/'new.txt').write_text('New work after preview')
        try:org.apply(stale['id'],store)
        except ValueError as exc:assert 'changed' in str(exc)
        else:raise AssertionError('Stale source was accepted')
        assert not (base/'Stale').exists()
        (site/'new.txt').unlink()
        abandoned=org.discard(stale['id'],store)
        assert Path(abandoned['path']).is_dir()
        assert org.recover(abandoned['id'],'restore',store)['status']=='restored'
        retirement=org.retirement_review(review['id'],store,references=[str(site/'index.html')])
        assert not retirement['items'][0]['eligible'],'A dependency was ignored'
        entry=org.retire(review['id'],source,store=store)
        assert not source.exists() and Path(entry['path']).is_dir()
        org.recover(entry['id'],'restore',store)
        assert source.is_dir()
        # New work in recovery disables automatic removal.
        entry=org.retire(review['id'],source,7,store)
        (Path(entry['path'])/'new.txt').write_text('Retain this new work')
        try:org.recover(entry['id'],'remove',store)
        except ValueError as exc:assert 'changed' in str(exc)
        else:raise AssertionError('Changed recovery copy removed')
        assert next(r for r in org.recovery(store) if r['id']==entry['id'])['status']=='changed'
        org.recover(entry['id'],'restore',store)
        # Expiry removes only an unchanged, explicitly retired copy.
        os.environ['BUSINESSOS_WORKSPACE']=str(target)
        expired=org.retire(review['id'],other,7,store)
        expired_record=store/'organization/recovery'/(expired['id']+'.json')
        expiry=json.loads(expired_record.read_text());expiry['expires']=time.time()-1;catalog.write_json(expired_record,expiry)
        assert not org.expire(store)
        assert not Path(expired['path']).exists() and target.is_dir() and source.is_dir()
        # Private exclusions prevent retiring the containing folder.
        (source/'.env').write_text('TEST_ONLY_SECRET=not-for-export')
        private=org.plan(source,[],base/'Private copy',store=store);org.apply(private['id'],store)
        assert not org.retirement_review(private['id'],store)['items'][0]['eligible']
        assert not (base/'Private copy/.env').exists()
        # Distinct businesses retain their own context; explicit grouping works
        # across different IDs without overwriting the starting Business record.
        third=base/'Separate';os.environ['BUSINESSOS_WORKSPACE']=str(third)
        third_bid=setup(organization='Another business')['business_id']
        separate=org.plan(source,[third],base/'Separate result',store=store)
        org.apply(separate['id'],store)
        assert (base/'Separate result/instances'/third_bid/'context/business.json').is_file()
        grouped=org.plan(source,[third],base/'Grouped result',{str(third)+'|'+third_bid:bid},store)
        org.apply(grouped['id'],store)
        assert not (base/'Grouped result/instances'/third_bid).exists()
        # An unreadable workspace is visible as needing attention.
        broken=base/'Broken';(broken/'.businessos').mkdir(parents=True)
        (broken/'.businessos/workspace.json').write_text('{broken')
        assert any(r['kind']=='attention' for r in catalog.discover([broken])['items'])
        # Real HTTP background review/apply and activation rollback. No model calls.
        os.environ['BUSINESSOS_WORKSPACE']=str(third)
        from workspace_ui import Workspace,handler_for
        from _common import workspace_root
        app=Workspace(settings_file=store/'view.json')
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        def api(route,data=None):
            request=Request(f'http://127.0.0.1:{server.server_port}'+route,data=json.dumps(data).encode() if data is not None else None,
                headers={'X-Aura-Token':app.token,**({'Content-Type':'application/json'} if data is not None else {})})
            with urlopen(request,timeout=60) as response:return json.load(response)
        def finished():
            deadline=time.monotonic()+60
            while time.monotonic()<deadline:
                job=api('/api/organization')['job']
                if job['status']!='working':return job
                time.sleep(.05)
            raise AssertionError('Background operation did not finish')
        try:
            api('/api/organization/plan',{'primary':str(third),'sources':[],'destination':str(base/'HTTP result')})
            job=finished();assert job['status']=='complete',job
            prepared=api('/api/request',{'business':third_bid,'text':'Review my organization recommendation.','organization_id':job['result']['id']})
            assert 'read-only organization review' in prepared['text'] and prepared['text'].endswith('Review my organization recommendation.')
            api('/api/organization/apply',{'id':job['result']['id']})
            job=finished();assert job['status']=='complete',job
            assert workspace_root().resolve()==(base/'HTTP result').resolve()
            previous=workspace_root().resolve();prior_selection=(store/'workspace-selection.json').read_bytes()
            with patch('workspace_ui.Workspace',side_effect=OSError('Controlled initialization failure')):
                try:app.open_workspace(str(source))
                except OSError:pass
                else:raise AssertionError('Initialization failure was hidden')
            assert workspace_root().resolve()==previous and (store/'workspace-selection.json').read_bytes()==prior_selection
            custom=third/'custom-view';custom.mkdir()
            for name in ('index.html','app.js','style.css'):(custom/name).write_text('Owned custom view fixture')
            custom_plan=org.plan(third,[],base/'Custom result',store=store);org.apply(custom_plan['id'],store)
            app.open_workspace(str(third));app.static=custom;app.launch_extra=['--interface-dir',str(custom)]
            app.open_workspace(str(base/'Custom result'))
            assert app.static==(base/'Custom result/custom-view') and str(app.static) in app.launch_extra
        finally:server.shutdown();server.server_close();thread.join()
        print('Workspace organization passed: real projects, distinct memory, alternatives, retry, changed inputs, dependencies, recovery, and private exclusions.')


def preview(directory):
    """Disposable local browser fixture, with no native agents or provider calls."""
    base=Path(directory).resolve();base.mkdir(parents=True,exist_ok=True)
    os.environ.update(BUSINESSOS_WORKSPACE=str(base/'Workspaces/Studio demo'),BUSINESSOS_WORKSPACE_CONFIG=str(base/'pointer.json'),
        LOCALAPPDATA=str(base/'local'),AURA_WORKSPACES_HOME=str(base/'Workspaces'))
    from setup import setup
    from remember import remember
    from _common import workspace_root
    bid=setup(organization='Studio demo')['business_id'];root=Path(workspace_root());site=root/'projects/website';site.mkdir(parents=True)
    (site/'index.html').write_text('<h1>Studio demo</h1><img src="logo.svg">')
    (site/'logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><circle r="10"/></svg>')
    remember(bid,{'objects':[{'object_type':'Asset','content':{'asset_type':'website','business_role':'Our first website','version':'1','status':'draft','location_reference':'projects/website'}}]})
    copy=base/'Workspaces/Studio earlier work';shutil.copytree(root,copy)
    (copy/'projects/website/index.html').write_text('<h1>An alternative message</h1><img src="logo.svg">')
    import workspace_ui,workspace_catalog
    workspace_ui.installed_agents=lambda:[]
    discover=workspace_catalog.discover
    workspace_catalog.discover=lambda roots,**kw:discover([base/'Workspaces'],**kw)
    app=workspace_ui.Workspace(settings_file=base/'machine/view.json');app.preferences['seen']=[bid];app.save_preferences()
    server=ThreadingHTTPServer(('127.0.0.1',0),workspace_ui.handler_for(app))
    print(json.dumps({'port':server.server_port,'business':bid,'root':str(base)}),flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--preview':preview(sys.argv[2])
    else:main()
