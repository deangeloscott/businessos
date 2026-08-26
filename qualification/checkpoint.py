#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys
from common import now, run_root_from_env, tree_snapshot, workspace_from_env, write_json

def collect_objects(workspace,business_id):
    out=[]; base=workspace/'instances'/business_id
    if not base.exists(): return out
    for p in sorted(base.rglob('*.json')):
        try: data=json.loads(p.read_text())
        except Exception: continue
        vals=data if isinstance(data,list) else [data]
        for obj in vals:
            if isinstance(obj,dict) and obj.get('object_type'):
                out.append({'id':obj.get('id'),'object_type':obj.get('object_type'),'owner_system':obj.get('owner_system'),'path':str(p.relative_to(workspace)),'sha256':hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest()})
    return out

def collect_runs(workspace,business_id):
    out=[]; base=workspace/'runtime'/'runs'/business_id
    if not base.exists(): return out
    for p in sorted(base.glob('*/run.json')):
        try: obj=json.loads(p.read_text())
        except Exception: continue
        out.append({'run_id':obj.get('run_id'),'contract_id':obj.get('contract_id'),'status':obj.get('status'),'path':str(p.relative_to(workspace))})
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('event_id'); ap.add_argument('phase',choices=['before','after']); ap.add_argument('--business-id',required=True); a=ap.parse_args()
    ws=workspace_from_env(); rr=run_root_from_env()
    env=dict(os.environ); env['BUSINESSOS_WORKSPACE']=str(ws); env['PYTHONDONTWRITEBYTECODE']='1'
    validation={}
    for name,cmd in {'workspace':[sys.executable,str(Path(__file__).resolve().parents[1]/'scripts/validate_workspace.py')],'business':[sys.executable,str(Path(__file__).resolve().parents[1]/'scripts/validate_business.py'),a.business_id,'--require-context']}.items():
        proc=subprocess.run(cmd,cwd=Path(__file__).resolve().parents[1],env=env,capture_output=True,text=True)
        validation[name]={'ok':proc.returncode==0,'returncode':proc.returncode,'stdout':proc.stdout[-4000:],'stderr':proc.stderr[-4000:]}
    snap={'event_id':a.event_id,'phase':a.phase,'business_id':a.business_id,'captured_at':now(),'workspace':tree_snapshot(ws),'objects':collect_objects(ws,a.business_id),'runs':collect_runs(ws,a.business_id),'validation':validation}
    p=rr/'checkpoints'/a.event_id/f'{a.phase}.json'; write_json(p,snap); print(p)
if __name__=='__main__': main()
