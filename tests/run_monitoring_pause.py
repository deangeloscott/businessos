#!/usr/bin/env python3
"""Regression for pause/resume semantics versus actual scheduler state."""
from pathlib import Path
import json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from list_due_monitoring import summarize

BID='monitoring-pause-regression'

def fail(msg):raise AssertionError(msg)

def run(args,env):
    p=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,env=env,capture_output=True,text=True)
    if p.returncode!=0:fail(f"command failed: {args}\n{p.stdout}\n{p.stderr}")
    return p

def main():
    prior=os.environ.get('BUSINESSOS_WORKSPACE');tmp=Path(tempfile.mkdtemp(prefix='aura-monitoring-pause-'));env=dict(os.environ);env['BUSINESSOS_WORKSPACE']=str(tmp);env['PYTHONDONTWRITEBYTECODE']='1'
    try:
        os.environ['BUSINESSOS_WORKSPACE']=str(tmp);(tmp/'instances'/BID).mkdir(parents=True)
        created=run([
            ROOT/'scripts/upsert_source_profile.py',BID,'--source-reference','https://example.com/watch','--display-name','Example Watch',
            '--subject-key','example_watch','--subject-name','Example Watch','--watch-status','active',
            '--cadence-mode','recurring','--cadence-expression','weekly','--cadence-source','user','--next-check-at','2026-08-28T00:00:00Z'
        ],env)
        profile_id=json.loads(created.stdout)['id']
        run([
            ROOT/'scripts/register_scheduler_binding.py','local','sched_pause_regression','--business-id',BID,'--target-kind','subject','--subject-key','example_watch',
            '--executor-kind','harness_scheduler','--executor-ref','host-schedule-1','--cadence-expression','weekly','--verified-at','2026-08-29T00:00:00Z'
        ],env)
        before=summarize(BID,'local','2026-08-29T01:00:00Z');row=before['subjects'][0]
        if row.get('execution_status')!='active_automatic':fail(f'expected active automatic before pause: {row}')

        pause=run([ROOT/'scripts/set_monitoring_watch_status.py',BID,'paused','--subject-key','example_watch'],env)
        changed=json.loads(pause.stdout).get('updated',[])
        if not changed or changed[0].get('id')!=profile_id:fail('pause helper did not update the existing SourceProfile')
        path=tmp/'instances'/BID/'intelligence'/'source-profiles'/f'{profile_id}.json';obj=json.loads(path.read_text())
        if obj.get('watch_status')!='paused' or obj.get('subject_key')!='example_watch' or not obj.get('monitoring_cadence'):fail('pause changed/deleted durable monitoring intelligence')
        mismatch=summarize(BID,'local','2026-08-29T01:00:00Z');row=mismatch['subjects'][0]
        if row.get('execution_status')!='configuration_mismatch_active_scheduler' or not row.get('configuration_mismatch'):fail(f'active host scheduler was hidden after semantic pause: {row}')
        if row.get('due') or row.get('needs_refresh_on_start'):fail('paused semantic watch remained due')

        # Simulate successful host scheduler pause and then update its AURA receipt.
        run([
            ROOT/'scripts/register_scheduler_binding.py','local','sched_pause_regression','--business-id',BID,'--target-kind','subject','--subject-key','example_watch',
            '--executor-kind','harness_scheduler','--executor-ref','host-schedule-1','--cadence-expression','weekly','--status','paused'
        ],env)
        reconciled=summarize(BID,'local','2026-08-29T01:00:00Z');row=reconciled['subjects'][0]
        if row.get('execution_status')!='paused' or row.get('configuration_mismatch'):fail(f'paused semantic/host state did not reconcile: {row}')
        print('monitoring pause regression passed: durable intelligence preserved, active-scheduler mismatch exposed, host pause reconciled')
    finally:
        if prior is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior
        shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
