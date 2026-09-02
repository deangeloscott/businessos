#!/usr/bin/env python3
"""Protect bounded Playbook/Workflow discovery without testing model semantics."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from find_playbooks import find_candidates as find_playbooks
from find_workflows import find_candidates as find_workflows
from operating_knowledge import installed_playbooks
from resolve_workflow import resolve_workflow


def req(condition,message):
    if not condition:raise AssertionError(message)


def main():
    registry={row['id']:row for row in json.loads((ROOT/'generated/contract-registry.json').read_text()).get('contracts',[])}
    playbook_ids={row['id'] for row in installed_playbooks(list(registry.values()))}
    req((ROOT/'generated/workflow-candidate-index.json').exists(),'Workflow candidate index was not generated')
    req(not (ROOT/'generated/playbook-candidate-index.json').exists(),'retired flattened playbook candidate index still exists')
    req(not (ROOT/'generated/route-index.json').exists(),'retired route index still exists')
    req(not (ROOT/'scripts/route_task.py').exists(),'retired route_task helper still exists')
    req(not (ROOT/'scripts/route_and_resolve.py').exists(),'retired route_and_resolve helper still exists')

    cases=[
        'Create a webinar.','Research our competitors and tell us where we can win.',
        'Why are customers leaving?','Create a presentation for our sales meeting.',
        'Research industry news that matters to us.','Figure out where customers are getting stuck.',
    ]
    for text in cases:
        rows=find_playbooks(text,5)
        req(len(rows)<=5,f'Playbook search exceeded bound for {text!r}: {len(rows)}')
        for row in rows:
            req(row.get('id') in playbook_ids,f'Playbook search returned unknown Playbook: {row}')
            req(row.get('selection_authority') is False,f'Playbook search claimed semantic authority: {row}')

    webinar=find_playbooks('Create a webinar.',5)
    req(any(row.get('entry_workflow')=='marketing.assets.webinar' for row in webinar),f'Webinar production Playbook was not discoverable: {webinar}')
    competitors=find_playbooks('Research our competitors and tell us where we can win.',5)
    req(any(row.get('id')=='competitor-research' for row in competitors),f'Competitor Research Playbook was not discoverable: {competitors}')

    workflow_cases=[
        ('Compare competitor pricing.','competitor.analysis.pricing','competitor-intelligence'),
        ('Create a publish-ready article.','content.production.article','content-synthesis'),
        ('Check our landing page claims.','marketing.landing-page.qa','marketing-synthesis'),
    ]
    for text,expected,owner in workflow_cases:
        rows=find_workflows(text,6,owner)
        req(len(rows)<=6,f'Workflow search exceeded bound for {text!r}: {len(rows)}')
        req(any(row.get('workflow_id')==expected for row in rows),f'expected Workflow {expected} not discoverable for {text!r}: {rows}')
        for row in rows:
            req(row.get('workflow_id') in registry,f'Workflow search returned unknown Workflow: {row}')
            req(row.get('selection_authority') is False,f'Workflow search claimed semantic authority: {row}')

    exact='content.production.presentation';rows=find_workflows(exact,3,'content-synthesis')
    req(rows and rows[0].get('workflow_id')==exact,'exact Workflow ID should be the highest Workflow candidate')
    path,meta=resolve_workflow(exact)
    req(meta.get('id')==exact and meta.get('type')=='workflow' and path.exists(),'exact selected Workflow ID did not resolve deterministically')

    print('Playbook/Workflow discovery passed: bounded navigation, model-owned semantic selection, exact Workflow resolution')

if __name__=='__main__':main()
