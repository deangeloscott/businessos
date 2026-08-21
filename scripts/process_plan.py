#!/usr/bin/env python3
from _common import *
import argparse,json

def registry_map():
    return {c['id']:c for c in load_registry()['contracts']}

def process_maps():
    out={}
    paths=[]
    cp=ROOT/'core/process-map.json'
    if cp.exists(): paths.append(cp)
    paths += sorted((ROOT/'systems').glob('*/process-map.json'))
    for p in paths:
        d=json.loads(p.read_text())
        out[d['system']]={a['id']:a for a in d.get('activities',[])}
    return out

def resolve_entry(system=None,activity=None,contract_id=None):
    if contract_id:return contract_id
    maps=process_maps()
    if not system or not activity:raise ValueError('Provide --contract or both --system and --activity')
    if system not in maps or activity not in maps[system]:raise ValueError('Unknown system/activity')
    return maps[system][activity]['entry_contract']

def expand(contract_id, reg=None, stack=None, depth=0):
    reg=reg or registry_map();stack=stack or []
    if contract_id not in reg:raise ValueError(f'Unknown contract {contract_id}')
    if contract_id in stack:raise ValueError('Process dependency cycle: '+' -> '.join(stack+[contract_id]))
    c=reg[contract_id];sc=c.get('subcontracts') or {}
    node={'contract_id':contract_id,'owner_system':c.get('owner_system'),'depth':depth,'required':[],'conditional':[]}
    nstack=stack+[contract_id]
    for child in sc.get('required',[]) or []:
        cid=child.get('id') if isinstance(child,dict) else child
        node['required'].append(expand(cid,reg,nstack,depth+1))
    for child in sc.get('conditional',[]) or []:
        if isinstance(child,str):cid,when=child,'condition determined by parent contract'
        else:cid,when=child.get('id'),child.get('when','condition determined by parent contract')
        node['conditional'].append({'when':when,'process':expand(cid,reg,nstack,depth+1)})
    return node

def flatten_required(node):
    out=[]
    def walk(n):
        for c in n.get('required',[]):walk(c)
        out.append({'contract_id':n['contract_id'],'owner_system':n['owner_system'],'depth':n['depth']})
    walk(node)
    # Deduplicate while preserving first executable occurrence; root remains last.
    seen=set();res=[]
    for x in out:
        if x['contract_id'] in seen:continue
        seen.add(x['contract_id']);res.append(x)
    return res

def build_process_plan(system=None,activity=None,contract_id=None):
    entry=resolve_entry(system,activity,contract_id)
    tree=expand(entry)
    return {'version':os_version(),'entry_contract':entry,'system':system,'activity':activity,'required_execution_order':flatten_required(tree),'tree':tree}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--system');ap.add_argument('--activity');ap.add_argument('--contract');ap.add_argument('--output');a=ap.parse_args()
    try:d=build_process_plan(a.system,a.activity,a.contract)
    except ValueError as e:raise SystemExit(str(e))
    s=json.dumps(d,indent=2)+'\n'
    if a.output:Path(a.output).write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
