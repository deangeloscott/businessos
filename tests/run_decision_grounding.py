#!/usr/bin/env python3
"""RC5 regressions for evidence -> inference -> unknown separation in Opportunity objects."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; SCRIPTS=ROOT/'scripts'; sys.path.insert(0,str(SCRIPTS))
from validate_business import validate_business
from validate_opportunity_grounding import opportunity_grounding_errors
from context_plan import build_plan

BID='decision-grounding-regression'; BASE=ROOT/'instances'/BID; SITE=ROOT/'test-inputs'/'_decision-grounding-regression-site'

def require(cond,msg):
    if not cond: raise AssertionError(msg)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def write_op(statement,diagnosis,priority='Dependency-first technical remediation.',unknowns=None,measured=None):
    inst=json.loads((BASE/'instance.json').read_text()); ts=inst.get('created_at') or '2026-01-01T00:00:00+00:00'
    obsfiles=list((BASE/'intelligence/observations').glob('*.json')); require(obsfiles,'expected deterministic observation')
    obs=json.loads(obsfiles[0].read_text()); oid=obs['id']
    op={
      'id':f'opp_{BID}_test','object_type':'Opportunity','schema_version':'1.0.0','business_id':BID,
      'created_at':ts,'updated_at':ts,'lineage':['seo.diagnosis.detectors.indexing'],'owner_system':'seo-aeo',
      'title':'Repair prerequisite indexability configuration','statement':statement,'status':'prioritized',
      'objective_refs':[],'origin_insight_refs':[],'evidence_links':[oid],'affected_refs':[],
      'diagnosis':diagnosis,'confidence':0.9,'urgency':0.8,'strategic_leverage':0.8,
      'risk':'Low implementation risk; verify intent before changing directives.','constraints':['Diagnostic evidence only'],
      'priority_assessment':{'rank':1,'rationale':priority},
      'recommended_intervention_types':['indexability'],'dependencies':[],
      'reasoning_basis':{
        'fact_refs':[oid], 'measured_refs': measured or [],
        'inferences':[{'statement':'Correcting an unintended indexability blocker should precede lower-priority presentation work because normal discoverability depends on eligible/crawlable content.','basis_refs':[oid],'confidence':0.9}],
        'unknowns':unknowns or ['Actual search-engine indexing/ranking state is unmeasured.','Traffic, leads, economics, and AI-answer citation behavior are unknown.']
      },
      'domain_data':{},'extensions':{'businessos':{'origin':'preexisting'}}
    }
    p=BASE/'decisions/opportunities'/f"{op['id']}.json"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(op,indent=2)+'\n'); return p

def errors():
    return validate_business(BID)[0]

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    if SITE.exists(): shutil.rmtree(SITE)
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

        good=write_op(
            'The page has a directly observed noindex directive; if that directive is unintended, correcting it is prerequisite technical work before lower-priority presentation optimization.',
            'Observed: the local export contains noindex,follow. Inference: an unintended noindex creates index-eligibility risk and should be corrected before dependent optimization. Unknown: actual live indexing, rankings, traffic, leads, economics, and AI-answer presence were not measured.'
        )
        e=errors(); require(not e,f'calibrated Opportunity should pass, got {e}')

        op=json.loads(good.read_text()); del op['reasoning_basis']; good.write_text(json.dumps(op,indent=2)+'\n')
        e=errors(); require(any('reasoning_basis' in x for x in e),f'prioritized Opportunity without reasoning basis must fail, got {e}')

        # Restore, then reproduce RC4 unsupported economics.
        good.unlink(); write_op(
            'Fix this page first because replacement is Northstar HVAC\'s highest-value service.',
            'The noindex is directly observed; correcting it is prerequisite work.',
            priority='Business relevance is direct because replacement is a high-value service.'
        )
        e=errors(); require(any('economic/value assertion' in x for x in e),f'unsupported highest/high-value service claim must fail, got {e}')

        # Reproduce RC4 overclaim from robots/indexability to absolute search/AI outcome.
        good.unlink(); write_op(
            'The robots block is preventing indexing and any AI-answer citation of this resource.',
            'The resource is invisible to both search engines and AI answer systems.',
        )
        e=errors(); require(any('overstates an inferred search/AI outcome' in x for x in e),f'absolute indexing/citation inference must fail, got {e}')

        # Unmeasured performance state must not be asserted as observed outcome.
        good.unlink(); write_op(
            'Organic traffic is down and rankings are low on this page.',
            'The technical directive is directly observed, but no performance source is available.'
        )
        e=errors(); require(any('performance without measured outcome evidence' in x for x in e),f'unmeasured performance claim must fail, got {e}')

        # Local configuration observation cannot be relabeled measured search performance.
        good.unlink(); write_op(
            'The page has a noindex directive and should be reviewed first as a prerequisite technical condition.',
            'Observed configuration is deterministic; actual search performance remains unknown.',
            measured=[oid]
        )
        e=errors(); require(any('not measured search/AI/business performance' in x for x in e),f'local config Observation must not satisfy measured outcome support, got {e}')

        plan=build_plan(BID,'seo.diagnosis.detectors.indexing')
        require('core/policies/decision-grounding.md' in plan['files'],'Opportunity-writing plan must load decision-grounding policy')
        policy=(ROOT/'core/policies/decision-grounding.md').read_text()
        require('highest-value' in policy and 'AI answer' in policy and 'reasoning_basis' in policy,'decision grounding policy missing key boundaries')
        print('decision grounding regressions passed')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
        if SITE.exists(): shutil.rmtree(SITE)
        r=ROOT/'runtime/runs'/BID
        if r.exists(): shutil.rmtree(r)

if __name__=='__main__': main()
