#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]


def req(cond,msg):
    if not cond: raise AssertionError(msg)


def controller(command,run_dir,*extra):
    p=subprocess.run([sys.executable,str(ROOT/'qualification/task_controller.py'),command,str(run_dir),*extra],cwd=ROOT,capture_output=True,text=True)
    req(p.returncode==0,f'task_controller {command} failed:\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}')
    return json.loads(p.stdout)


def main():
    with tempfile.TemporaryDirectory(prefix='aura-qualification-resume-') as td:
        root=Path(td); rr=root/'run'; ws=root/'workspace'; product=root/'product'
        (rr/'evaluator/receipts').mkdir(parents=True); (rr/'checkpoints').mkdir(); ws.mkdir(); product.mkdir()
        events=[
            {'event_id':'TASK-0001','evaluation_id':'E1','kind':'workflow_diagnostic','business_id':'atlasops','workflow_id':'content.intake.content-brief','task':'Create a useful content brief for the active business.','receipt_path':'evaluator/receipts/TASK-0001.json'},
            {'event_id':'TASK-0002','evaluation_id':'E2','kind':'workflow_diagnostic','business_id':'atlasops','workflow_id':'content.production.article','task':'Create the requested customer-facing article for the active business.','receipt_path':'evaluator/receipts/TASK-0002.json'}
        ]
        (rr/'evaluator/queue.json').write_text(json.dumps({'events':events},indent=2)+'\n')
        (rr/'run.json').write_text(json.dumps({'workspace':str(ws),'product_root':str(product)},indent=2)+'\n')

        fresh=controller('status',rr)
        req(fresh['terminal']==0 and fresh['in_progress']==0 and fresh['pending']==2,'fresh run should have two pending events')
        req(fresh['next_business_request']==events[0]['task'],'fresh run must expose the first ordinary business request as the next work')

        e1cp=rr/'checkpoints/TASK-0001'; e1cp.mkdir(parents=True)
        (e1cp/'before.json').write_text(json.dumps({'marker':'first-before'})+'\n')
        (rr/'evaluator/receipts/TASK-0001.json').write_text(json.dumps({'event_id':'TASK-0001','status':'completed'})+'\n')
        (e1cp/'after.json').write_text(json.dumps({'event_id':'TASK-0001','phase':'after'})+'\n')
        e2cp=rr/'checkpoints/TASK-0002'; e2cp.mkdir(parents=True)
        before_text=json.dumps({'marker':'preserve-this-baseline'})+'\n'; (e2cp/'before.json').write_text(before_text)

        interrupted=controller('status',rr)
        req(interrupted['terminal']==1 and interrupted['in_progress']==1 and interrupted['pending']==0,'interrupted run classification mismatch')
        req(interrupted['next_business_request']==events[1]['task'],'recovery must continue the unresolved ordinary business request rather than a hidden Workflow target')
        req(interrupted['business_id']=='atlasops','recovery lost active business identity')

        resumed=controller('start',rr)
        req(resumed['status']=='ready' and resumed['candidate_message']==events[1]['task'],'controller did not resume the same ordinary business request')
        req((e2cp/'before.json').read_text()==before_text,'recovery replaced the original before-checkpoint instead of preserving the baseline')
        req('qualification run directory' in resumed['maintainer_note'].lower(),'resume boundary must keep evaluator state hidden from the replacement candidate')

    print('qualification interruption recovery regressions passed through the single task controller path')

if __name__=='__main__': main()
