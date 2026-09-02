#!/usr/bin/env python3
"""Build qualification cases that test real business work, not internal AURA ceremony."""
from pathlib import Path
import argparse,json
from common import ROOT,load_contracts,family_for,fixture_for,competitive_profile,output_policy,write_json

RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())
MISSIONS=json.loads((ROOT/'qualification/missions/missions.json').read_text())

def dimensions_for(profile):return [x['id'] for x in RUBRICS['base']]+list(RUBRICS['profiles'].get(profile,[]))
def workflow_ids(items,workflow_id):
    """Expose authored supporting Workflow knowledge to reviewers without making it an execution gate."""
    out=[]
    for item in items or []:
        if isinstance(item,str):wid=item
        elif isinstance(item,dict):wid=item.get('id')
        else:wid=None
        if not isinstance(wid,str) or not wid.strip():raise ValueError(f'{workflow_id}: invalid supporting Workflow metadata {item!r}')
        out.append(wid.strip())
    return out
def candidate_task(c):
    outcome=(c.get('business_outcome') or c.get('purpose') or c['title']).strip();profile=competitive_profile(c);extra=''
    if profile=='search_live_field':extra='Inspect enough of the current search/AI-answer field to understand the competitive pattern and make the result genuinely competitive rather than generic. Start with a small credible sample of strong results and expand only if more evidence could materially change the work.'
    elif profile=='paid_and_persuasion_field':extra='Inspect enough relevant current competitors, ads, landing paths, or persuasion surfaces to understand the market pattern; expand only when more evidence could materially change the work, and treat longevity or engagement as signals rather than proof of profitability.'
    elif profile=='organic_attention_field':extra='Use enough real visible performance evidence to understand the relevant pattern, normalize obvious context differences, expand only when more evidence could materially change the work, and extract reusable mechanisms rather than copying expression.'
    elif output_policy(c)['artifact_required']:extra='Create the actual usable deliverable, not a plan, outline, generic substitute, or description of what could be created.'
    return (f'For the active business, {outcome.rstrip(".")}. {extra} Use AURA normally from this natural-language request: reuse relevant business state, use available tools, other Skills, and real evidence when the work requires them, do the substantive business work, and preserve the material result so future organizational work can continue from it. Do not invent missing facts, sources, tool use, execution, or outcomes. If something genuinely required is unavailable, state the precise blocker instead of manufacturing completion.').replace('  ',' ').strip()
def hard_gates(c):
    """Deterministic integrity floor; professional excellence is judged separately."""
    gates=['workspace_valid','business_valid','material_result_observed','completion_claim_truthful']
    if output_policy(c)['artifact_required']:gates+=['actual_artifact_exists','artifact_nontrivial','artifact_event_specific']
    if competitive_profile(c) in {'search_live_field','paid_and_persuasion_field','organic_attention_field'}:gates+=['competitive_field_evidence_recorded','competitive_field_evidence_exists','competitive_field_evidence_event_specific','competitive_field_evidence_reconstructable']
    if c.get('artifact_role')=='customer_facing_production_root':gates+=['customer_facing_claim_governance_passed']
    return gates

def build():
    contracts=load_contracts();ids={c['contract_id'] for c in contracts};tests=[]
    for c in contracts:
        if c.get('type')!='workflow':continue
        normal=workflow_ids((c.get('workflows') or {}).get('required') or [],c['contract_id']);conditional=workflow_ids((c.get('workflows') or {}).get('conditional') or [],c['contract_id'])
        tests.append({'test_id':'WORKFLOW-'+c['contract_id'].replace('.','-').upper(),'kind':'workflow_acceptance','contract_id':c['contract_id'],'workflow_id':c['contract_id'],'contract_path':c['path'],'workflow_path':c['path'],'owner_system':c['owner_system'],'family':family_for(c['contract_id']),'fixture':fixture_for(c['contract_id'],c['owner_system']),'claim_under_test':{'title':c['title'],'purpose':c['purpose'],'business_outcome':c['business_outcome'],'completion_evidence':c['completion_evidence']},'candidate_task':candidate_task(c),'reads':c['reads'],'writes':c['writes'],'context':c['context'],'normally_used_workflows':normal,'conditional_workflows':conditional,'unknown_composed_workflows':sorted(x for x in normal+conditional if x not in ids),'process_steps':c['process'],'output_policy':output_policy(c),'competitive_profile':competitive_profile(c),'rubric_dimensions':dimensions_for(competitive_profile(c)),'hard_gates':hard_gates(c),'artifact_role':c.get('artifact_role')})
    return {'format_version':'3.0','suite_name':'AURA Real Business Work Qualification Suite','qualification_model':'output_and_evidence_first','workflow_count':len(tests),'contract_count':len(tests),'workflow_tests':tests,'contract_tests':tests,'composition_missions':MISSIONS.get('composition_missions',[]),'domain_missions':MISSIONS['domain_missions'],'cross_domain_missions':MISSIONS['cross_domain_missions'],'marathon_missions':MISSIONS['marathon_missions']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='qualification/generated/full-suite.json');ap.add_argument('--stdout',action='store_true');a=ap.parse_args();suite=build()
    if any(t['unknown_composed_workflows'] for t in suite['workflow_tests']):
        bad=[(t['workflow_id'],t['unknown_composed_workflows']) for t in suite['workflow_tests'] if t['unknown_composed_workflows']];raise SystemExit(f'Unknown composed Workflow(s): {bad[:20]}')
    if a.stdout:print(json.dumps(suite,indent=2))
    else:
        p=ROOT/a.out;write_json(p,suite);print(f"generated {p}: {suite['workflow_count']} Workflow tests, {len(suite['composition_missions'])} composition missions, {len(suite['domain_missions'])} domain missions, {len(suite['cross_domain_missions'])} cross-domain missions, {len(suite['marathon_missions'])} marathon missions")

if __name__=='__main__':main()
