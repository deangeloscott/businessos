#!/usr/bin/env python3
"""Regression checks for broad Competitor Intelligence composition as operating knowledge."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter
from completion_evidence import completion_spec
from process_plan import build_process_plan
from route_and_resolve import route_and_resolve


def fail(msg):raise AssertionError(msg)
def candidate_ids(result):return [x.get('contract_id') for x in result.get('candidates',[]) if isinstance(x,dict)]


def main():
    path=ROOT/'systems/competitor-intelligence/contracts/analysis/competitive-position/CONTEXT.md'
    if not path.exists():fail('missing broad competitive-position contract')
    meta,body=read_frontmatter(path)
    if meta.get('id')!='competitor.analysis.competitive-position':fail('competitive-position contract id regressed')
    if meta.get('owner_system')!='competitor-intelligence':fail('competitive-position domain owner regressed')
    spec=completion_spec(meta)
    if spec.get('profile')!='intelligence':fail(f'competitive-position must use auditable intelligence completion profile, got {spec}')

    sub=meta.get('subcontracts') or {};required=set(sub.get('required') or [])
    for cid in [
        'competitor.discovery.competitive-set','competitor.analysis.profiling',
        'competitor.analysis.benchmark','competitor.analysis.competitive-implications',
    ]:
        if cid not in required:fail(f'competitive-position missing required composition component {cid}')

    conditional={x.get('id') if isinstance(x,dict) else x for x in (sub.get('conditional') or [])}
    for cid in [
        'competitor.analysis.pricing','competitor.analysis.offer-comparison','competitor.analysis.capability-comparison',
        'competitor.analysis.positioning','competitor.analysis.funnels','competitor.analysis.advertising',
        'competitor.analysis.content-strategy','competitor.analysis.customer-sentiment','competitor.analysis.strategic-change',
        'competitor.analysis.tactic-validation',
    ]:
        if cid not in conditional:fail(f'competitive-position missing conditional dimension {cid}')

    for phrase in [
        'Do **not** use this as a mandatory wrapper around a narrow request',
        'Explicitly requested material dimensions must not silently disappear',
        'evidence-closure map','subject-relevant support-grade evidence','Do not manufacture precision',
        'Visibility, ad longevity, engagement','A deliberately chosen success threshold/stop rule is a decision rule',
        'Do not invent owned-product capabilities, guarantees, integrations, implementation timelines, performance targets, or outcome forecasts',
        'what would falsify it','a Run is not required to perform or preserve this work',
        'Do not claim decision-grade completion while a material conclusion outruns its subject-relevant evidence',
    ]:
        if phrase not in body:fail(f'competitive-position missing guardrail: {phrase}')

    for benchmark_fragment in ['two-to-twelve-month range','five-to-fifty-thousand-dollar range']:
        if benchmark_fragment in body:fail(f'competitive-position contains benchmark-shaped failed-run example: {benchmark_fragment}')

    cmap=json.loads((ROOT/'systems/competitor-intelligence/process-map.json').read_text())
    entries={x.get('id'):x.get('entry_contract') for x in cmap.get('activities',[])}
    if entries.get('competitive-position')!='competitor.analysis.competitive-position':fail('competitor process map missing broad competitive-position activity')

    plan=build_process_plan(contract_id='competitor.analysis.competitive-position')
    components=[x['contract_id'] for x in plan.get('required_playbook_components',[])]
    if not components or components[-1]!='competitor.analysis.competitive-position':fail('competitive-position root missing from composed operating knowledge')
    for cid in required:
        if cid not in components:fail(f'playbook composition did not expand required competitor component {cid}')
    if 'execution' in plan.get('rule','').lower() and 'not runtime execution order' not in plan.get('rule','').lower():fail('process composition became runtime execution authority')

    # Natural language only produces candidates. The model/user decides whether the broad
    # or focused competitor method is actually appropriate, then AURA resolves that ID.
    broad='Research our competitors and tell us where we can win.'
    discovered=route_and_resolve(broad)
    if discovered.get('contract_id') is not None or not discovered.get('semantic_selection_required'):fail('broad competitor request was semantically auto-selected')
    if 'competitor.analysis.competitive-position' not in candidate_ids(discovered):fail(f'broad competitive-position playbook is not discoverable: {discovered}')
    selected=route_and_resolve(broad,selected_contract_id='competitor.analysis.competitive-position')
    if selected.get('contract_id')!='competitor.analysis.competitive-position':fail('explicit broad competitor selection failed')

    focused='Compare competitor pricing'
    focused_candidates=route_and_resolve(focused)
    if focused_candidates.get('contract_id') is not None:fail('focused competitor request was semantically auto-selected')
    if 'competitor.analysis.pricing' not in candidate_ids(focused_candidates):fail(f'focused pricing playbook is not discoverable: {focused_candidates}')
    focused_selected=route_and_resolve(focused,selected_contract_id='competitor.analysis.pricing')
    if focused_selected.get('contract_id')!='competitor.analysis.pricing':fail('explicit focused competitor selection failed')

    print('competitor composition regressions passed: composed knowledge stays useful without semantic routing or Run authority')

if __name__=='__main__':main()
