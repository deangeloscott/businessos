#!/usr/bin/env python3
"""Describe composed AURA playbook knowledge without scheduling runtime execution.

Required/conditional subcontract metadata says what a selected AURA method is composed of.
The active model/user decides how to reason, sequence, delegate, parallelize, or otherwise
execute the work in the host environment while preserving any genuinely essential method
invariants needed to claim playbook conformance.
"""
from _common import *
import argparse,json


def registry_map():return {c['id']:c for c in load_registry()['contracts']}


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


def expand(contract_id,reg=None,stack=None,depth=0):
    reg=reg or registry_map();stack=stack or []
    if contract_id not in reg:raise ValueError(f'Unknown contract {contract_id}')
    if contract_id in stack:raise ValueError('Playbook dependency cycle: '+' -> '.join(stack+[contract_id]))
    contract=reg[contract_id];subcontracts=contract.get('subcontracts') or {}
    node={'contract_id':contract_id,'owner_system':contract.get('owner_system'),'depth':depth,'required':[],'conditional':[]}
    nstack=stack+[contract_id]
    for child in subcontracts.get('required',[]) or []:
        cid=child.get('id') if isinstance(child,dict) else child
        node['required'].append(expand(cid,reg,nstack,depth+1))
    for child in subcontracts.get('conditional',[]) or []:
        if isinstance(child,str):cid,when=child,'condition described by parent playbook'
        else:cid,when=child.get('id'),child.get('when','condition described by parent playbook')
        node['conditional'].append({'when':when,'playbook':expand(cid,reg,nstack,depth+1)})
    return node


def flatten_required(node):
    """Return dependency-first components as a reading/conformance aid, not a scheduler."""
    out=[]
    def walk(n):
        for child in n.get('required',[]):walk(child)
        out.append({'contract_id':n['contract_id'],'owner_system':n['owner_system'],'depth':n['depth']})
    walk(node);seen=set();result=[]
    for row in out:
        if row['contract_id'] in seen:continue
        seen.add(row['contract_id']);result.append(row)
    return result


def build_process_plan(system=None,activity=None,contract_id=None):
    entry=resolve_entry(system,activity,contract_id);tree=expand(entry)
    return {
        'version':os_version(),'entry_contract':entry,'system':system,'activity':activity,
        'required_playbook_components':flatten_required(tree),'dependency_tree':tree,
        'rule':'This describes composed AURA operating knowledge. It is not runtime execution order, scheduling, delegation, or orchestration authority; the active model/user/harness decides how best to perform the selected method.'
    }


def main():
    ap=argparse.ArgumentParser(description='Describe the required/conditional knowledge components of a selected AURA playbook without creating an execution plan.')
    ap.add_argument('--system');ap.add_argument('--activity');ap.add_argument('--contract');ap.add_argument('--output');a=ap.parse_args()
    try:data=build_process_plan(a.system,a.activity,a.contract)
    except ValueError as e:raise SystemExit(str(e))
    text=json.dumps(data,indent=2)+'\n'
    if a.output:Path(a.output).write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
