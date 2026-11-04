#!/usr/bin/env python3
"""Outcome regressions for the demonstrated memory/portability audit failures."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import zipfile
import shutil

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))


def save(bid,ref,**content):
    from remember import remember
    return remember(bid,{'objects':[{'object_ref':ref,'content':content}]})


def worker(bid,ref,field):
    for i in range(4):save(bid,ref,**{field:str(i)})


def main():
    import _common as common
    import remember as memory
    import init_business as init
    import workspace_storage as storage
    from setup import setup
    from doctor import doctor
    from enter import prepare_work
    from forget import forget
    from persist_research_bundle import persist
    from resolve_preferences import resolve_effective_preferences
    from upsert_preference_profile import upsert
    from canonical_store import validate_canonical
    from validate_business import validate_business
    from validate_isolation import isolation_errors
    from validate_references import reference_errors
    from list_due_monitoring import summarize
    from workspace_support import human_error,ErrorDetails,prepare

    with tempfile.TemporaryDirectory(prefix='aura-audit-repairs-') as td:
        base=Path(td);ws=base/'workspace';ws.mkdir()
        with patch.dict(os.environ,{'BUSINESSOS_WORKSPACE':str(ws),'BUSINESSOS_WORKSPACE_CONFIG':str(base/'pointer.json'),
                                   'AURA_STATE_DIR':str(base/'local')}):
            bid='audit-fixture';init.init_business(bid,'Audit fixture')
            created=memory.remember(bid,{'objects':[{'object_type':'Asset','content':{
                'asset_type':'document','version':'0','business_role':'Explain ast_node structures','status':'draft'}}]})
            ref=created['objects'][0]['id']
            asset=ws/created['objects'][0]['path']
            (ws/'attachments'/bid).mkdir(parents=True)
            logo=ws/'attachments'/bid/'src_logo.svg';logo.write_text('<svg/>',encoding='utf-8')
            save(bid,ref,location_reference=logo.relative_to(ws).as_posix())
            assert not reference_errors(bid),'Prose/filenames were interpreted as canonical relationships'
            try:save(bid,ref,extensions={'source_ref':'src_missing'})
            except ValueError:pass
            else:raise AssertionError('An actual broken reference was accepted')

            # Independent processes must retain both final field updates.
            env=dict(os.environ,PYTHONUTF8='1')
            children=[subprocess.Popen([sys.executable,'-X','utf8',str(Path(__file__)),
                       '--worker',bid,ref,field],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                      for field in ('version','business_role')]
            for child in children:
                out,err=child.communicate(timeout=60)
                assert child.returncode==0,err.decode('utf-8','replace')
            current=json.loads(asset.read_text(encoding='utf-8'))
            assert current['version']==current['business_role']=='3','A successful concurrent update was lost'

            # A failed writer must finish rollback before another writer commits.
            entered=threading.Event();release=threading.Event();real_validate=memory.validate_business
            def validation(*args,**kwargs):
                if threading.current_thread().name.startswith('failed-writer'):
                    entered.set();assert release.wait(10)
                    return ['injected audit failure'],[],{}
                return real_validate(*args,**kwargs)
            with patch.object(memory,'validate_business',side_effect=validation),ThreadPoolExecutor(1,thread_name_prefix='failed-writer') as first,ThreadPoolExecutor(1) as second:
                failed=first.submit(save,bid,ref,version='rejected')
                assert entered.wait(10)
                successful=second.submit(save,bid,ref,business_role='kept after rollback')
                try:
                    assert not successful.done(),'A write bypassed an active transaction'
                finally:release.set()
                try:failed.result(10)
                except ValueError:pass
                else:raise AssertionError('Injected invalid transaction committed')
                successful.result(10)
            assert json.loads(asset.read_text(encoding='utf-8'))['business_role']=='kept after rollback'

            # Legacy duplicated source IDs are local identities, never global owners.
            init.init_business('other-fixture','Other fixture')
            bundle={'sources':[{'id':'src_legacy_shared','source_reference':'User supplied audit brief',
                'captured_text':'A fixture statement.','acquisition_method':'user_provided'}],
                'observations':[{'statement':'A fixture statement.','source_indexes':[0]}]}
            for organization in (bid,'other-fixture'):persist(organization,bundle)
            assert not isolation_errors()[0],'Valid local evidence was falsely classified as cross-business'
            for organization in (bid,'other-fixture'):assert not validate_business(organization,True)[0]
            other_ref=next(o['id'] for o,p in common.iter_instance_objects('other-fixture') if o['object_type']=='Business')
            try:memory.remember(bid,{'objects':[{'object_ref':ref,'content':{},'lineage_refs':[other_ref]}]})
            except ValueError:pass
            else:raise AssertionError('Actual cross-organization relationship was accepted')

            upsert(bid,'House style','business',bid,{'writing':{'dialect':'British English'}})
            entry=prepare_work('Write a short invitation to our workshop.',bid)
            assert entry['retrieval']['preferences']['effective_preferences']['writing']['dialect']=='British English'
            upsert(bid,'Alternative','business',bid,{'writing':{'dialect':'American English'}})
            overridden=resolve_effective_preferences(bid,task_preferences={'writing':{'dialect':'Australian English'}})
            assert overridden['effective_preferences']['writing']['dialect']=='Australian English' and not overridden['conflicts']
            assert resolve_effective_preferences(bid,fail_on_conflict=False)['conflicts'],'Unresolved defaults disappeared'

            # Unknown monitoring state must not become an all-clear.
            profiles=ws/'instances'/bid/'intelligence/source-profiles';broken=profiles/'sprof_broken.json'
            broken.write_text('{broken',encoding='utf-8')
            monitoring=summarize(bid)
            assert not monitoring['complete'] and monitoring['read_diagnostics']
            broken.unlink()
            business=json.loads((ws/'instances'/bid/'context/business.json').read_text(encoding='utf-8'))
            business['created_at']='not-a-date'
            try:validate_canonical('Business',business)
            except ValueError:pass
            else:raise AssertionError('An invalid date was accepted')

            # Interrupted identity writes do not publish an incomplete organization.
            original=init.write_canonical;count=0
            def interrupted(*args,**kwargs):
                nonlocal count
                count+=1
                if count==2:raise OSError('injected second identity write failure')
                return original(*args,**kwargs)
            with patch.object(init,'write_canonical',side_effect=interrupted):
                try:init.init_business('retry-fixture','Retry fixture')
                except OSError:pass
                else:raise AssertionError('Injected setup failure did not run')
            assert not (ws/'instances/retry-fixture').exists()
            ready=setup(workspace=ws,organization='Retry fixture',write_link=False)
            assert ready['status']=='ready',ready
            command=ready['visual_workspace']['command']
            assert command[command.index('--workspace')+1]==str(ws)
            # Recognizable old interrupted setup is repaired, without probing invalid state first.
            (ws/'instances/retry-fixture/context/business.json').unlink()
            before=set((ws/'instances/retry-fixture').rglob('*.json'))
            assert doctor('retry-fixture')['status']=='not_ready'
            assert set((ws/'instances/retry-fixture').rglob('*.json'))==before,'Doctor left a probe in invalid state'
            assert setup(workspace=ws,organization='Retry fixture',write_link=False)['status']=='ready'

            # Default backup excludes Windows junctions and POSIX directory links.
            outside=base/'outside';outside.mkdir();(outside/'sentinel.txt').write_text('external fixture',encoding='utf-8')
            link=ws/'attachments'/bid/'linked'
            if os.name=='nt':
                ps="New-Item -ItemType Junction -Path '"+str(link).replace("'","''")+"' -Target '"+str(outside).replace("'","''")+"' | Out-Null"
                subprocess.run(['powershell','-NoProfile','-NonInteractive','-Command',ps],check=True,capture_output=True)
            else:link.symlink_to(outside,target_is_directory=True)
            try:
                destination=base/'backups';destination.mkdir()
                result=storage.backup(ws,destination,False)
                with zipfile.ZipFile(result['path']) as archive:
                    assert not any('sentinel.txt' in name for name in archive.namelist())
            finally:
                if os.name=='nt':link.rmdir()
                else:link.unlink()

            # Locale-independent core operations, even without UTF-8 startup mode.
            save(bid,ref,business_role='日本語の資料')
            done=subprocess.run([sys.executable,'-X','utf8=0','-E','-s','-B',str(ROOT/'scripts/forget.py'),bid,ref],
                                env=env,capture_output=True,timeout=30)
            assert done.returncode==0,done.stderr.decode('utf-8','replace')

            # Friendly messages retain redacted technical evidence in reviewed reports.
            errors=ErrorDetails()
            assert human_error(PermissionError('Reload this page to reconnect to AURA.'))=='Reload this page to reconnect to AURA.'
            try:raise AttributeError("Cannot set properties of null (setting 'innerHTML')")
            except AttributeError as exc:
                ident=errors.record(exc,'/api/other')
                assert 'innerHTML' not in human_error(exc)
            report=prepare({'kind':'troubleshooting','title':'Fixture','description':'Fixture error',
                'include_environment':True,'browser_errors':[{'type':'TypeError','message':'innerHTML failure'}]},
                {'recent_errors':errors.snapshot()},base/'reports',persist=False)['report']
            assert report['environment']['recent_errors'][0]['id']==ident
            assert report['environment']['browser_errors'][0]['message']=='innerHTML failure'
            assert prepare({'kind':'feature','title':'Fixture','description':'Fixture','include_environment':False},
                None,base/'reports',persist=False)['report']['environment'] is None
    if shutil.which('node'):
        subprocess.run(['node',str(ROOT/'tests/workspace_errors_ui.cjs'),str(ROOT/'interface/app.js')],check=True)
    print('Audit repairs passed: concurrent saves/rollback, organization isolation, reference semantics, preferences, monitoring, recoverable setup, junction exports, UTF-8 and readable diagnostics')


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--worker':worker(*sys.argv[2:])
    else:main()
