#!/usr/bin/env python3
from _common import *
from innovation_common import load_package,validate_package,validate_schema
import argparse,json

def build_index(directory,exchange_id='local-aura-exchange',output=None):
    directory=Path(directory)
    if not directory.exists() or not directory.is_dir():raise ValueError(f'Exchange package directory not found: {directory}')
    entries=[];seen=set()
    for p in sorted(directory.iterdir()):
        if p.suffix.lower() not in {'.json','.zip'}:continue
        try:pkg=load_package(p);validate_package(pkg,require_export_approval=True)
        except Exception:continue
        if pkg['package_id'] in seen:continue
        seen.add(pkg['package_id']);proc=pkg['process'];entries.append({'package_id':pkg['package_id'],'innovation_fingerprint':pkg['innovation_fingerprint'],'title':proc['title'],'purpose':proc['purpose'],'owner_system':proc['owner_system'],'target_workflow_id':proc.get('target_workflow_id'),'local_workflow_id':proc.get('local_workflow_id'),'detail_level':pkg['detail_level'],'identity_level':pkg['identity_level'],'aura_version':pkg['aura_version'],'artifact_reference':p.name,'reported_evidence':pkg.get('evidence_summary')})
    idx={'format_version':'1.0','exchange_id':exchange_id,'generated_at':now(),'entries':entries};validate_schema('InnovationExchangeIndex',idx);out=Path(output) if output else directory/'innovation-index.json';out.write_text(json.dumps(idx,indent=2)+'\n');return idx,out

def main():
    ap=argparse.ArgumentParser(description='Build a portable searchable Innovation Exchange index from approved Workflow-knowledge packages.');ap.add_argument('directory');ap.add_argument('--exchange-id',default='local-aura-exchange');ap.add_argument('--output');a=ap.parse_args()
    try:idx,out=build_index(a.directory,a.exchange_id,a.output)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'exchange_id':idx['exchange_id'],'entries':len(idx['entries']),'output':str(out)},indent=2))
if __name__=='__main__':main()
