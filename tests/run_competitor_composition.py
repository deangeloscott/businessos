#!/usr/bin/env python3
"""Regression checks for broad Competitor Intelligence composition without exhaustive-by-default routing."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from _common import read_frontmatter
from completion_evidence import completion_spec, contract_index
from process_plan import build_process_plan
from route_and_resolve import route_and_resolve


def fail(msg): raise AssertionError(msg)


def main():
    path=ROOT/'systems/competitor-intelligence/contracts/analysis/competitive-position/CONTEXT.md'
    if not path.exists():fail('missing broad competitive-position contract')
    meta,body=read_frontmatter(path)
    if meta.get('id')!='competitor.analysis.competitive-position':fail('competitive-position contract id regressed')
    if meta.get('owner_system')!='competitor-intelligence':fail('competitive-position semantic owner regressed')
    spec=completion_spec(contract_index()['competitor.analysis.competitive-position'])
    if spec.get('profile')!='intelligence':fail(f'competitive-position must use auditable intelligence completion profile, got {spec}')

    sub=meta.get('subcontracts') or {}
    required=set(sub.get('required') or [])
    for cid in [
        'competitor.discovery.competitive-set',
        'competitor.analysis.profiling',
        'competitor.analysis.benchmark',
        'competitor.analysis.competitive-implications',
    ]:
        if cid not in required:fail(f'competitive-position missing required composition step {cid}')

    conditional={x.get('id') if isinstance(x,dict) else x for x in (sub.get('conditional') or [])}
    for cid in [
        'competitor.analysis.pricing',
        'competitor.analysis.offer-comparison',
        'competitor.analysis.capability-comparison',
        'competitor.analysis.positioning',
        'competitor.analysis.funnels',
        'competitor.analysis.advertising',
        'competitor.analysis.content-strategy',
        'competitor.analysis.customer-sentiment',
        'competitor.analysis.strategic-change',
        'competitor.analysis.tactic-validation',
    ]:
        if cid not in conditional:fail(f'competitive-position missing conditional dimension {cid}')

    for phrase in [
        'Do **not** use this as a mandatory wrapper around a narrow request',
        'Explicitly requested material dimensions must not silently disappear',
        'evidence-closure map',
        'subject-relevant support-grade evidence',
        'Do not manufacture precision',
        'Visibility, ad longevity, engagement',
        'A deliberately chosen success threshold/stop rule is a decision rule',
        'Do not invent owned-product capabilities, guarantees, integrations, implementation timelines, performance targets, or outcome forecasts',
        'what would falsify it',
        'Run-local intelligence analysis record',
        'Do not mark the Run complete while a material conclusion outruns its subject-relevant evidence',
    ]:
        if phrase not in body:fail(f'competitive-position missing guardrail: {phrase}')

    # Keep the product invariant general rather than teaching the candidate a frozen failed-run answer.
    for benchmark_fragment in ['two-to-twelve-month range','five-to-fifty-thousand-dollar range']:
        if benchmark_fragment in body:fail(f'competitive-position contains benchmark-shaped failed-run example: {benchmark_fragment}')

    cmap=json.loads((ROOT/'systems/competitor-intelligence/process-map.json').read_text())
    entries={x.get('id'):x.get('entry_contract') for x in cmap.get('activities',[])}
    if entries.get('competitive-position')!='competitor.analysis.competitive-position':fail('competitor process map missing broad competitive-position activity')

    plan=build_process_plan(contract_id='competitor.analysis.competitive-position')
    order=[x['contract_id'] for x in plan.get('required_execution_order',[])]
    if not order or order[-1]!='competitor.analysis.competitive-position':fail('competitive-position root must finish after required composition')
    for cid in required:
        if cid not in order:fail(f'process plan did not expand required competitor job {cid}')

    broad_cases=[
        'Establish the real competitive set and produce a decision-grade competitive position.',
        'Research our competitors and tell us where we can win.',
        'Give me a current competitive landscape with strengths, weaknesses, and whitespace.',
    ]
    for text in broad_cases:
        got=route_and_resolve(text).get('contract_id')
        if got!='competitor.analysis.competitive-position':fail(f'broad competitor request collapsed to {got}: {text}')
    focused=route_and_resolve('Compare competitor pricing').get('contract_id')
    if focused!='competitor.analysis.pricing':fail(f'focused competitor pricing request should remain atomic, got {focused}')

    print('competitor composition regressions passed: broad requests compose, focused requests stay focused, and evidence closure is required without benchmark-shaped answers')

if __name__=='__main__': main()
