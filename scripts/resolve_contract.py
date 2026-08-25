#!/usr/bin/env python3
from _common import *
import argparse,json

def resolve_contract(contract_id):
    matches=[]
    for p in contract_files():
        try: meta,_=read_frontmatter(p)
        except Exception: continue
        if meta.get('id')==contract_id:matches.append((p,meta))
    if not matches: raise ValueError(f'Unknown contract id: {contract_id}')
    if len(matches)>1: raise ValueError(f'Duplicate contract id: {contract_id}')
    return matches[0]

def main():
    ap=argparse.ArgumentParser(description='Resolve a BusinessOS contract ID. With --business-id, include active ProcessExtensions/local playbooks.');ap.add_argument('contract_id');ap.add_argument('--business-id');ap.add_argument('--team-ref');ap.add_argument('--role-ref');ap.add_argument('--operator-ref');ap.add_argument('--json',action='store_true');ap.add_argument('--show',action='store_true');a=ap.parse_args()
    if a.business_id:
        from process_extensions import resolve_effective
        try:p,meta,content,exts=resolve_effective(a.contract_id,a.business_id,a.team_ref,a.role_ref,a.operator_ref)
        except ValueError as e:raise SystemExit(str(e))
        rel=str(p.relative_to(ROOT)) if p else None
        if a.show: print(content,end='' if content.endswith('\n') else '\n')
        elif a.json:print(json.dumps({'contract_id':a.contract_id,'business_id':a.business_id,'path':rel,'owner_system':meta.get('owner_system'),'type':meta.get('type'),'risk':meta.get('risk'),'autonomy_ceiling':meta.get('autonomy_ceiling'),'process_extension_ids':[x['id'] for x in exts],'local_playbook':bool(meta.get('local_playbook')),'executable':False},indent=2))
        else: print(rel or f"process-extension:{exts[0]['id']}")
        return
    try:p,meta=resolve_contract(a.contract_id)
    except ValueError as e:raise SystemExit(str(e))
    rel=str(p.relative_to(ROOT))
    if a.show:print(p.read_text(),end='')
    elif a.json:print(json.dumps({'contract_id':a.contract_id,'path':rel,'owner_system':meta.get('owner_system'),'type':meta.get('type'),'executable':False},indent=2))
    else:print(rel)
if __name__=='__main__':main()
