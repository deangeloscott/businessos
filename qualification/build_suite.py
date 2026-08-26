#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from common import ROOT, load_contracts, family_for, fixture_for, competitive_profile, output_policy, write_json

RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())
MISSIONS=json.loads((ROOT/'qualification/missions/missions.json').read_text())

def dimensions_for(profile):
    base=[x['id'] for x in RUBRICS['base']]
    return base + list(RUBRICS['profiles'].get(profile,[]))

def candidate_task(c):
    outcome=c.get('business_outcome') or c.get('purpose') or c['title']
    run_when=c.get('run_when') or ''
    profile=competitive_profile(c)
    extra=''
    if profile=='search_live_field':
        extra=' Inspect the live search/AI-answer field when the environment permits, compare multiple leaders, and create the actual competitively ready result rather than a generic best-practice output.'
    elif profile=='paid_and_persuasion_field':
        extra=' Inspect multiple relevant competitors/ads/landing paths using current transparency or creative surfaces when available; calibrate longevity/engagement as proxies rather than proof of profit; create the actual production-ready result.'
    elif profile=='organic_attention_field':
        extra=' Identify top/outlier content using visible performance proxies normalized to context where possible, extract mechanisms rather than copying expression, and produce the actual native result.'
    elif output_policy(c)['artifact_required']:
        extra=' Produce the actual promised artifact at professional usable quality; a plan, outline, mock description, or statement of what could be created does not satisfy this test unless this contract specifically promises that planning artifact.'
    return f"Execute AURA contract {c['contract_id']} for the active qualification business as a real production task. Intended outcome: {outcome} {run_when}{extra} Follow AURA governance, required subcontracts, evidence/provenance, and completion rules. Continue until the contract is genuinely complete or record a specific external blocker."

def hard_gates(c):
    gates=[
        'checkpoint_before_exists','checkpoint_after_exists','candidate_receipt_exists',
        'root_run_exists','root_run_contract_matches','root_run_completed',
        'required_subcontracts_completed','workspace_valid','business_valid','completion_claim_truthful'
    ]
    if output_policy(c)['artifact_required']:
        gates += ['actual_artifact_exists','artifact_referenced_by_receipt']
    if c.get('writes'):
        gates += ['declared_write_type_observed_or_explicitly_justified']
    if c.get('artifact_role')=='customer_facing_production_root':
        gates += ['customer_facing_claim_governance_passed','prepublish_or_required_qa_recorded']
    return gates

def build():
    contracts=load_contracts(); ids={c['contract_id'] for c in contracts}; tests=[]
    for c in contracts:
        req=list((c.get('subcontracts') or {}).get('required') or [])
        tests.append({
            'test_id':'CONTRACT-'+c['contract_id'].replace('.','-').upper(),
            'kind':'contract_acceptance','contract_id':c['contract_id'],'contract_path':c['path'],
            'owner_system':c['owner_system'],'family':family_for(c['contract_id']),'fixture':fixture_for(c['contract_id'],c['owner_system']),
            'claim_under_test':{'title':c['title'],'purpose':c['purpose'],'business_outcome':c['business_outcome'],'completion_evidence':c['completion_evidence']},
            'candidate_task':candidate_task(c),'reads':c['reads'],'writes':c['writes'],'capabilities':c['capabilities'],'context':c['context'],
            'required_subcontracts':req,'unknown_required_subcontracts':sorted(x for x in req if x not in ids),'process_steps':c['process'],
            'output_policy':output_policy(c),'competitive_profile':competitive_profile(c),'rubric_dimensions':dimensions_for(competitive_profile(c)),
            'hard_gates':hard_gates(c),'artifact_role':c.get('artifact_role'),'risk':c.get('risk'),'autonomy_ceiling':c.get('autonomy_ceiling')
        })
    return {'format_version':'1.0','suite_name':'AURA Business Capability Qualification Suite','contract_count':len(contracts),'contract_tests':tests,
            'domain_missions':MISSIONS['domain_missions'],'cross_domain_missions':MISSIONS['cross_domain_missions'],'marathon_missions':MISSIONS['marathon_missions']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default='qualification/generated/full-suite.json'); ap.add_argument('--stdout',action='store_true'); a=ap.parse_args()
    suite=build()
    if any(t['unknown_required_subcontracts'] for t in suite['contract_tests']):
        bad=[(t['contract_id'],t['unknown_required_subcontracts']) for t in suite['contract_tests'] if t['unknown_required_subcontracts']]
        raise SystemExit(f'Unknown required subcontract(s): {bad[:20]}')
    if a.stdout: print(json.dumps(suite,indent=2))
    else:
        p=ROOT/a.out; write_json(p,suite); print(f"generated {p}: {suite['contract_count']} contract tests, {len(suite['domain_missions'])} domain missions, {len(suite['cross_domain_missions'])} cross-domain missions, {len(suite['marathon_missions'])} marathon missions")
if __name__=='__main__': main()
