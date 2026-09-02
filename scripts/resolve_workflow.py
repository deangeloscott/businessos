#!/usr/bin/env python3
"""Resolve one installed or organization-local AURA Workflow."""
from _common import *
import argparse,json


def resolve_workflow(workflow_id):
    matches=[]
    for path in contract_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        if meta.get('id')==workflow_id:matches.append((path,meta))
    if not matches:raise ValueError(f'Unknown Workflow id: {workflow_id}')
    if len(matches)>1:raise ValueError(f'Duplicate Workflow id: {workflow_id}')
    if matches[0][1].get('type')!='workflow':raise ValueError(f'{workflow_id} is not an AURA Workflow')
    return matches[0]


def _result(workflow_id,meta,path=None,business_id=None,extensions=None):
    return {'workflow_id':workflow_id,'business_id':business_id,'path':path,'owner_system':meta.get('owner_system'),'type':meta.get('type'),'process_extension_ids':[x['id'] for x in (extensions or [])],'local_workflow':bool(meta.get('local_workflow')),'executable':False,'boundary':'Workflow knowledge helps the active intelligence do the job; the model/harness owns tool choice, external Skills, orchestration, providers, permissions, and execution.'}


def main():
    ap=argparse.ArgumentParser(description='Resolve an AURA Workflow. With --business-id, include applicable organization ProcessExtensions/local Workflows.');ap.add_argument('workflow_id');ap.add_argument('--business-id');ap.add_argument('--team-ref');ap.add_argument('--role-ref');ap.add_argument('--operator-ref');ap.add_argument('--json',action='store_true');ap.add_argument('--show',action='store_true');a=ap.parse_args()
    if a.business_id:
        from process_extensions import resolve_effective
        try:path,meta,content,extensions=resolve_effective(a.workflow_id,a.business_id,a.team_ref,a.role_ref,a.operator_ref)
        except ValueError as exc:raise SystemExit(str(exc))
        rel=str(path.relative_to(ROOT)) if path else None
        if a.show:print(content,end='' if content.endswith('\n') else '\n')
        elif a.json:print(json.dumps(_result(a.workflow_id,meta,rel,a.business_id,extensions),indent=2))
        else:print(rel or f"process-extension:{extensions[0]['id']}")
        return
    try:path,meta=resolve_workflow(a.workflow_id)
    except ValueError as exc:raise SystemExit(str(exc))
    rel=str(path.relative_to(ROOT))
    if a.show:print(path.read_text(),end='')
    elif a.json:print(json.dumps(_result(a.workflow_id,meta,rel),indent=2))
    else:print(rel)

if __name__=='__main__':main()
