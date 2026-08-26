#!/usr/bin/env python3
from pathlib import Path
import argparse, json, subprocess, sys, tempfile, uuid
from build_suite import build
from common import ROOT, now, write_json
from prepare_run import copy_product, init_business

def lane_instructions(product_root,run_dir,workspace,lane,events):
    return f'''# AURA Concurrent Qualification — Lane {lane}

You are operator/candidate lane {lane} in a two-operator shared-workspace AURA qualification run. Another independent AI/harness is operating concurrently on the same business and workspace.

Product root: `{product_root}`
Workspace: `{workspace}`
Run directory: `{run_dir}`
Your queue: `{run_dir/f'candidate-{lane.lower()}/queue.json'}`

Retain:
```bash
export BUSINESSOS_WORKSPACE='{workspace}'
export AURA_QUALIFICATION_RUN='{run_dir}'
export BUSINESSOS_OPERATOR_REF='qualification-{lane.lower()}'
```

Process your {len(events)} events continuously. For every event, create before/after checkpoints with `qualification/checkpoint.py`, execute the real business work through AURA, write the receipt to the run-relative `receipt_path`, and immediately continue. Expect overlapping evidence and problems. Reuse/deduplicate canonical state, preserve semantic ownership and operator provenance, and never resolve concurrency by editing AURA product source or overwriting another operator's work blindly.
'''

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run-root'); ap.add_argument('--run-id'); a=ap.parse_args()
    suite=build(); run_id=a.run_id or ('aura-concurrency-'+uuid.uuid4().hex[:10]); root=Path(a.run_root).expanduser().resolve() if a.run_root else Path(tempfile.gettempdir())/'aura-qualification-runs'; run_dir=root/run_id
    if run_dir.exists(): raise SystemExit(f'Run already exists: {run_dir}')
    try:
        run_dir.relative_to(ROOT.resolve()); raise SystemExit('Qualification run root must be outside the AURA product tree')
    except ValueError: pass
    product_root=copy_product(ROOT,run_dir/'product'); subprocess.run([sys.executable,str(product_root/'scripts/generate_registry.py')],cwd=product_root,check=True,capture_output=True,text=True)
    workspace=run_dir/'workspace'; workspace.mkdir(parents=True); init_business(product_root,workspace,'atlasops-saas')
    events=[]
    for m in suite.get('concurrency_missions',[]):
        e={'event_id':m['id'],'kind':'concurrency_mission','business_id':'qa-atlasops-saas','fixture':m['fixture'],'contract_id':None,'task':m['task'],'competitive_profile':'concurrency','required_output':{'actual_output_not_description':True},'receipt_path':f"candidate-results/{m['id']}.json",'lane':m['lane']}; events.append(e)
    for sub in ('candidate','candidate-a','candidate-b','candidate-results','checkpoints','evaluator'): (run_dir/sub).mkdir(parents=True,exist_ok=True)
    master={'format_version':'1.0','run_id':run_id,'profile':'concurrency','events':events,'event_count':len(events)}
    write_json(run_dir/'master-queue.json',master); write_json(run_dir/'candidate/queue.json',master)
    for lane in ('A','B'):
        lane_events=[e for e in events if e['lane']==lane]; ld=run_dir/f'candidate-{lane.lower()}'; write_json(ld/'queue.json',{'format_version':'1.0','run_id':run_id,'lane':lane,'events':lane_events,'event_count':len(lane_events)}); (ld/'RUN-INSTRUCTIONS.md').write_text(lane_instructions(product_root,run_dir,workspace,lane,lane_events),encoding='utf-8')
    write_json(run_dir/'evaluator/suite.json',suite); write_json(run_dir/'run.json',{'run_id':run_id,'created_at':now(),'product_root':str(product_root),'workspace':str(workspace),'profile':'concurrency','event_count':len(events),'status':'prepared'})
    print(json.dumps({'run_id':run_id,'run_dir':str(run_dir),'product_root':str(product_root),'workspace':str(workspace),'lane_a':str(run_dir/'candidate-a/RUN-INSTRUCTIONS.md'),'lane_b':str(run_dir/'candidate-b/RUN-INSTRUCTIONS.md')},indent=2))
if __name__=='__main__': main()
