#!/usr/bin/env python3
"""Describe reusable AURA playbook composition without constructing an execution graph.

Subcontract metadata identifies supporting operating knowledge that is essential or
conditional to the authored method. It does not specify runtime order, scheduling,
delegation, service calls, or receipt-completion requirements. The active model/user
chooses how to apply and sequence relevant knowledge in the real host environment.
"""
from _common import *
import argparse,json


def contract_map():
    out={}
    for path in contract_files():
        meta,_=read_frontmatter(path);cid=meta.get('id')
        if cid:out[cid]=meta
    return out


def process_maps():
    out={};paths=[];cp=ROOT/'core/process-map.json'
    if cp.exists():paths.append(cp)
    paths+=sorted((ROOT/'systems').glob('*/process-map.json'))
    for p in paths:
        data=json.loads(p.read_text());out[data['system']]={a['id']:a for a in data.get('activities',[])}
    return out


def resolve_entry(system=None,activity=None,contract_id=None):
    if contract_id:return contract_id
    maps=process_maps()
    if not system or not activity:raise ValueError('Provide --contract or both --system and --activity')
    if system not in maps or activity not in maps[system]:raise ValueError('Unknown system/activity')
    return maps[system][activity]['entry_contract']


def composition(contract_id,contracts=None,stack=None):
    contracts=contracts or contract_map();stack=stack or []
    if contract_id not in contracts:raise ValueError(f'Unknown contract {contract_id}')
    if contract_id in stack:raise ValueError('Playbook composition cycle: '+' -> '.join(stack+[contract_id]))
    contract=contracts[contract_id];subs=contract.get('subcontracts') or {};nstack=stack+[contract_id]
    essential=[];conditional=[]
    for child in subs.get('required',[]) or []:
        cid=child.get('id') if isinstance(child,dict) else child
        essential.append(composition(cid,contracts,nstack))
    for child in subs.get('conditional',[]) or []:
        if isinstance(child,str):cid,when=child,'condition described by parent playbook'
        else:cid,when=child.get('id'),child.get('when','condition described by parent playbook')
        conditional.append({'when':when,'knowledge':composition(cid,contracts,nstack)})
    return {'contract_id':contract_id,'owner_system':contract.get('owner_system'),'essential_knowledge':essential,'conditional_knowledge':conditional}


def build_process_plan(system=None,activity=None,contract_id=None):
    entry=resolve_entry(system,activity,contract_id)
    return {
        'entry_contract':entry,'system':system,'activity':activity,
        'composition':composition(entry),
        'rule':'Browse view only: this describes supporting AURA operating knowledge, not execution order, dependencies between workers, scheduling, delegation, or orchestration authority.'
    }


def main():
    ap=argparse.ArgumentParser(description='Describe the reusable knowledge composition of an AURA playbook without creating an execution plan.')
    ap.add_argument('--system');ap.add_argument('--activity');ap.add_argument('--contract');ap.add_argument('--output');a=ap.parse_args()
    try:data=build_process_plan(a.system,a.activity,a.contract)
    except ValueError as e:raise SystemExit(str(e))
    text=json.dumps(data,indent=2)+'\n'
    if a.output:Path(a.output).write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
