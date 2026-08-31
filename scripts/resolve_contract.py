#!/usr/bin/env python3
from _common import *
import argparse,json


def resolve_contract(contract_id):
    matches=[]
    for p in contract_files():
        try:meta,_=read_frontmatter(p)
        except Exception:continue
        if meta.get('id')==contract_id:matches.append((p,meta))
    if not matches:raise ValueError(f'Unknown contract id: {contract_id}')
    if len(matches)>1:raise ValueError(f'Duplicate contract id: {contract_id}')
    return matches[0]


def _result(contract_id,meta,path=None,business_id=None,exts=None):
    return {
        'contract_id':contract_id,
        'business_id':business_id,
        'path':path,
        'owner_system':meta.get('owner_system'),
        'type':meta.get('type'),
        'capabilities':meta.get('capabilities') or {'required':['none'],'optional':['none']},
        'process_extension_ids':[x['id'] for x in (exts or [])],
        'local_playbook':bool(meta.get('local_playbook')),
        'executable':False,
        'boundary':'Contract metadata describes AURA operational knowledge. Live tools/providers/permissions belong to the active harness/runtime.'
    }


def main():
    ap=argparse.ArgumentParser(description='Resolve an AURA contract ID. With --business-id, include applicable business ProcessExtensions/local playbooks.')
    ap.add_argument('contract_id');ap.add_argument('--business-id');ap.add_argument('--team-ref');ap.add_argument('--role-ref');ap.add_argument('--operator-ref');ap.add_argument('--json',action='store_true');ap.add_argument('--show',action='store_true');a=ap.parse_args()
    if a.business_id:
        from process_extensions import resolve_effective
        try:p,meta,content,exts=resolve_effective(a.contract_id,a.business_id,a.team_ref,a.role_ref,a.operator_ref)
        except ValueError as e:raise SystemExit(str(e))
        rel=str(p.relative_to(ROOT)) if p else None
        if a.show:print(content,end='' if content.endswith('\n') else '\n')
        elif a.json:print(json.dumps(_result(a.contract_id,meta,rel,a.business_id,exts),indent=2))
        else:print(rel or f"process-extension:{exts[0]['id']}")
        return
    try:p,meta=resolve_contract(a.contract_id)
    except ValueError as e:raise SystemExit(str(e))
    rel=str(p.relative_to(ROOT))
    if a.show:print(p.read_text(),end='')
    elif a.json:print(json.dumps(_result(a.contract_id,meta,rel),indent=2))
    else:print(rel)


if __name__=='__main__':main()
