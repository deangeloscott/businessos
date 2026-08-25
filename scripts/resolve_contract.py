#!/usr/bin/env python3
from _common import *
import argparse,json

def resolve_contract(contract_id):
    matches=[]
    for p in contract_files():
        try: meta,_=read_frontmatter(p)
        except Exception: continue
        if meta.get('id')==contract_id:
            matches.append((p,meta))
    if not matches: raise ValueError(f'Unknown contract id: {contract_id}')
    if len(matches)>1: raise ValueError(f'Duplicate contract id: {contract_id}')
    p,meta=matches[0]
    return p,meta

def main():
    ap=argparse.ArgumentParser(description='Resolve a BusinessOS contract ID to its operating CONTEXT.md. Contract IDs are identifiers, not executables.')
    ap.add_argument('contract_id'); ap.add_argument('--json',action='store_true'); ap.add_argument('--show',action='store_true')
    a=ap.parse_args()
    try: p,meta=resolve_contract(a.contract_id)
    except ValueError as e: raise SystemExit(str(e))
    rel=str(p.relative_to(ROOT))
    if a.show:
        print(p.read_text(),end='')
    elif a.json:
        print(json.dumps({'contract_id':a.contract_id,'path':rel,'owner_system':meta.get('owner_system'),'type':meta.get('type'),'executable':False},indent=2))
    else:
        print(rel)
if __name__=='__main__': main()
