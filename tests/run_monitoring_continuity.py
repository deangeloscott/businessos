#!/usr/bin/env python3
"""Regression for semantic monitoring continuity without AURA-owned runtime machinery."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from list_due_monitoring import summarize

BID='monitoring-continuity'

def req(cond,msg):
    if not cond:raise AssertionError(msg)

def run(cmd,env,ok=True):
    p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
    if ok and p.returncode!=0:raise AssertionError(f"command failed: {' '.join(map(str,cmd))}\n{p.stdout}\n{p.stderr}")
    return p

def main():
    retired=[
        'core/providers/registry.json','core/schemas/runtime/capability-binding.schema.json','core/schemas/runtime/scheduler-bindings.schema.json',
        'scripts/preflight_capabilities.py','scripts/resolve_capability.py','scripts/bootstrap_environment.py','scripts/manage_local_capabilities.py',
        'scripts/register_scheduler_binding.py','deployment/operator-profile.json','docs/provider-resolution.md','docs/host-capability-discovery.md'
    ]
    for rel in retired:req(not (ROOT/rel).exists(),f'retired runtime/provider artifact still exists: {rel}')
    catalog=json.loads((ROOT/'core/capabilities/catalog.json').read_text())
    ids={x.get('id') for x in catalog.get('capabilities',[])}
    req('web.search' in ids and 'web.fetch' in ids,'provider-neutral capability vocabulary was lost')
    guide=(ROOT/'docs/adding-a-capability.md').read_text()
    for phrase in ['not permissions','active model/harness/user decides','does not inventory host tools']:
        req(phrase in guide,f'capability guidance missing boundary: {phrase}')

    tmp=Path(tempfile.mkdtemp(prefix='aura-monitoring-continuity-'));env={**os.environ,'BUSINESSOS_WORKSPACE':str(tmp),'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'};prior=os.environ.get('BUSINESSOS_WORKSPACE')
    try:
        os.environ['BUSINESSOS_WORKSPACE']=str(tmp)
        init=run([sys.executable,str(ROOT/'scripts/init_business.py'),BID,'--name','Monitoring Continuity'],env)
        upsert=[sys.executable,str(ROOT/'scripts/upsert_source_profile.py'),BID]
        pricing=json.dumps({'signal':'pricing changes','mode':'recurring','expression':'monthly','source':'user','next_check_at':'2026-08-28T00:00:00Z','notification_mode':'material_changes_only'})
        run(upsert+['--source-reference','https://example.com/competitor','--display-name','Example Competitor','--subject-key','example_competitor','--subject-name','Example Competitor','--subject-kind','organization','--subject-relationship','competitor','--watch-status','active','--source-modality','text','--monitoring-question','What materially changed?','--cadence-mode','recurring','--cadence-expression','weekly','--cadence-source','user','--notification-mode','material_changes_only','--notification-source','user','--signal-cadence-json',pricing,'--last-checked-at','2026-08-20T00:00:00Z','--next-check-at','2026-08-28T00:00:00Z'],env)
        data=summarize(BID,'2026-08-29T00:00:00Z')
        req(data.get('due_count')==1,f'semantic due state not preserved: {data}')
        row=data['subjects'][0]
        req(row.get('cadences') and 'weekly' in row['cadences'][0],'source cadence missing')
        req(any(x.get('signal')=='pricing changes' and x.get('expression')=='monthly' for x in row.get('signal_cadences',[])),'signal cadence missing')
        req('runtime/harness' in data.get('rule',''),'summary does not state runtime boundary')
        blocked=run(upsert+['--source-reference','https://example.com/competitor','--cadence-mode','recurring','--cadence-expression','monthly','--cadence-source','inferred'],env,ok=False)
        req(blocked.returncode!=0 and 'user-specified' in (blocked.stdout+blocked.stderr),'inferred cadence overwrote explicit user intent')
        status=run([sys.executable,str(ROOT/'scripts/monitoring_status.py'),BID,'--at','2026-08-29T00:00:00Z'],env).stdout
        req('Runtime scheduling is external to AURA' in status,'human monitoring view implies AURA owns scheduling')
        req(not (tmp/'.businessos/environments').exists(),'monitoring created deprecated runtime binding state')
        print('AURA monitoring continuity regression passed: semantic intent persists without provider/scheduler runtime machinery')
    finally:
        if prior is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior
        shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
