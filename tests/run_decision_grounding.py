#!/usr/bin/env python3
"""Regressions for structural evidence -> inference -> unknown separation in Opportunities."""
from pathlib import Path
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];SCRIPTS=ROOT/'scripts';sys.path.insert(0,str(SCRIPTS))
from validate_business import validate_business
from context_plan import build_plan

BID='decision-grounding-regression';BASE=ROOT/'instances'/BID;SITE=ROOT/'test-inputs'/'_decision-grounding-regression-site'

def require(cond,msg):
    if not cond:raise AssertionError(msg)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def write_op(statement,diagnosis,measured=None,fact_refs=None,inference_refs=None):
    inst=json.loads((BASE/'instance.json').read_text());ts=inst.get('created_at') or '2026-01-01T00:00:00+00:00'
    obsfiles=list((BASE/'intelligence/observations').glob('*.json'));require(obsfiles,'expected deterministic observation')
    obs=json.loads(obsfiles[0].read_text());oid=obs['id'];facts=fact_refs if fact_refs is not None else [oid];irefs=inference_refs if inference_refs is not None else [oid]
    op={
      'id':f'opp_{BID}_test','object_type':'Opportunity','schema_version':'1.0.0','business_id':BID,
      'created_at':ts,'updated_at':ts,'lineage':['seo.diagnosis.detectors.indexing'],'owner_system':'seo-aeo',
      'title':'Repair prerequisite indexability configuration','statement':statement,'status':'prioritized',
      'objective_refs':[],'origin_insight_refs':[],'evidence_links':[oid],'affected_refs':[],
      'diagnosis':diagnosis,'constraints':['Diagnostic evidence only'],
      'priority_assessment':{'rationale':'Dependency-first technical remediation.'},
      'recommended_intervention_types':['indexability'],'dependencies':[],
      'reasoning_basis':{
        'fact_refs':facts,'measured_refs':measured or [],
        'inferences':[{'statement':'Correcting an unintended indexability blocker may be useful prerequisite work.','basis_refs':irefs}],
        'unknowns':['Actual search-engine indexing/ranking state is unmeasured.','Traffic, leads, economics, and AI-answer citation behavior are unknown.']
      },
      'domain_data':{},'extensions':{'businessos':{'origin':'preexisting'}}
    }
    p=BASE/'decisions/opportunities'/f"{op['id']}.json";p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(op,indent=2)+'\n');return p,oid

def errors():return validate_business(BID)[0]

def main():
    if BASE.exists():shutil.rmtree(BASE)
    if SITE.exists():shutil.rmtree(SITE)
    try:
        run(SCRIPTS/'init_business.py',BID,'--name','Decision Grounding Regression')
        SITE.mkdir(parents=True,exist_ok=True)
        (SITE/'index.html').write_text('<!doctype html><html><head><title>HVAC Replacement</title><meta name="robots" content="noindex,follow"></head><body>Replacement</body></html>')
        (SITE/'robots.txt').write_text('User-agent: *\nDisallow: /resources/\n')
        (SITE/'sitemap.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/sitemap/0.9"></urlset>')
        ins=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE.relative_to(ROOT))).stdout)
        f=next(x for x in ins['fact_index'] if x['kind']=='html.meta_robots')
        po=json.loads(run(SCRIPTS/'persist_site_observation.py',BID,'--source-ref',ins['source_ref'],'--fact-id',f['id'],'--observation-type','noindex_directive','--id-suffix','noindex').stdout)
        oid=po['observation_id']

        good,_=write_op(
            'The page has a directly observed noindex directive; if unintended, correcting it may be useful prerequisite technical work.',
            'Observed configuration and derived implications are kept distinct from unmeasured search and business outcomes.'
        )
        e=errors();require(not e,f'grounded Opportunity without numeric confidence should pass, got {e}')

        op=json.loads(good.read_text());del op['reasoning_basis'];good.write_text(json.dumps(op,indent=2)+'\n')
        e=errors();require(any('reasoning_basis' in x for x in e),f'prioritized Opportunity without reasoning basis must fail, got {e}')

        good.unlink();write_op('A candidate action.','Grounded structurally.',fact_refs=['obs_missing'])
        e=errors();require(any('missing canonical object' in x for x in e),f'missing fact reference must fail, got {e}')

        good.unlink();write_op('A candidate action.','Grounded structurally.',fact_refs=[oid],inference_refs=['obs_missing'])
        e=errors();require(any('inference references missing canonical object' in x for x in e),f'missing inference reference must fail, got {e}')

        # A direct local-site configuration Observation is evidence, but it must not be relabeled measured outcome/performance evidence.
        good.unlink();write_op('The page has a noindex directive.','Actual downstream performance remains unknown.',measured=[oid])
        e=errors();require(any('not measured outcome/performance evidence' in x for x in e),f'local config Observation must not satisfy measured outcome support, got {e}')

        # Natural-language interpretation belongs to the model/policy layer, not deterministic regex validation.
        good.unlink();write_op(
            'This could be our highest-value page and traffic may be down; verify those business claims before treating them as established fact.',
            'The model must interpret and ground the statement using the policy; the structural validator should not police keywords.'
        )
        e=errors();require(not e,f'keyword semantics must not be deterministically rejected, got {e}')

        plan=build_plan(BID,'seo.diagnosis.detectors.indexing')
        require('core/policies/decision-grounding.md' in plan['files'],'Opportunity-writing plan must load decision-grounding policy')
        policy=(ROOT/'core/policies/decision-grounding.md').read_text()
        require('reasoning_basis' in policy and 'Leading signals and measured outcomes' in policy and 'not a deterministic prose rules engine' in policy,'decision grounding policy missing model-owned grounding boundaries')
        print('decision grounding regressions passed with structural validation and model-owned semantics')
    finally:
        if BASE.exists():shutil.rmtree(BASE)
        if SITE.exists():shutil.rmtree(SITE)
        r=ROOT/'runtime/runs'/BID
        if r.exists():shutil.rmtree(r)

if __name__=='__main__':main()
