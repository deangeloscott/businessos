#!/usr/bin/env python3
"""RC4/RC6 regressions for deterministic first-party/local website evidence."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; SCRIPTS=ROOT/'scripts'; sys.path.insert(0,str(SCRIPTS))
from validate_business import validate_business
from validate_local_evidence import local_evidence_errors
from context_plan import build_plan

BID='local-evidence-regression'; BASE=ROOT/'instances'/BID
SITE_A=ROOT/'test-inputs'/'_local-evidence-regression-site-a'
SITE_B=ROOT/'test-inputs'/'_local-evidence-regression-site-b'

def require(cond,msg):
    if not cond: raise AssertionError(msg)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def seed_site(site):
    site.mkdir(parents=True,exist_ok=True)
    (site/'index.html').write_text('<!doctype html><html><head><title>Northstar HVAC</title><meta name="description" content="HVAC repair"><script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Northstar HVAC"}</script></head><body><a href="/missing.html">Missing</a></body></html>')
    (site/'robots.txt').write_text('User-agent: *\nDisallow: /private/\n')
    (site/'sitemap.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/sitemap/0.9"><url><loc>https://example.test/index.html</loc></url></urlset>')

def main():
    for p in (BASE,SITE_A,SITE_B):
        if p.exists(): shutil.rmtree(p)
    try:
        run(SCRIPTS/'init_business.py',BID,'--name','Local Evidence Regression')
        seed_site(SITE_A); shutil.copytree(SITE_A,SITE_B)

        # RC6 identity regression: identical bytes at different source locators are distinct captures.
        ins_a=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE_A.relative_to(ROOT))).stdout)
        ins_b=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE_B.relative_to(ROOT))).stdout)
        require(ins_a['snapshot_hash']==ins_b['snapshot_hash'],'identical directories should have the same content snapshot hash')
        require(ins_a['source_ref']!=ins_b['source_ref'],'different source locators with identical bytes must have distinct SourceRecords')
        require(ins_a['manifest_path']!=ins_b['manifest_path'],'different source locators with identical bytes must have distinct manifests')
        ma=json.loads((ROOT/ins_a['manifest_path']).read_text()); mb=json.loads((ROOT/ins_b['manifest_path']).read_text())
        require(ma['source_identity']!=mb['source_identity'],'source identity must distinguish identical content at different locators')
        require(ma['source_root']==SITE_A.relative_to(ROOT).as_posix() and mb['source_root']==SITE_B.relative_to(ROOT).as_posix(),'each capture must preserve its own locator')

        # Same source + same snapshot is idempotent.
        ins_a2=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE_A.relative_to(ROOT))).stdout)
        require(ins_a2['source_ref']==ins_a['source_ref'] and ins_a2['manifest_path']==ins_a['manifest_path'],'same locator + snapshot should reuse the capture identity')

        jf=next((x for x in ins_a['fact_index'] if x['kind']=='html.jsonld_block' and x['path']=='index.html'),None)
        require(jf and 'is valid JSON' in jf['rendered'] and 'https://schema.org' in jf['rendered'],f'valid JSON-LD must be preserved deterministically, got {jf}')
        broken=next((x for x in ins_a['fact_index'] if x['kind']=='html.internal_link' and x.get('path')=='index.html' and 'does not resolve' in x['rendered']),None)
        require(broken,'broken local link should be captured deterministically')
        po=json.loads(run(SCRIPTS/'persist_site_observation.py',BID,'--source-ref',ins_a['source_ref'],'--fact-id',jf['id'],'--observation-type','structured_data_direct_observation','--id-suffix','jsonld-a').stdout)
        # Persist a historical direct observation against B before B changes.
        title_b=next(x for x in ins_b['fact_index'] if x['kind']=='html.title' and x['path']=='index.html')
        run(SCRIPTS/'persist_site_observation.py',BID,'--source-ref',ins_b['source_ref'],'--fact-id',title_b['id'],'--observation-type','title_direct_observation','--id-suffix','title-b-before')

        le,_=local_evidence_errors(BID); require(not le,f'valid local evidence should pass, got {le}')
        errors,_,_=validate_business(BID); require(not errors,f'valid local evidence should pass business validation, got {errors}')

        # Exact RC4 false-observation regression remains enforced.
        opath=BASE/'intelligence/observations'/f"{po['observation_id']}.json"; obs=json.loads(opath.read_text()); good=obs['statement']
        obs['statement']='Direct inspection found the homepage JSON-LD is corrupted and invalid.'; opath.write_text(json.dumps(obs,indent=2)+'\n')
        errors,_,_=validate_business(BID)
        require(any('statement does not exactly match its deterministic fact_refs' in e for e in errors),f'false direct observation must be rejected, got {errors}')
        obs['statement']=good; opath.write_text(json.dumps(obs,indent=2)+'\n')

        # Manual SourceRecord + prose observation may not bypass deterministic capture.
        ts=json.loads((BASE/'instance.json').read_text()).get('created_at') or '2026-01-01T00:00:00+00:00'
        manual_src={'id':f'src_{BID}_manual-site','object_type':'SourceRecord','schema_version':'1.0.0','business_id':BID,'created_at':ts,'updated_at':ts,'lineage':[],'source_type':'first_party_website_export','source_reference':str(SITE_A.relative_to(ROOT)),'origin':'manual','retrieved_at':ts,'published_at':None,'content_hash':None,'access_scope':'first_party_local','extensions':{}}
        msp=BASE/'intelligence/sources'/f"{manual_src['id']}.json";msp.write_text(json.dumps(manual_src,indent=2)+'\n')
        manual_obs={'id':f'obs_{BID}_manual-site','object_type':'Observation','schema_version':'1.0.0','business_id':BID,'created_at':ts,'updated_at':ts,'lineage':[manual_src['id']],'producer_system':'seo-aeo','observation_type':'technical_indexability_defects','subject_refs':[],'statement':'Direct inspection says the JSON-LD is corrupted.','source_refs':[manual_src['id']],'observed_at':ts,'method':'manual file inspection','extraction_confidence':1.0,'extensions':{}}
        mop=BASE/'intelligence/observations'/f"{manual_obs['id']}.json";mop.write_text(json.dumps(manual_obs,indent=2)+'\n')
        errors,_,_=validate_business(BID)
        require(any('without deterministic capture' in e for e in errors),f'manual local-site source must not support direct SEO facts, got {errors}')
        mop.unlink();msp.unlink()

        # RC6 historical-evidence regression: changing B does not erase/invalidate B-before evidence.
        (SITE_B/'index.html').write_text((SITE_B/'index.html').read_text().replace('Northstar HVAC</title>','Changed Northstar HVAC</title>'))
        errors,_,_=validate_business(BID)
        require(not errors,f'historical evidence must remain valid after its source later changes, got {errors}')
        stale=run(SCRIPTS/'persist_site_observation.py',BID,'--source-ref',ins_b['source_ref'],'--fact-id',title_b['id'],'--observation-type','title_direct_observation','--id-suffix','must-fail-stale',check=False)
        require(stale.returncode!=0 and 'changed after evidence capture' in (stale.stderr+stale.stdout),f'old capture must not support a new current Observation after source changes: {stale.stderr}{stale.stdout}')

        # Recapturing changed B creates a third, independent state; A and B-before remain intact.
        ins_b_after=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE_B.relative_to(ROOT))).stdout)
        require(ins_b_after['source_ref'] not in {ins_a['source_ref'],ins_b['source_ref']},'changed state at same locator must create a new SourceRecord')
        require(ins_b_after['manifest_path'] not in {ins_a['manifest_path'],ins_b['manifest_path']},'changed state at same locator must create a new manifest')
        require((ROOT/ins_a['manifest_path']).exists() and (ROOT/ins_b['manifest_path']).exists(),'older baseline/working captures must not be overwritten')
        require(json.loads((ROOT/ins_a['manifest_path']).read_text())['source_root']==SITE_A.relative_to(ROOT).as_posix(),'baseline provenance changed unexpectedly')
        require(json.loads((ROOT/ins_b['manifest_path']).read_text())['source_root']==SITE_B.relative_to(ROOT).as_posix(),'working-before provenance changed unexpectedly')
        title_b_after=next(x for x in ins_b_after['fact_index'] if x['kind']=='html.title' and x['path']=='index.html')
        run(SCRIPTS/'persist_site_observation.py',BID,'--source-ref',ins_b_after['source_ref'],'--fact-id',title_b_after['id'],'--observation-type','title_direct_observation','--id-suffix','title-b-after')
        errors,_,_=validate_business(BID); require(not errors,f'baseline, working-before, and working-after evidence should validate simultaneously, got {errors}')

        # Locator binding is enforceable: source_reference may not be pointed at another identical source.
        sp=BASE/'intelligence/sources'/f"{ins_b['source_ref']}.json"; srec=json.loads(sp.read_text()); original_ref=srec['source_reference']
        srec['source_reference']=SITE_A.relative_to(ROOT).as_posix(); sp.write_text(json.dumps(srec,indent=2)+'\n')
        errors,_,_=validate_business(BID)
        require(any('source_reference does not match local evidence manifest source_root' in e for e in errors),f'locator provenance mismatch must fail, got {errors}')
        srec['source_reference']=original_ref; sp.write_text(json.dumps(srec,indent=2)+'\n')

        policy=(ROOT/'core/policies/local-evidence.md').read_text()
        require('source identity' in policy.lower() and 'inspect_site_evidence.py' in policy and 'persist_site_observation.py' in policy,'local evidence policy missing RC6 identity/freshness rules')
        plan=build_plan(BID,'seo.bootstrap.asset-state-inventory')
        require('core/policies/local-evidence.md' in plan['files'],'SEO Observation-writing plan must load local-evidence policy')
        print('local evidence regressions passed')
    finally:
        for p in (BASE,SITE_A,SITE_B):
            if p.exists(): shutil.rmtree(p)
        r=ROOT/'runtime/runs'/BID
        if r.exists(): shutil.rmtree(r)
if __name__=='__main__': main()
