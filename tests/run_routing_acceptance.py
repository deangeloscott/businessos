#!/usr/bin/env python3
"""Protect deterministic playbook discovery without testing model semantics."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from route_task import route
from route_and_resolve import route_and_resolve


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    registry={row['id']:row for row in json.loads((ROOT/'generated/contract-registry.json').read_text()).get('contracts',[])}

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
        rows=route(text,5)
        req(len(rows)<=5,f'candidate search exceeded bound for {text!r}: {len(rows)}')
        for row in rows:
            req(row.get('contract_id') in registry,f'candidate search returned unknown playbook: {row}')
            req(row.get('status')=='available',f'candidate availability must be mechanically valid: {row}')
            req(row.get('selection_authority') is False,f'candidate search claimed semantic authority: {row}')

        resolved=route_and_resolve(text)
        req(resolved.get('contract_id') is None,f'natural language was silently converted into selected playbook for {text!r}: {resolved}')
        req(resolved.get('semantic_selection_required') is True,f'natural-language method choice must remain with model/user: {resolved}')
        req(resolved.get('selection_mode')=='model_selection_required',f'model-selection boundary drifted: {resolved}')

    # Candidate search should still be useful for distinctive literal jobs.
    webinar=route('Create a webinar.',5)
    req(any(row.get('contract_id')=='marketing.assets.webinar' for row in webinar),f'distinctive literal playbook was not discoverable: {webinar}')

    # Exact IDs are deterministic identifiers, not semantic guesses.
    exact='content.production.presentation';rows=route(exact,3)
    req(rows and rows[0].get('contract_id')==exact,'exact playbook ID should resolve as the highest candidate')
    selected=route_and_resolve('Create a presentation.',selected_contract_id=exact)
    req(selected.get('contract_id')==exact and selected.get('semantic_selection_required') is False,'explicitly selected playbook did not resolve deterministically')
    req(selected.get('selection_mode')=='explicit_model_selection','explicit selection lost model-owned provenance')

    print('playbook candidate discovery passed: deterministic index, model-owned semantic selection')


if __name__=='__main__':main()
