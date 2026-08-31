#!/usr/bin/env python3
"""Maintainer-side snapshots used only to observe what changed during qualification."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys
from common import now,tree_snapshot,write_json


def collect_objects(workspace,business_id):
    out=[];base=workspace/'instances'/business_id
    if not base.exists():return out
    for p in sorted(base.rglob('*.json')):
        try:data=json.loads(p.read_text())
        except Exception:continue
        vals=data if isinstance(data,list) else [data]
        for obj in vals:
            if isinstance(obj,dict) and obj.get('object_type'):
                out.append({'id':obj.get('id'),'object_type':obj.get('object_type'),'owner_system':obj.get('owner_system'),'path':str(p.relative_to(workspace)),'sha256':hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest()})
    return out


def collect_runs(workspace,business_id):
    """Record optional AURA work receipts as provenance, not as qualification requirements."""
    out=[];base=workspace/'runtime'/'runs'/business_id
    if not base.exists():return out
    for p in sorted(base.glob('*/run.json')):
        try:obj=json.loads(p.read_text())
        except Exception:continue
        out.append({'run_id':obj.get('run_id'),'method_type':obj.get('method_type'),'method_ref':obj.get('method_ref'),'contract_id':obj.get('contract_id'),'status':obj.get('status'),'path':str(p.relative_to(workspace))})
    return out


def capture_checkpoint(product_root,workspace,run_dir,event_id,phase,business_id):
    product_root=Path(product_root).resolve();workspace=Path(workspace).resolve();run_dir=Path(run_dir).resolve();env=dict(os.environ);env['BUSINESSOS_WORKSPACE']=str(workspace);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1';validation={}
    for name,cmd in {'workspace':[sys.executable,str(product_root/'scripts/validate_workspace.py')],'business':[sys.executable,str(product_root/'scripts/validate_business.py'),business_id,'--require-context']}.items():
        proc=subprocess.run(cmd,cwd=product_root,env=env,capture_output=True,text=True);validation[name]={'ok':proc.returncode==0,'returncode':proc.returncode,'stdout':proc.stdout[-4000:],'stderr':proc.stderr[-4000:]}
    snap={'event_id':event_id,'phase':phase,'business_id':business_id,'captured_at':now(),'workspace':tree_snapshot(workspace),'objects':collect_objects(workspace,business_id),'runs':collect_runs(workspace,business_id),'validation':validation};p=run_dir/'checkpoints'/event_id/f'{phase}.json';write_json(p,snap);return p,snap


def main():
    ap=argparse.ArgumentParser(description='Maintainer-side before/after snapshot for an AURA qualification task.');ap.add_argument('event_id');ap.add_argument('phase',choices=['before','after']);ap.add_argument('--business-id',required=True);ap.add_argument('--run-dir',required=True);ap.add_argument('--workspace',required=True);ap.add_argument('--product-root',required=True);a=ap.parse_args();p,_=capture_checkpoint(a.product_root,a.workspace,a.run_dir,a.event_id,a.phase,a.business_id);print(p)

if __name__=='__main__':main()
