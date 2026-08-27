#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, subprocess, sys, tempfile, uuid
from build_suite import build
from common import ROOT, now, product_snapshot, write_json
RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())
from prepare_run import copy_product, init_business, fixture_business_id


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run-root'); ap.add_argument('--run-id'); a=ap.parse_args()
    suite=build(); run_id=a.run_id or ('aura-concurrency-'+uuid.uuid4().hex[:10]); root=Path(a.run_root).expanduser().resolve() if a.run_root else Path(tempfile.gettempdir())/'aura-qualification-runs'; run_dir=root/run_id
    if run_dir.exists(): raise SystemExit(f'Run already exists: {run_dir}')
    try: run_dir.relative_to(ROOT.resolve()); raise SystemExit('Qualification run root must be outside the AURA product tree')
    except ValueError: pass
    product_root=copy_product(ROOT,run_dir/'product'); env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1'; subprocess.run([sys.executable,str(product_root/'scripts/generate_registry.py')],cwd=product_root,env=env,check=True,capture_output=True,text=True)
    workspace=run_dir/'workspace'; workspace.mkdir(parents=True); (run_dir/'evaluator').mkdir(); (run_dir/'checkpoints').mkdir()
    init_business(product_root,workspace,'atlasops-saas',run_dir/'evaluator'); bid=fixture_business_id('atlasops-saas')
    events=[]
    lane_counts={'A':0,'B':0}
    for m in suite.get('concurrency_missions',[]):
        lane=m['lane']; lane_counts[lane]=lane_counts.get(lane,0)+1; eid=f'TASK-{lane}-{lane_counts[lane]:04d}'
        events.append({'event_id':eid,'evaluation_id':m['id'],'kind':'concurrency_mission','business_id':bid,'fixture':m['fixture'],'contract_id':None,'task':m['task'],'competitive_profile':'concurrency','required_output':{'actual_output_not_description':True},'rubric_dimensions':[x['id'] for x in RUBRICS['base']]+RUBRICS['profiles']['concurrency_system'],'receipt_path':f'evaluator/receipts/{eid}.json','lane':lane})
    queue={'format_version':'2.0','run_id':run_id,'profile':'concurrency','events':events,'event_count':len(events)}
    write_json(run_dir/'evaluator/queue.json',queue); write_json(run_dir/'evaluator/suite.json',suite); write_json(run_dir/'evaluator/preparation.json',{'profile':'concurrency','prepared_at':now(),'candidate_blind':True})
    baseline=product_snapshot(product_root); write_json(run_dir/'evaluator/product-snapshot.json',baseline)
    write_json(run_dir/'run.json',{'run_id':run_id,'created_at':now(),'product_root':str(product_root),'workspace':str(workspace),'profile':'concurrency','event_count':len(events),'status':'prepared','execution_status':'prepared','qualification_status':'NOT_EVALUATED','benchmark_context_seeded':True,'product_snapshot_digest':baseline['digest'],'candidate_blind':True})
    lane_requests={lane:[{'controller_event_id':e['event_id'],'business_request':e['task'],'start_command':f'python3 qualification/task_controller.py start "{run_dir}" --event-id {e["event_id"]}','finish_command':f'python3 qualification/task_controller.py finish "{run_dir}" --event-id {e["event_id"]}'} for e in events if e['lane']==lane] for lane in ('A','B')}
    print(json.dumps({'run_id':run_id,'run_dir':str(run_dir),'product_root':str(product_root),'workspace':str(workspace),'candidate_blind':True,'lane_requests':lane_requests,'candidate_exposure':'Each model receives only the shared AURA product/workspace, its operator identity, and the business_request text for its lane. Do not expose controller event IDs or evaluator files to the model.'},indent=2))

if __name__=='__main__': main()
