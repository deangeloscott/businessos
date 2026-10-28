"""One upgrade/copy/export/restore journey, without models or provider accounts."""
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
import hashlib
import json
import os
import shutil
import sys
import tempfile
import threading
import zipfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / 'scripts'))


def main():
    import workspace_catalog as catalog
    import workspace_storage as storage
    from workspace_ui import Workspace, handler_for
    from workspace_startup import state_dir
    from setup import setup
    from remember import remember
    with tempfile.TemporaryDirectory(prefix='aura-continuity-') as directory, patch.dict(os.environ):
        base = Path(directory)
        source = base / 'Downloads/older-aura/inner-folder'
        os.environ.update(BUSINESSOS_WORKSPACE=str(source), BUSINESSOS_WORKSPACE_CONFIG=str(base / 'product-link.json'),
            LOCALAPPDATA=str(base / 'local'), AURA_WORKSPACES_HOME=str(base / 'Documents/AURA Workspaces'))
        bid = setup(organization='Café business')['business_id']
        profile_path = source / '.businessos/workspace.json'
        profile = json.loads(profile_path.read_text());profile['profile']='organization';catalog.write_json(profile_path,profile)
        (source / 'scripts').mkdir()
        (source / 'VERSION').write_text('0.1.12')
        report = source / 'reports/research.txt'
        report.parent.mkdir()
        report.write_text('Real saved research from a native app.',encoding='utf-8')
        legacy = source / 'deliverables/site/index.html'
        legacy.parent.mkdir(parents=True)
        legacy.write_text('<h1>Our actual website</h1>')
        (legacy.parent / '.htaccess').write_text('DirectoryIndex index.html')
        ads = base / 'Brand assets'
        ads.mkdir();(ads / 'ad.txt').write_text('A reusable creative.')
        (ads / '.env').write_text('SECRET_MUST_NOT_EXPORT=example')
        (source / '.env').write_text('SECRET_MUST_NOT_EXPORT=example')
        saved = remember(bid,{'objects':[{'object_type':'Asset','content':{
            'asset_type':'research report','business_role':'Useful evidence','version':'1','status':'draft',
            'location_reference':str(report)}}]})
        remember(bid,{'objects':[{'object_type':'Asset','content':{
            'asset_type':'creative','business_role':'An external creative','version':'1','status':'draft',
            'location_reference':str(ads / 'ad.txt')}}]})
        alias = base / 'Downloads/newer-aura'
        (alias / '.businessos').mkdir(parents=True)
        (alias / '.businessos/workspace.json').write_text(json.dumps({'workspace_root':str(source)}))
        copy = base / 'Downloads/separate-copy'
        shutil.copytree(source,copy)
        before = {p:p.read_bytes() for p in source.rglob('*') if p.is_file()}
        found = catalog.discover([base / 'Downloads'])
        workspaces = [r for r in found['items'] if r['kind']=='workspace']
        assert len(workspaces)==2, 'Same business IDs in different folders were merged'
        assert any(str(alias) in r['aliases'] for r in workspaces)
        assert all(p.read_bytes()==value for p,value in before.items()), 'Discovery wrote to existing work'
        assert catalog.candidates(source.parent)['items'][0]['kind']=='workspace'
        app = Workspace()
        app.preferences['appearance']='dark'
        app.preferences['file_locations']={bid:[{'id':'brand-files','name':'Brand assets','kind':'folder','path':str(ads)}]}
        app.save_preferences(portable=True)
        new_download = base / 'A fresh AURA download'
        (new_download / 'scripts').mkdir(parents=True)
        (new_download / 'VERSION').write_text('0.1.99')
        assert catalog.launch_workspace(new_download)==source, 'A new download lost the chosen workspace'
        server=ThreadingHTTPServer(('127.0.0.1',0),handler_for(app))
        worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        def api(route,data=None):
            request=Request(f'http://127.0.0.1:{server.server_port}'+route,
                data=json.dumps(data).encode() if data is not None else None,
                headers={'X-Aura-Token':app.token,**({'Content-Type':'application/json'} if data is not None else {})})
            with urlopen(request,timeout=90) as response:return json.load(response)
        try:
            preview=api('/api/workspaces/preview',{'path':str(source.parent)})
            assert preview['items'][0]['businesses'][0]['id']==bid
            assert any(f['name']=='research.txt' for f in api('/api/files?business='+bid)['items']), 'Native saved Asset was invisible'
            target=catalog.default_home() / bid
            original_asset=(source / 'instances' / bid / 'assets').glob('*.json')
            original_asset={p:p.read_bytes() for p in original_asset}
            app.preferences['chats']=[{'id':'old-chat','business_id':bid,'agent':'pi','native_id':'saved-native-chat'}]
            app.preferences['active_chats']={bid:'old-chat'}
            moved=api('/api/workspaces/relocate',{'path':str(target)})
            assert moved['verified'] and moved['source_retained'] and app.state(bid)['workspace']==str(target)
            assert json.loads((target / '.businessos/workspace.json').read_text())['profile']=='organization'
            assert app.preferences['chats'][0]['workspace']==str(source) and not app.preferences['active_chats']
            assert all(p.read_bytes()==value for p,value in original_asset.items()), 'Copy rewrote the original memory'
            assert (target / 'reports/research.txt').read_bytes()==report.read_bytes()
            assert (target / 'deliverables/site/index.html').read_bytes()==legacy.read_bytes()
            assert app.preferences['appearance']=='dark' and app.preferences['file_locations'][bid][0]['id']=='brand-files'
            assert catalog.launch_workspace(new_download)==target
            plans=api('/api/workspaces/backup-preview',{'include_linked':False})
            assert plans['links'] and all(not r['included'] for r in plans['links'])
            exports=base / 'Backups';exports.mkdir()
            backup=api('/api/workspaces/backup',{'path':str(exports),'include_linked':True})
            with zipfile.ZipFile(backup['path']) as archive:
                assert 'deliverables/site/index.html' in archive.namelist()
                assert 'deliverables/site/.htaccess' in archive.namelist()
                assert 'reports/research.txt' in archive.namelist()
                assert not any(name.endswith('.env') for name in archive.namelist())
                assert not any('SECRET_MUST_NOT_EXPORT' in archive.read(name).decode('utf-8',errors='ignore') for name in archive.namelist())
            restore_parent=base / 'Another computer';restore_parent.mkdir()
            restored=api('/api/workspaces/restore',{'archive':backup['path'],'path':str(restore_parent / 'Restored work')})
            api('/api/workspaces/open',{'path':restored['path']})
            restored_root=Path(restored['path'])
            assert json.loads((restored_root / '.businessos/workspace.json').read_text())['profile']=='organization'
            assert app.preferences['appearance']=='dark'
            restored_link=app.preferences['file_locations'][bid][0]
            assert Path(restored_link['path']).is_relative_to(restored_root)
            assert (Path(restored_link['path']) / 'ad.txt').read_bytes()==(ads / 'ad.txt').read_bytes()
            # A native app uses normal AURA persistence, without UI registration.
            native=restored_root / 'attachments' / bid / 'work/native-result.txt'
            native.parent.mkdir(parents=True,exist_ok=True);native.write_text('A useful native CLI result.')
            remember(bid,{'objects':[{'object_type':'Asset','content':{'asset_type':'document',
                'business_role':'Native app work','location_reference':native.relative_to(restored_root).as_posix(),
                'version':'1','status':'draft'}}]})
            assert any(f['name']==native.name for f in api('/api/files?business='+bid)['items'])
            # Repair a moved folder without changing its saved identity.
            elsewhere=base / 'Assets moved';ads.rename(elsewhere)
            api('/api/workspaces/open',{'path':str(source)})
            assert api('/api/files?business='+bid)['locations'][0]['missing']
            api('/api/locations',{'business':bid,'replace':'brand-files','path':str(elsewhere)})
            assert app.preferences['file_locations'][bid][0]['id']=='brand-files'
            assert not api('/api/files?business='+bid)['locations'][0]['missing']
            assert not api('/api/files?business='+bid)['missing_assets'], 'Folder repair left a child Asset pointing at its old location'
            # Routine UI receipts must not overwrite a native change to shared links.
            view=source / storage.VIEW_FILE
            changed=json.loads(view.read_text());changed['appearance']='light';catalog.write_json(view,changed)
            digest=hashlib.sha256(view.read_bytes()).hexdigest()
            app.save_preferences()
            assert hashlib.sha256(view.read_bytes()).hexdigest()==digest and app.state(bid)['appearance']=='light'
        finally:
            server.shutdown();server.server_close();worker.join()
        missing=base / 'Disconnected drive/Workspace'
        catalog.remember(missing,'Café business')
        assert catalog.launch_workspace(new_download)==missing and not missing.exists()
        os.environ['BUSINESSOS_WORKSPACE']=str(missing)
        unavailable=Workspace()
        assert unavailable.state()['workspace_missing'] and not missing.exists(), 'Missing work was silently replaced'
        print('Workspace discovery, upgrade, verified copy, full export/restore, native output visibility, and repair passed.')


if __name__=='__main__':main()
