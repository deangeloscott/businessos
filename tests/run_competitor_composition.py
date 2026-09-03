#!/usr/bin/env python3
"""Protect useful Competitor Research discovery without creating a Workflow execution graph."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter
from process_plan import build_process_plan
from find_playbooks import find_candidates as find_playbook_candidates
from find_workflows import find_candidates as find_workflow_candidates


def fail(msg):raise AssertionError(msg)


def main():
    path=ROOT/'systems/competitor-intelligence/workflows/analysis/competitive-position/CONTEXT.md'
    if not path.exists():fail('missing broad competitive-position Workflow')
    meta,body=read_frontmatter(path)
    if meta.get('id')!='competitor.analysis.competitive-position':fail('competitive-position Workflow id regressed')
    if meta.get('type')!='workflow':fail('competitive-position must be represented as a Workflow')
    if meta.get('owner_system')!='competitor-intelligence':fail('competitive-position owner regressed')
    if meta.get('completion_evidence'):fail('competitive-position regained a semantic completion-evidence profile')

    composition=meta.get('workflows') or {}
    if composition.get('required'):fail('competitive-position must not force supporting Workflows')
    conditional={item.get('id') if isinstance(item,dict) else item for item in (composition.get('conditional') or [])}
    for wid in [
        'competitor.discovery.competitive-set','competitor.analysis.profiling','competitor.analysis.benchmark',
        'competitor.analysis.competitive-implications','competitor.analysis.pricing','competitor.analysis.offer-comparison',
        'competitor.analysis.capability-comparison','competitor.analysis.positioning','competitor.analysis.funnels',
        'competitor.analysis.advertising','competitor.analysis.content-strategy','competitor.analysis.customer-sentiment',
        'competitor.analysis.strategic-change','competitor.analysis.tactic-validation',
    ]:
        if wid not in conditional:fail(f'competitive-position missing useful conditional knowledge {wid}')

    for phrase in [
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
        if phrase not in body:fail(f'competitive-position missing important guardrail: {phrase}')

    plan=build_process_plan(workflow_id='competitor.analysis.competitive-position')
    node=plan.get('workflow_composition') or {}
    if node.get('workflow_id')!='competitor.analysis.competitive-position':fail('competitive-position root missing from browse view')
    if node.get('normally_use'):fail('browse view turned supporting knowledge into a normally-required chain')
    conditional_ids={((item or {}).get('workflow') or {}).get('workflow_id') for item in node.get('conditionally_use') or []}
    if not {'competitor.discovery.competitive-set','competitor.analysis.pricing'} <= conditional_ids:
        fail(f'browse view lost conditional competitor knowledge: {conditional_ids}')
    rule=plan.get('rule','').lower()
    if 'not an execution graph' not in rule:fail('Workflow browse view lost explicit non-execution boundary')

    # Natural-language discovery surfaces candidates; the model/user owns semantics.
    broad=find_playbook_candidates('Research our competitors and tell us where we can win.',5)
    if 'competitor-research' not in [row.get('id') for row in broad]:fail(f'Competitor Research Playbook is not discoverable: {broad}')
    if any(row.get('selection_authority') is not False for row in broad):fail('Playbook discovery claimed semantic authority')

    focused=find_workflow_candidates('Compare competitor pricing',5,'competitor-intelligence')
    if 'competitor.analysis.pricing' not in [row.get('workflow_id') for row in focused]:fail(f'focused pricing Workflow is not discoverable: {focused}')
    if any(row.get('selection_authority') is not False for row in focused):fail('Workflow discovery claimed semantic authority')

    print('competitor composition regressions passed: useful supporting knowledge remains discoverable without mandatory composition or routing authority')

if __name__=='__main__':main()
