#!/usr/bin/env python3
"""Protect broad Competitor Research composition without turning it into execution authority."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter
from completion_evidence import completion_spec
from process_plan import build_process_plan
from find_playbooks import find_candidates as find_playbook_candidates
from find_workflows import find_candidates as find_workflow_candidates
from resolve_workflow import resolve_workflow


def fail(msg):raise AssertionError(msg)
def workflow_ids(node):
    if not isinstance(node,dict):return []
    out=[]
    wid=node.get('workflow_id')
    if wid:out.append(wid)
    for child in node.get('normally_use') or []:out.extend(workflow_ids(child))
    for item in node.get('conditionally_use') or []:out.extend(workflow_ids((item or {}).get('workflow')))
    return out


def main():
    path=ROOT/'systems/competitor-intelligence/contracts/analysis/competitive-position/CONTEXT.md'
    if not path.exists():fail('missing broad competitive-position Workflow')
    meta,body=read_frontmatter(path)
    if meta.get('id')!='competitor.analysis.competitive-position':fail('competitive-position Workflow id regressed')
    if meta.get('type')!='workflow':fail('competitive-position must be represented as a Workflow')
    if meta.get('owner_system')!='competitor-intelligence':fail('competitive-position owner regressed')
    spec=completion_spec(meta)
    if spec.get('profile')!='intelligence':fail(f'competitive-position must retain auditable intelligence quality requirements, got {spec}')

    composition=meta.get('workflows') or {};normally=set(composition.get('required') or [])
    for wid in [
        'competitor.discovery.competitive-set','competitor.analysis.profiling',
        'competitor.analysis.benchmark','competitor.analysis.competitive-implications',
    ]:
        if wid not in normally:fail(f'competitive-position missing normally useful supporting Workflow {wid}')

    conditional={item.get('id') if isinstance(item,dict) else item for item in (composition.get('conditional') or [])}
    for wid in [
        'competitor.analysis.pricing','competitor.analysis.offer-comparison','competitor.analysis.capability-comparison',
        'competitor.analysis.positioning','competitor.analysis.funnels','competitor.analysis.advertising',
        'competitor.analysis.content-strategy','competitor.analysis.customer-sentiment','competitor.analysis.strategic-change',
        'competitor.analysis.tactic-validation',
    ]:
        if wid not in conditional:fail(f'competitive-position missing conditionally useful Workflow {wid}')

    for phrase in [
        'Do **not** use this as a mandatory wrapper around a narrow request',
        'Explicitly requested material dimensions must not silently disappear',
        'evidence-closure map','subject-relevant support-grade evidence','Do not manufacture precision',
        'Visibility, ad longevity, engagement','A deliberately chosen success threshold/stop rule is a decision rule',
        'Do not invent owned-product capabilities, guarantees, integrations, implementation timelines, performance targets, or outcome forecasts',
        'what would falsify it','a Run is not required to perform, validate, or preserve this work',
        'Do not claim decision-grade completion while a material conclusion outruns its subject-relevant evidence',
    ]:
        if phrase not in body:fail(f'competitive-position missing important guardrail: {phrase}')

    plan=build_process_plan(workflow_id='competitor.analysis.competitive-position')
    ids=workflow_ids(plan.get('workflow_composition'))
    if not ids or ids[0]!='competitor.analysis.competitive-position':fail('competitive-position root missing from Workflow composition')
    for wid in normally:
        if wid not in ids:fail(f'Workflow composition did not expose normally useful competitor knowledge {wid}')
    rule=plan.get('rule','').lower()
    if 'not an execution graph' not in rule and 'not execution' not in rule:fail('Workflow composition lost explicit non-execution boundary')

    # Broad natural-language intent should surface the human-meaningful Playbook; focused
    # requests may surface a detailed Workflow. Neither discovery surface owns semantics.
    broad=find_playbook_candidates('Research our competitors and tell us where we can win.',5)
    if 'competitor-research' not in [row.get('id') for row in broad]:fail(f'Competitor Research Playbook is not discoverable: {broad}')
    if any(row.get('selection_authority') is not False for row in broad):fail('Playbook discovery claimed semantic authority')

    focused=find_workflow_candidates('Compare competitor pricing',5,'competitor-intelligence')
    if 'competitor.analysis.pricing' not in [row.get('workflow_id') for row in focused]:fail(f'focused pricing Workflow is not discoverable: {focused}')
    if any(row.get('selection_authority') is not False for row in focused):fail('Workflow discovery claimed semantic authority')

    selected_path,selected_meta=resolve_workflow('competitor.analysis.competitive-position')
    if selected_meta.get('type')!='workflow' or not selected_path.exists():fail('explicit competitor Workflow resolution failed')

    print('competitor composition regressions passed: Playbook framing and reusable Workflow composition stay useful without routing or execution authority')

if __name__=='__main__':main()
