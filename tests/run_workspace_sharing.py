"""Sharing journeys and integrity boundaries, using disposable businesses only."""
from pathlib import Path
import json
import os
import sys
import tempfile
import zipfile
import threading
import subprocess
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def main():
    import workspace_sharing as share
    from setup import setup
    from remember import remember
    from validate_business import validate_business
    with tempfile.TemporaryDirectory(prefix='aura-sharing-') as directory, patch.dict(os.environ):
        base = Path(directory)
        source, target, store = base / 'Head office', base / 'Local business', base / 'state'
        os.environ.update(BUSINESSOS_WORKSPACE=str(source), BUSINESSOS_WORKSPACE_CONFIG=str(base / 'source-pointer.json'), LOCALAPPDATA=str(base / 'local'))
        bid = setup(organization='Head office')['business_id']
        report = source / 'attachments' / bid / 'work' / 'Training' / 'welcome.txt'
        report.parent.mkdir(parents=True)
        report.write_text('A reusable introduction.', encoding='utf-8')
        (report.parent / '.env').write_text('DO_NOT_SHARE=secret')
        result = remember(bid, {'objects':[{'object_type':'Asset', 'content':{
            'asset_type':'training', 'business_role':'Welcome guide', 'version':'1', 'status':'draft',
            'location_reference':report.relative_to(source).as_posix()}}]})
        asset = next(p for p in (source / 'instances' / bid / 'assets').glob('*.json'))
        asset_id = json.loads(asset.read_text())['id']
        # Target has independent identity and facts, even when names or IDs overlap.
        os.environ.update(BUSINESSOS_WORKSPACE=str(target), BUSINESSOS_WORKSPACE_CONFIG=str(base / 'target-pointer.json'))
        local = setup(organization='Local business')['business_id']
        identity = target / 'instances' / local / 'context/business.json'
        identity_before = identity.read_bytes()
        os.environ['BUSINESSOS_WORKSPACE'] = str(source)
        inventory = share.public_inventory(source, bid)
        assert not any('.env' in r['key'] for r in inventory['items'])
        selection = ['record:' + asset_id]
        saved = share.save_selection(source, bid, 'New location', selection, 'Add your address and opening hours. Adapt the introduction for your location.')
        renamed = share.save_selection(source, bid, 'Location starter', selection, 'Revised notes.', saved['id'])
        assert renamed['id']==saved['id'] and len(share.history(source,bid)['selections'])==1
        for invalid in ('', 'missing-selection'):
            try:
                share.save_selection(source,bid,'Location starter',selection,selection_id=invalid)
                raise AssertionError('Duplicate name or stale selection identity was accepted')
            except ValueError:
                assert share.history(source,bid)['selections'][0]['note']=='Revised notes.'
        package = share.prepare(source, bid, selection, 'New location', 'Add your address and hours.', store)
        assert len(package['items']) == 2 and any(i['kind']=='file' and i['supporting'] for i in package['items'])
        archive = share.export_package(package['id'], base / 'Starter.zip', store)
        assert archive['verified']
        # Exported locations remain discoverable without duplicating the ZIP. Internal
        # sharing metadata is expected, while private exclusions are informational.
        found = share.discover_packages(source,bid,folder=base)
        assert any(r['path']==archive['path'] and r['name']=='New location' for r in found['items'])
        assert str(base / 'Starter.zip') in share.read(share.metadata(source,bid)/'packages.json')
        inventory = share.public_inventory(source,bid)
        assert not any('.sharing' in n for n in inventory['notes']+inventory['excluded'])
        assert not inventory['notes'] and any('.env' in n for n in inventory['excluded'])
        with zipfile.ZipFile(base/'Not a sharing package.zip','w') as z:z.writestr('AURA-BACKUP.json','{}')
        (base/'Unreadable.zip').write_text('not a zip')
        assert len(share.discover_packages(source,bid,folder=base)['items'])==1
        share.remember_package(source,bid,base/'A moved package.zip')
        with patch.object(Path,'home',return_value=base/'profile'):
            recent = share.discover_packages(source,bid)
        assert any(r['path']==archive['path'] for r in recent['items'])
        assert any('missing or unreadable' in n for n in recent['notes'])
        # Explicitly connected locations work through the same save function as the UI.
        linked = base/'Linked project';linked.mkdir();(linked/'guide.txt').write_text('Linked material.')
        locations = [{'path':str(linked),'name':'Linked project'}]
        linked_key = next(r['key'] for r in share.public_inventory(source,bid,locations)['items'] if r.get('external'))
        share.save_selection(source,bid,'Linked starter',[linked_key],locations=locations)
        with zipfile.ZipFile(archive['path']) as z:
            assert all('.env' not in n for n in z.namelist())
        loaded = share.import_package(archive['path'], store)
        preview = share.review(loaded['id'], target, local, store=store)
        assert preview['counts']['add'] == 2
        added = share.apply(loaded['id'], store=store)
        assert added['added'] == 2 and identity.read_bytes() == identity_before
        assert share.review(loaded['id'], target, local, store=store)['counts']['already'] == 2
        notes_only = share.prepare(source,bid,selection,'New location','A revised setup note.',store)
        note_preview = share.review(notes_only['id'],target,local,store=store)
        assert note_preview['notes_changed'] and note_preview['counts']['already']==2
        note_result = share.apply(notes_only['id'],store=store)
        assert share.imported_detail(target,local,note_result['receipt'])['note']=='A revised setup note.'
        assert share.undo(target,local,note_result['receipt'],True)['status']=='undone'
        os.environ['BUSINESSOS_WORKSPACE'] = str(target)
        errors, _, _ = validate_business(local)
        assert not errors, errors
        # The imported original Asset is support material, not another business's canonical state.
        assert not (target / 'instances' / bid).exists()
        imported = target / next(r['target'] for r in preview['items'] if r['kind']=='file')
        assert imported.read_bytes() == report.read_bytes()
        # Local changes survive both repeat imports and undo requests.
        imported.write_text('A locally adapted introduction.')
        errors, _, _ = validate_business(local)
        assert not errors, errors
        assert share.review(loaded['id'], target, local, store=store)['counts']['local'] == 1
        assert not share.undo(target, local, added['receipt'])['can_undo']
        report.write_text('Updated standard introduction.')
        updated = share.prepare(source, bid, selection, 'New location', store=store)
        assert share.review(updated['id'], target, local, store=store)['counts']['conflict'] == 1
        conflict_result = share.apply(updated['id'], True, store)
        assert conflict_result['added'] == 0 and conflict_result['comparison']
        assert imported.read_text() == 'A locally adapted introduction.'
        conflict_detail = share.imported_detail(target, local, conflict_result['receipt'])
        assert any(i['incoming_path'] and (target / i['incoming_path']).read_text() == 'Updated standard introduction.' for i in conflict_detail['items'])
        assert share.undo(target, local, conflict_result['receipt'], True)['status'] == 'undone'
        imported.write_text('A reusable introduction.')
        update_preview = share.review(updated['id'], target, local, store=store)
        assert update_preview['counts']['update'] == 1
        updated_result = share.apply(updated['id'], True, store)
        assert imported.read_text() == 'Updated standard introduction.'
        assert not share.undo(target, local, added['receipt'])['can_undo'], 'Old undo may not undo a later update'
        assert share.undo(target, local, updated_result['receipt'], True)['status'] == 'undone'
        assert imported.read_text() == 'A reusable introduction.'
        assert share.undo(target, local, added['receipt'], True)['status'] == 'undone'
        assert not imported.exists() and identity.read_bytes() == identity_before
        # Preview is invalidated if target work changes, and source changes invalidate local snapshots.
        fresh = share.prepare(source, bid, selection, store=store)
        fresh_review = share.review(fresh['id'], target, local, store=store)
        occupied = target / fresh_review['items'][0]['target']
        occupied.parent.mkdir(parents=True, exist_ok=True); occupied.write_text('Keep this local work')
        try:
            share.apply(fresh['id'], store=store)
            raise AssertionError('Changed destination was accepted')
        except ValueError:
            assert occupied.read_text() == 'Keep this local work'
        report.write_text('Changed after source review.')
        try:
            share.export_package(fresh['id'], base / 'Stale.zip', store)
            raise AssertionError('Stale source was accepted')
        except ValueError:
            assert not (base / 'Stale.zip').exists()
        occupied.unlink()
        # Archived snapshots do not need the original computer and can start a new business.
        new = share.import_package(archive['path'], store)
        new_root = base / 'A new franchise'
        new_preview = share.review(new['id'], new_root, new_name='Downtown location', store=store)
        created = share.apply(new['id'], store=store)
        new_identity = share.business(new_root, new_preview['business'])
        assert new_identity['name'] == 'Downtown location' and new_identity['name'] != 'Head office'
        assert created['added'] == 2
        # Same source copied into two businesses in one data folder keeps canonical IDs isolated.
        os.environ['BUSINESSOS_WORKSPACE'] = str(target)
        from init_business import init_business
        from validate_isolation import isolation_errors
        init_business('second-location', 'Second location')
        share.review(new['id'], target, 'second-location', store=store)
        share.apply(new['id'], store=store)
        first_again = share.import_package(archive['path'], store)
        share.review(first_again['id'], target, local, store=store)
        share.apply(first_again['id'], store=store)
        assert not isolation_errors()[0], isolation_errors()[0]
        # CLI uses the same inventory and review contract without changing active workspace.
        cmd = subprocess.run([sys.executable,str(ROOT / 'scripts/workspace_sharing.py'),'--store',str(store),
                              'list',str(source),bid],capture_output=True,text=True,check=True)
        assert any(r['key']=='record:'+asset_id for r in json.loads(cmd.stdout)['items'])
        cmd = subprocess.run([sys.executable,str(ROOT/'scripts/workspace_sharing.py'),'discover',str(source),bid,'--folder',str(base)],capture_output=True,text=True,check=True)
        assert any(r['path']==archive['path'] for r in json.loads(cmd.stdout)['items'])
        # Real HTTP routes: package -> current business review -> apply -> detail/undo.
        from workspace_ui import Workspace, handler_for
        app = Workspace(settings_file=base / 'ui/settings.json')
        server = ThreadingHTTPServer(('127.0.0.1',0),handler_for(app))
        worker = threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        def api(route, data=None, scope=None):
            request = Request(f'http://127.0.0.1:{server.server_port}'+route,
                data=json.dumps(data).encode() if data is not None else None,
                headers={'X-Aura-Token':app.token,'X-Aura-Workspace':scope or str(target),
                         **({'Content-Type':'application/json'} if data is not None else {})})
            with urlopen(request,timeout=60) as response:
                return json.load(response)
        try:
            assert api('/api/sharing?business='+local)['business'] == local
            http_saved = api('/api/sharing/selection',{'business':local,'name':'Reusable selection','keys':['record:'+share.business(target,local)['id']]})
            http_edited = api('/api/sharing/selection',{'business':local,'selection_id':http_saved['id'],'name':'Renamed selection','keys':http_saved['keys'],'note':'New notes'})
            assert http_edited['id']==http_saved['id'] and http_edited['note']=='New notes'
            assert any(r['path']==archive['path'] for r in api('/api/sharing/discover',{'business':local,'path':str(base)})['items'])
            pkg = api('/api/sharing/package',{'business':local,'path':archive['path']})
            assert archive['path'] in share.read(share.metadata(target,local)/'packages.json')
            reviewed = api('/api/sharing/review',{'business':local,'id':pkg['id'],'path':str(target),'target_business':local})
            assert reviewed['counts']['already'] == 2
            assert api('/api/sharing/apply',{'business':local,'id':pkg['id']})['status'] == 'unchanged'
            try:
                api('/api/sharing/review',{'business':'second-location','id':pkg['id'],'path':str(target),'target_business':'second-location'})
                raise AssertionError('A different business reused a UI review')
            except HTTPError as error:
                assert error.code == 400
            try:
                api('/api/sharing/package',{'business':local,'path':archive['path']},str(source))
                raise AssertionError('A stale browser tab imported into another workspace')
            except HTTPError as error:
                assert error.code == 400
        finally:
            server.shutdown();server.server_close();worker.join()
        # Unexpected write failure rolls back; a killed writer leaves a recoverable receipt.
        interrupted_root = base / 'Recovery location'
        recovery_pkg = share.import_package(archive['path'], store)
        share.review(recovery_pkg['id'],interrupted_root,new_name='Recovery location',store=store)
        original_copy = share._copy_file
        def broken_copy(src,dest):
            if 'shared' in Path(dest).parts:
                raise OSError('Injected copy failure')
            return original_copy(src,dest)
        try:
            with patch.object(share,'_copy_file',broken_copy):
                share.apply(recovery_pkg['id'],store=store)
            raise AssertionError('Failed copy was reported as success')
        except OSError:
            assert not list((interrupted_root / 'instances/recovery-location/intelligence/sources').glob('src_shared_*.json'))
            assert not share.history(interrupted_root,'recovery-location')['imports']
        share.review(recovery_pkg['id'],interrupted_root,'recovery-location',store=store)
        class SimulatedDisconnect(BaseException):
            pass
        counter = [0]
        def disconnected_copy(src,dest):
            counter[0] += 1
            if counter[0] == 2:
                raise SimulatedDisconnect()
            return original_copy(src,dest)
        try:
            with patch.object(share,'_copy_file',disconnected_copy):
                share.apply(recovery_pkg['id'],store=store)
            raise AssertionError('Disconnect was not simulated')
        except SimulatedDisconnect:
            receipt = share.history(interrupted_root,'recovery-location')['imports'][0]
            assert receipt['status']=='adding'
            assert share.undo(interrupted_root,'recovery-location',receipt['id'],True)['status']=='undone'
        with share.destination_lock(target):
            try:
                with share.destination_lock(target):
                    raise AssertionError('A second writer acquired the same destination')
            except ValueError:
                pass
        # A tampered archive, excluded credential file and traversal never reach the destination.
        with zipfile.ZipFile(archive['path']) as z:
            members = {n:z.read(n) for n in z.namelist()}
        damaged = base / 'Damaged.zip'
        with zipfile.ZipFile(damaged, 'w') as z:
            for name, content in members.items():
                z.writestr(name, b'changed' if name.startswith('files/') else content)
        for bad in [damaged]:
            try:
                share.import_package(bad, store)
                raise AssertionError('Damaged archive was accepted')
            except ValueError:
                pass
        for name in ['../outside', 'files/C:/secret', 'files/x\\secret', 'files/CON.txt']:
            try:
                share.safe(name)
                raise AssertionError('Unsafe path was accepted')
            except ValueError:
                pass
        # Locks survive as harmless files; the OS releases ownership, including on crashes.
        with share.destination_lock(target):
            pass
    print('workspace sharing journeys passed')


if __name__ == '__main__':
    main()
