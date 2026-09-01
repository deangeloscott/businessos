#!/usr/bin/env python3
"""Protect bounded playbook discovery without testing model semantics."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from find_playbooks import find_candidates
from resolve_contract import resolve_contract


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    registry={row['id']:row for row in json.loads((ROOT/'generated/contract-registry.json').read_text()).get('contracts',[])}
    req((ROOT/'generated/playbook-candidate-index.json').exists(),'playbook candidate index was not generated')
    req(not (ROOT/'generated/route-index.json').exists(),'retired route index still exists')
    req(not (ROOT/'scripts/route_task.py').exists(),'retired route_task helper still exists')
    req(not (ROOT/'scripts/route_and_resolve.py').exists(),'retired route_and_resolve helper still exists')

    cases=[
        'Create a webinar.',
        'Why are customers leaving?',
        'What should we work on first?',
        'Compare competitor pricing.',
        'Create a publish-ready organic page for our target query.',
        'Research industry news and turn it into LinkedIn posts.',
        'Help me figure out what to improve.',
    ]
    for text in cases:
        rows=find_candidates(text,5)
        req(len(rows)<=5,f'candidate search exceeded bound for {text!r}: {len(rows)}')
        for row in rows:
            req(row.get('contract_id') in registry,f'candidate search returned unknown playbook: {row}')
            req(row.get('status')=='available',f'candidate availability must be mechanically valid: {row}')
            req(row.get('selection_authority') is False,f'candidate search claimed semantic authority: {row}')

    webinar=find_candidates('Create a webinar.',5)
    req(any(row.get('contract_id')=='marketing.assets.webinar' for row in webinar),f'distinctive literal playbook was not discoverable: {webinar}')

    exact='content.production.presentation';rows=find_candidates(exact,3)
    req(rows and rows[0].get('contract_id')==exact,'exact playbook ID should be the highest candidate')
    path,meta=resolve_contract(exact)
    req(meta.get('id')==exact and path.exists(),'exact selected playbook ID did not resolve deterministically')

    print('playbook discovery passed: bounded lexical candidates, model-owned semantic selection, exact deterministic resolution')


if __name__=='__main__':main()
