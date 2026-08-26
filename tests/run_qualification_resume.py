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
        (rr/'candidate').mkdir(parents=True); (rr/'candidate-results').mkdir(); (rr/'checkpoints').mkdir(); ws.mkdir()
        events=[
            {'event_id':'E1','kind':'contract_acceptance','business_id':'qa-test','contract_id':'content.intake.content-brief','receipt_path':'candidate-results/E1.json'},
            {'event_id':'E2','kind':'contract_acceptance','business_id':'qa-test','contract_id':'content.intake.work-request','receipt_path':'candidate-results/E2.json'}
        ]
        (rr/'candidate/queue.json').write_text(json.dumps({'events':events},indent=2)+'\n')
        (rr/'run.json').write_text(json.dumps({'workspace':str(ws)},indent=2)+'\n')

        d=run_status(rr)
        s=d['summary']; req(s['terminal']==0 and s['pending']==2,'fresh run should have two pending events')
        req(s['first_unfinished']['event_id']=='E1' and s['first_unfinished']['state']=='pending','fresh run must resume at first event')

        e1cp=rr/'checkpoints/E1'; e1cp.mkdir(parents=True)
        (e1cp/'before.json').write_text(json.dumps({'runs':[]})+'\n')
        (rr/'candidate-results/E1.json').write_text(json.dumps({'event_id':'E1','status':'completed'})+'\n')
        (e1cp/'after.json').write_text(json.dumps({'event_id':'E1','phase':'after'})+'\n')
        e2cp=rr/'checkpoints/E2'; e2cp.mkdir(parents=True)
        (e2cp/'before.json').write_text(json.dumps({'runs':[]})+'\n')
        run_dir=ws/'runtime/runs/qa-test/run_interrupted'; run_dir.mkdir(parents=True)
        (run_dir/'run.json').write_text(json.dumps({'run_id':'run_interrupted','business_id':'qa-test','contract_id':'content.intake.work-request','status':'active'})+'\n')

        d=run_status(rr,'--write-instructions'); s=d['summary']
        req(s['terminal']==1 and s['in_progress']==1,'interrupted run classification mismatch')
        first=s['first_unfinished']; req(first['event_id']=='E2' and first['state']=='in_progress','must resume at interrupted second event')
        req(any(r['run_id']=='run_interrupted' for r in first['candidate_event_runs']),'active event Run must be surfaced for recovery')
        resume=rr/'candidate/RESUME-INSTRUCTIONS.md'; req(resume.exists(),'resume instructions were not written')
        text=resume.read_text(); req('do not redo terminal events' in text.lower(),'resume instructions must forbid repeating terminal work')
        req('run_interrupted' in text and 'resume compatible active/incomplete Run state' in text,'resume instructions must tell candidate to reuse active Run')

    print('qualification interruption recovery regressions passed')

if __name__=='__main__': main()
