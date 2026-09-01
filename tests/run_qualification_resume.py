#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]


def req(cond,msg):
    if not cond: raise AssertionError(msg)


def run_status(run_dir,*extra):
    p=subprocess.run([sys.executable,str(ROOT/'qualification/resume_status.py'),str(run_dir),'--json',*extra],cwd=ROOT,capture_output=True,text=True)
    req(p.returncode==0,f'resume_status failed:\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
    return json.loads(p.stdout)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-qualification-resume-') as td:
        rr=Path(td)/'run'; ws=Path(td)/'workspace'
        (rr/'evaluator/receipts').mkdir(parents=True); (rr/'checkpoints').mkdir(); ws.mkdir()
        events=[
            {'event_id':'TASK-0001','evaluation_id':'E1','kind':'contract_acceptance','business_id':'atlasops','contract_id':'content.intake.content-brief','task':'Create a useful content brief for the active business.','receipt_path':'evaluator/receipts/TASK-0001.json'},
            {'event_id':'TASK-0002','evaluation_id':'E2','kind':'contract_acceptance','business_id':'atlasops','contract_id':'content.production.article','task':'Create the requested customer-facing article for the active business.','receipt_path':'evaluator/receipts/TASK-0002.json'}
        ]
        (rr/'evaluator/queue.json').write_text(json.dumps({'events':events},indent=2)+'\n'); (rr/'run.json').write_text(json.dumps({'workspace':str(ws)},indent=2)+'\n')

        d=run_status(rr); s=d['summary']; req(s['terminal']==0 and s['pending']==2,'fresh run should have two pending events'); req(s['first_unfinished']['event_id']=='TASK-0001' and s['first_unfinished']['state']=='pending','fresh run must resume at first event')

        e1cp=rr/'checkpoints/TASK-0001'; e1cp.mkdir(parents=True); (e1cp/'before.json').write_text(json.dumps({'runs':[]})+'\n'); (rr/'evaluator/receipts/TASK-0001.json').write_text(json.dumps({'event_id':'TASK-0001','status':'completed'})+'\n'); (e1cp/'after.json').write_text(json.dumps({'event_id':'TASK-0001','phase':'after'})+'\n')
        e2cp=rr/'checkpoints/TASK-0002'; e2cp.mkdir(parents=True); (e2cp/'before.json').write_text(json.dumps({'runs':[]})+'\n')
        run_dir=ws/'runtime/runs/atlasops/run_interrupted'; run_dir.mkdir(parents=True); (run_dir/'run.json').write_text(json.dumps({'run_id':'run_interrupted','business_id':'atlasops','contract_id':'content.production.article','status':'active'})+'\n')

        d=run_status(rr,'--write-instructions'); s=d['summary']; req(s['terminal']==1 and s['in_progress']==1,'interrupted run classification mismatch')
        first=s['first_unfinished']; req(first['event_id']=='TASK-0002' and first['state']=='in_progress','must resume at interrupted second task'); req(any(r['run_id']=='run_interrupted' for r in first['event_runs']),'active task Run must be surfaced maintainer-side for recovery')
        recovery=rr/'evaluator/RECOVERY.md'; req(recovery.exists(),'maintainer recovery instructions were not written'); text=recovery.read_text().lower(); req('candidate/model should still receive only the normal aura product/workspace and an ordinary business request' in text,'recovery must preserve blind candidate boundary'); req('create the requested customer-facing article' in text,'recovery must preserve original ordinary business request'); req(not (rr/'candidate').exists(),'recovery created candidate-visible qualification files')

    print('qualification interruption recovery regressions passed with evaluator-side recovery')

if __name__=='__main__': main()
