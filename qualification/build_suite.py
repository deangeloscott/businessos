#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from common import ROOT, load_contracts, family_for, fixture_for, competitive_profile, output_policy, write_json

RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())
MISSIONS=json.loads((ROOT/'qualification/missions/missions.json').read_text())

def dimensions_for(profile):
    base=[x['id'] for x in RUBRICS['base']]
    return base + list(RUBRICS['profiles'].get(profile,[]))

def subcontract_ids(items, contract_id):
    out=[]
    for item in items or []:
        if isinstance(item,str): cid=item
        elif isinstance(item,dict): cid=item.get('id')
        else: cid=None
        if not isinstance(cid,str) or not cid.strip(): raise ValueError(f'{contract_id}: invalid required subcontract metadata {item!r}')
        out.append(cid.strip())
    return out

def candidate_task(c):
    """Turn a contract claim into a production-like user request without exposing the test target."""
    outcome=(c.get('business_outcome') or c.get('purpose') or c['title']).strip()
    profile=competitive_profile(c); extra=''
    if profile=='search_live_field':
        extra=' Inspect the current search/AI-answer field where relevant, compare multiple strong results, and use what you learn to make the result genuinely competitive rather than generic.'
    elif profile=='paid_and_persuasion_field':
        extra=' Inspect relevant current competitors, ads, landing paths, or persuasion surfaces where useful; treat longevity or engagement as signals rather than proof of profitability.'
    elif profile=='organic_attention_field':
        extra=' Use real visible performance evidence where available, normalize obvious context differences, and extract reusable mechanisms rather than copying expression.'
    elif output_policy(c)['artifact_required']:
        extra=' Create the actual usable deliverable, not a plan describing what could be created.'
    return (
        f'For the active business, {outcome.rstrip(".")}. {extra.strip()} '
        'Use AURA normally from this natural-language request: reuse relevant business state, use available tools and real evidence when the work requires them, and persist the useful business result. '
        'Do not invent missing facts, sources, tool use, execution, or outcomes. If something genuinely required is unavailable, leave a precise blocker instead of manufacturing completion.'
    ).replace('  ',' ').strip()

def hard_gates(c):
    gates=['checkpoint_before_exists','checkpoint_after_exists','candidate_receipt_exists','root_run_exists','root_run_contract_matches','root_run_completed','root_completion_evidence_valid','required_subcontracts_completed','required_subcontract_evidence_valid','workspace_valid','business_valid','completion_claim_truthful']
    if output_policy(c)['artifact_required']:
        gates += ['actual_artifact_exists','artifact_referenced_by_receipt','artifact_nontrivial','artifact_contract_specific']
    if c.get('writes'):
        gates += ['declared_write_type_observed_or_explicitly_justified']
    if competitive_profile(c) in {'search_live_field','paid_and_persuasion_field','organic_attention_field'}:
        gates += ['competitive_field_evidence_recorded','competitive_field_evidence_exists','competitive_field_evidence_event_specific','competitive_field_evidence_reconstructable']
    if c.get('artifact_role')=='customer_facing_production_root':
        gates += ['customer_facing_claim_governance_passed','prepublish_or_required_qa_recorded']
    return gates

def build():
    contracts=load_contracts(); ids={c['contract_id'] for c in contracts}; tests=[]
    for c in contracts:
        req=subcontract_ids((c.get('subcontracts') or {}).get('required') or [],c['contract_id'])
        tests.append({'test_id':'CONTRACT-'+c['contract_id'].replace('.','-').upper(),'kind':'contract_acceptance','contract_id':c['contract_id'],'contract_path':c['path'],'owner_system':c['owner_system'],'family':family_for(c['contract_id']),'fixture':fixture_for(c['contract_id'],c['owner_system']),'claim_under_test':{'title':c['title'],'purpose':c['purpose'],'business_outcome':c['business_outcome'],'completion_evidence':c['completion_evidence']},'candidate_task':candidate_task(c),'reads':c['reads'],'writes':c['writes'],'capabilities':c['capabilities'],'context':c['context'],'required_subcontracts':req,'unknown_required_subcontracts':sorted(x for x in req if x not in ids),'process_steps':c['process'],'output_policy':output_policy(c),'competitive_profile':competitive_profile(c),'rubric_dimensions':dimensions_for(competitive_profile(c)),'hard_gates':hard_gates(c),'artifact_role':c.get('artifact_role'),'risk':c.get('risk'),'autonomy_ceiling':c.get('autonomy_ceiling')})
    catalog=json.loads((ROOT/'core/capabilities/catalog.json').read_text()).get('capabilities',[]); coverage={}
    for cap in catalog:
        capid=cap['id']; required=[]; optional=[]
        for t in tests:
            cm=t.get('capabilities') or {}
            if capid in (cm.get('required') or []): required.append(t['test_id'])
            if capid in (cm.get('optional') or []): optional.append(t['test_id'])
        coverage[capid]={'description':cap.get('description'),'required_by':required,'optional_by':optional,'covered_by_contract_tests':sorted(set(required+optional))}
    return {'format_version':'1.0','suite_name':'AURA Business Capability Qualification Suite','contract_count':len(contracts),'contract_tests':tests,'capability_count':len(catalog),'capability_coverage':coverage,'unreferenced_capabilities':sorted(k for k,v in coverage.items() if not v['covered_by_contract_tests']),'domain_missions':MISSIONS['domain_missions'],'cross_domain_missions':MISSIONS['cross_domain_missions'],'marathon_missions':MISSIONS['marathon_missions'],'concurrency_missions':MISSIONS.get('concurrency_missions',[])}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default='qualification/generated/full-suite.json'); ap.add_argument('--stdout',action='store_true'); a=ap.parse_args(); suite=build()
    if any(t['unknown_required_subcontracts'] for t in suite['contract_tests']):
        bad=[(t['contract_id'],t['unknown_required_subcontracts']) for t in suite['contract_tests'] if t['unknown_required_subcontracts']]; raise SystemExit(f'Unknown required subcontract(s): {bad[:20]}')
    if a.stdout: print(json.dumps(suite,indent=2))
    else:
        p=ROOT/a.out; write_json(p,suite); print(f"generated {p}: {suite['contract_count']} contract tests, {len(suite['domain_missions'])} domain missions, {len(suite['cross_domain_missions'])} cross-domain missions, {len(suite['marathon_missions'])} marathon missions, {len(suite['concurrency_missions'])} concurrency missions")
if __name__=='__main__': main()
