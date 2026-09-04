#!/usr/bin/env python3
"""Build qualification cases that test real business work, not internal AURA ceremony.

The deterministic suite establishes coverage, fixture context, reference integrity, and a
small universal honesty floor. A capable evaluator judges whether each actual result fulfilled
the Workflow's business outcome with the necessary research, artifact creation, execution,
QA, and evidence. Python does not infer those semantic requirements from Workflow ids.
"""
from pathlib import Path
import argparse,json
from common import ROOT,load_workflows,family_for,fixture_for,write_json

RUBRICS=json.loads((ROOT/'qualification/rubrics/rubrics.json').read_text())
MISSIONS=json.loads((ROOT/'qualification/missions/missions.json').read_text())
BASE_DIMENSIONS=[x['id'] for x in RUBRICS['base']]


def candidate_task(c):
    outcome=(c.get('business_outcome') or c.get('purpose') or c['title']).strip()
    return (f'For the active business, {outcome.rstrip(".")}. Use AURA normally from this natural-language request: reuse relevant business state, use available tools, other Skills, and real evidence when the work requires them, do the substantive business work, and preserve the material result so future organizational work can continue from it. Do not invent missing facts, sources, tool use, execution, or outcomes. If something genuinely required is unavailable, state the precise blocker instead of manufacturing completion.').replace('  ',' ').strip()


def hard_gates():
    """Universal deterministic honesty/integrity floor.

    Whether a particular Workflow required a finished artifact, current field research,
    rendered QA, a specific amount of evidence, or another substantive method is a semantic
    quality judgment made from the task, Workflow, and actual result by the evaluator.
    """
    return ['workspace_valid','business_valid','material_result_observed','completion_claim_truthful']


def build():
    workflows=load_workflows();tests=[]
    for c in workflows:
        if c.get('type')!='workflow':continue
        tests.append({
            'test_id':'WORKFLOW-'+c['workflow_id'].replace('.','-').upper(),
            'kind':'workflow_acceptance','workflow_id':c['workflow_id'],'workflow_path':c['path'],
            'owner_system':c['owner_system'],'family':family_for(c['workflow_id']),
            'fixture':fixture_for(c['workflow_id'],c['owner_system']),
            'claim_under_test':{
                'title':c['title'],'purpose':c['purpose'],'business_outcome':c['business_outcome'],
                'completion_evidence':c['completion_evidence']
            },
            'candidate_task':candidate_task(c),'reads':c['reads'],'writes':c['writes'],'context':c['context'],
            'process_steps':c['process'],'rubric_dimensions':list(BASE_DIMENSIONS),'hard_gates':hard_gates(),
            'evaluation_rule':'Judge the real business result against the request and authored Workflow expertise. Equivalent or better methods are valid; missing substantive work is not.'
        })
    return {
        'format_version':'4.0','suite_name':'AURA Real Business Work Qualification Suite',
        'qualification_model':'universal_integrity_floor_plus_capable_quality_review',
        'workflow_count':len(tests),'workflow_tests':tests,
        'composition_missions':MISSIONS.get('composition_missions',[]),'domain_missions':MISSIONS['domain_missions'],
        'cross_domain_missions':MISSIONS['cross_domain_missions'],'marathon_missions':MISSIONS['marathon_missions']
    }


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='qualification/generated/full-suite.json');ap.add_argument('--stdout',action='store_true');a=ap.parse_args();suite=build()
    if a.stdout:print(json.dumps(suite,indent=2))
    else:
        p=ROOT/a.out;write_json(p,suite);print(f"generated {p}: {suite['workflow_count']} Workflow tests, {len(suite['composition_missions'])} composition missions, {len(suite['domain_missions'])} domain missions, {len(suite['cross_domain_missions'])} cross-domain missions, {len(suite['marathon_missions'])} marathon missions")

if __name__=='__main__':main()
