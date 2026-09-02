#!/usr/bin/env python3
from _common import *
from process_extensions import resolve_effective
import argparse,json

def main():
    ap=argparse.ArgumentParser(description='Resolve a canonical or organization-local AURA Workflow with applicable ProcessExtensions.');ap.add_argument('business_id');ap.add_argument('contract_id');ap.add_argument('--team-ref');ap.add_argument('--role-ref');ap.add_argument('--operator-ref');ap.add_argument('--json',action='store_true');ap.add_argument('--show',action='store_true');a=ap.parse_args()
    try:path,meta,content,exts=resolve_effective(a.contract_id,a.business_id,a.team_ref,a.role_ref,a.operator_ref)
    except ValueError as e:raise SystemExit(str(e))
    result={'business_id':a.business_id,'workflow_id':a.contract_id,'contract_id':a.contract_id,'path':str(path.relative_to(ROOT)) if path else None,'owner_system':meta.get('owner_system'),'type':meta.get('type'),'process_extension_ids':[x['id'] for x in exts],'local_workflow':bool(meta.get('local_workflow') or meta.get('local_playbook')),'executable':False,'boundary':'AURA resolves operating knowledge; the active model/harness owns tools, external Skills, orchestration, providers, permissions, and execution.'}
    if a.show:print(content,end='' if content.endswith('\n') else '\n')
    elif a.json:print(json.dumps(result,indent=2))
    else:print(result['path'] or f"process-extension:{result['process_extension_ids'][0]}")
if __name__=='__main__':main()
