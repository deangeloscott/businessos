#!/usr/bin/env python3
"""Resolve an explicitly selected AURA playbook or return bounded candidates.

Natural-language semantic intent belongs to the active model/user. AURA deterministically
checks installed operating knowledge and resolves an explicit playbook ID after that judgment.
"""
from _common import ROOT
import argparse,json
from route_task import route
from resolve_contract import resolve_contract
from process_extensions import local_playbook_candidates,resolve_effective


def _selected(task,contract_id,business_id=None,team_ref=None,role_ref=None,operator_ref=None):
    if business_id:
        path,meta,_,exts=resolve_effective(contract_id,business_id,team_ref,role_ref,operator_ref)
        return {
            'task':task,'contract_id':contract_id,'owner_system':meta.get('owner_system'),'status':'available',
            'reason':'explicitly selected by the active model/user after semantic judgment',
            'path':str(path.relative_to(ROOT)) if path else None,
            'process_extension_ids':[x['id'] for x in exts],'local_playbook':bool(meta.get('local_playbook')),
            'executable':False,'selection_mode':'explicit_model_selection','semantic_selection_required':False,
            'business_id':business_id,
        }
    path,meta=resolve_contract(contract_id)
    return {
        'task':task,'contract_id':contract_id,'owner_system':meta.get('owner_system'),'status':'available',
        'reason':'explicitly selected by the active model/user after semantic judgment',
        'path':str(path.relative_to(ROOT)),'executable':False,'selection_mode':'explicit_model_selection',
        'semantic_selection_required':False,
    }


def route_and_resolve(task,business_id=None,team_ref=None,role_ref=None,operator_ref=None,selected_contract_id=None,top=5):
    if selected_contract_id:
        return _selected(task,selected_contract_id,business_id,team_ref,role_ref,operator_ref)

    candidates=local_playbook_candidates(task,business_id,team_ref,role_ref,operator_ref,top) if business_id else []
    seen={row['contract_id'] for row in candidates}
    for row in route(task,top):
        if row.get('contract_id') in seen:continue
        candidates.append(row);seen.add(row.get('contract_id'))
        if len(candidates)>=top:break
    return {
        'task':task,'contract_id':None,'owner_system':None,
        'status':'candidates' if candidates else 'no_candidate',
        'reason':'AURA returns bounded installed playbook candidates but does not semantically choose the method.',
        'candidates':candidates,
        'selection_mode':'model_selection_required',
        'semantic_selection_required':True,
        'executable':False,
        **({'business_id':business_id} if business_id else {}),
    }


def main():
    ap=argparse.ArgumentParser(description='Resolve an explicitly selected AURA playbook or list bounded candidates for model judgment.')
    ap.add_argument('task');ap.add_argument('--business-id');ap.add_argument('--team-ref');ap.add_argument('--role-ref');ap.add_argument('--operator-ref')
    ap.add_argument('--selected-contract',help='Playbook ID explicitly selected by the active model/user after semantic judgment')
    ap.add_argument('--top',type=int,default=5);ap.add_argument('--show',action='store_true');a=ap.parse_args()
    try:result=route_and_resolve(a.task,a.business_id,a.team_ref,a.role_ref,a.operator_ref,a.selected_contract,a.top)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps(result,indent=2))
    if a.show and result.get('contract_id'):
        print('\n--- RESOLVED PLAYBOOK ---\n')
        if a.business_id:
            _,_,content,_=resolve_effective(result['contract_id'],a.business_id,a.team_ref,a.role_ref,a.operator_ref);print(content,end='' if content.endswith('\n') else '\n')
        elif result.get('path'):print((ROOT/result['path']).read_text(),end='')


if __name__=='__main__':main()
