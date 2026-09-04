#!/usr/bin/env python3
"""Protect useful Competitor Research discovery without creating a Workflow execution graph."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter,workflow_files
from process_plan import build_process_plan
from find_playbooks import find_candidates as find_playbook_candidates
from find_workflows import find_candidates as find_workflow_candidates


def fail(msg):raise AssertionError(msg)


def main():
    # Every Competitor Workflow is authored operating knowledge, never a machine-readable
    # execution graph or an owner-routing view over organization-owned canonical memory.
    count=0
    for workflow_path in workflow_files():
        workflow_meta,_=read_frontmatter(workflow_path)
        if workflow_meta.get('owner_system')!='competitor-intelligence':continue
        count+=1
        rel=workflow_path.relative_to(ROOT)
        if workflow_meta.get('type')!='workflow':fail(f'{rel} is not typed as Workflow')
        if 'workflows' in workflow_meta:fail(f'{rel} regained machine-readable Workflow composition metadata')
        if 'capabilities' in workflow_meta:fail(f'{rel} regained AURA capability metadata')
        for selector in workflow_meta.get('reads',[]):
            if not isinstance(selector,dict):continue
            retired=set(selector)&{'owner_system','owner_scope','producer_system'}
            if retired:fail(f'{rel} canonical read selector regained internal ownership keys {sorted(retired)}')
            unsupported=set(selector)-{'type','domain','scope'}
            if unsupported:fail(f'{rel} canonical read selector has unsupported keys {sorted(unsupported)}')
    if not count:fail('no Competitor Intelligence Workflows found')

    path=ROOT/'systems/competitor-intelligence/workflows/analysis/competitive-position/CONTEXT.md'
    if not path.exists():fail('missing broad competitive-position Workflow')
    meta,body=read_frontmatter(path)
    if meta.get('id')!='competitor.analysis.competitive-position':fail('competitive-position Workflow id regressed')
    if meta.get('type')!='workflow':fail('competitive-position must be represented as a Workflow')
    if meta.get('owner_system')!='competitor-intelligence':fail('competitive-position owner regressed')
    if meta.get('completion_evidence'):fail('competitive-position regained a semantic completion-evidence profile')
    if meta.get('workflows'):fail('competitive-position regained machine-readable composition metadata')

    # Specialist knowledge should stay discoverable/advisory in the authored procedure,
    # not become a hidden execution graph in front matter.
    for phrase in [
        '`competitor.discovery.competitive-set`','`competitor.analysis.profiling`','`competitor.analysis.benchmark`',
        '`competitor.analysis.competitive-implications`','Use the relevant specialist Workflows when they add useful expertise',
        'Do **not** use this as a mandatory wrapper around a narrow request',
        'the active model decides which supporting Workflows, outside methods, tools, and evidence are useful',
        'Explicitly requested material dimensions must not silently disappear',
        'evidence-closure map','subject-relevant support-grade evidence','Do not manufacture precision',
        'valuable leading signals','not by themselves proof of profitability, downstream revenue, or causal impact',
        'A deliberately chosen success threshold/stop rule is a decision rule',
        'Do not invent owned-product capabilities, guarantees, integrations, implementation timelines, performance targets, or outcome forecasts',
        'what would falsify it','a Run is not required to perform, validate, or preserve this work',
        'Do not claim decision-grade completion while a material conclusion outruns its subject-relevant evidence',
    ]:
        if phrase not in body:fail(f'competitive-position missing important expertise/guardrail: {phrase}')

    plan=build_process_plan(workflow_id='competitor.analysis.competitive-position')
    view=plan.get('workflow_view') or {}
    if view.get('workflow_id')!='competitor.analysis.competitive-position':fail('competitive-position missing from browse view')
    if 'workflow_composition' in plan:fail('browse helper recreated a Workflow composition graph')
    rule=plan.get('rule','').lower()
    if 'does not construct' not in rule:fail('Workflow browse view lost explicit non-graph boundary')

    # Natural-language discovery surfaces candidates; the model/user owns semantics.
    broad=find_playbook_candidates('Research our competitors and tell us where we can win.',5)
    if 'competitor-research' not in [row.get('id') for row in broad]:fail(f'Competitor Research Playbook is not discoverable: {broad}')
    if any(row.get('selection_authority') is not False for row in broad):fail('Playbook discovery claimed semantic authority')

    focused=find_workflow_candidates('Compare competitor pricing',5,'competitor-intelligence')
    if 'competitor.analysis.pricing' not in [row.get('workflow_id') for row in focused]:fail(f'focused pricing Workflow is not discoverable: {focused}')
    if any(row.get('selection_authority') is not False for row in focused):fail('Workflow discovery claimed semantic authority')

    print(f'competitor composition regressions passed: {count} Workflows remain discoverable operating knowledge without composition metadata or routing authority')

if __name__=='__main__':main()
