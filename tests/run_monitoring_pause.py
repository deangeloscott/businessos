#!/usr/bin/env python3
"""Regression for semantic monitoring pause/resume without scheduler bindings."""
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
        created=run([ROOT/'scripts/upsert_source_profile.py',BID,'--source-reference','https://example.com/watch','--display-name','Example Watch','--subject-key','example_watch','--subject-name','Example Watch','--watch-status','active','--cadence-mode','recurring','--cadence-expression','weekly','--cadence-source','user','--next-check-at','2026-08-28T00:00:00Z'],env)
        profile_id=json.loads(created.stdout)['id']
        before=summarize(BID,'2026-08-29T01:00:00Z');row=before['subjects'][0]
        if not row.get('due'):fail(f'active overdue watch was not semantically due: {row}')
        pause=run([ROOT/'scripts/set_monitoring_watch_status.py',BID,'paused','--subject-key','example_watch'],env)
        changed=json.loads(pause.stdout).get('updated',[])
        if not changed or changed[0].get('id')!=profile_id:fail('pause helper did not update existing SourceProfile')
        path=tmp/'instances'/BID/'intelligence'/'source-profiles'/f'{profile_id}.json';obj=json.loads(path.read_text())
        if obj.get('watch_status')!='paused' or obj.get('subject_key')!='example_watch' or not obj.get('monitoring_cadence'):fail('pause changed/deleted durable monitoring intelligence')
        paused=summarize(BID,'2026-08-29T01:00:00Z');row=paused['subjects'][0]
        if row.get('due'):fail('paused semantic watch remained due')
        if (tmp/'.businessos/environments').exists():fail('semantic pause created deprecated runtime/scheduler state')
        run([ROOT/'scripts/set_monitoring_watch_status.py',BID,'active','--subject-key','example_watch'],env)
        resumed=summarize(BID,'2026-08-29T01:00:00Z');row=resumed['subjects'][0]
        if not row.get('due'):fail('resumed overdue watch did not become semantically due again')
        print('monitoring pause regression passed: pause/resume preserves durable intent without AURA-owned scheduler state')
    finally:
        if prior is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior
        shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__':main()
