#!/usr/bin/env python3
"""Regressions for optional deterministic first-party/local-site capture integrity.

AURA's inspector is useful for reproducible evidence, but it is not the only legitimate
way a capable model/harness may inspect first-party material.
"""
from pathlib import Path
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];SCRIPTS=ROOT/'scripts';sys.path.insert(0,str(SCRIPTS))
from validate_business import validate_business
from validate_local_evidence import local_evidence_errors
from context_plan import build_plan

BID='local-evidence-regression';BASE=ROOT/'instances'/BID
SITE_A=ROOT/'test-inputs'/'_local-evidence-regression-site-a';SITE_B=ROOT/'test-inputs'/'_local-evidence-regression-site-b'


def require(cond,msg):
    if not cond:raise AssertionError(msg)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def seed_site(site):
    site.mkdir(parents=True,exist_ok=True)
    (site/'index.html').write_text('<!doctype html><html><head><title>Northstar HVAC</title><meta name="description" content="HVAC repair"><script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Northstar HVAC"}</script></head><body><a href="/missing.html">Missing</a></body></html>')
    (site/'robots.txt').write_text('User-agent: *\nDisallow: /private/\n')
    (site/'sitemap.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.test/index.html</loc></url></urlset>')


def main():
    for p in (BASE,SITE_A,SITE_B):
        if p.exists():shutil.rmtree(p)
    try:
        run(SCRIPTS/'init_business.py',BID,'--name','Local Evidence Regression')
        seed_site(SITE_A);shutil.copytree(SITE_A,SITE_B)

        # Same bytes at different locators are distinct evidence sources; same locator+state is idempotent.
        ins_a=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE_A.relative_to(ROOT))).stdout)
        ins_b=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE_B.relative_to(ROOT))).stdout)
        require(ins_a['snapshot_hash']==ins_b['snapshot_hash'],'identical directories should share a content snapshot hash')
        require(ins_a['source_ref']!=ins_b['source_ref'],'different source locators must retain distinct SourceRecords')
        require(ins_a['manifest_path']!=ins_b['manifest_path'],'different source locators must retain distinct manifests')
        ma=json.loads((ROOT/ins_a['manifest_path']).read_text());mb=json.loads((ROOT/ins_b['manifest_path']).read_text())
        require(ma['source_identity']!=mb['source_identity'],'source identity must preserve locator identity')
        require(ma['source_root']==SITE_A.relative_to(ROOT).as_posix() and mb['source_root']==SITE_B.relative_to(ROOT).as_posix(),'capture locator provenance was lost')
        ins_a2=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE_A.relative_to(ROOT))).stdout)
        require(ins_a2['source_ref']==ins_a['source_ref'] and ins_a2['manifest_path']==ins_a['manifest_path'],'same locator + snapshot should reuse capture identity')

        jf=next((x for x in ins_a['fact_index'] if x['kind']=='html.jsonld_block' and x['path']=='index.html'),None)
        require(jf and 'is valid JSON' in jf['rendered'] and 'https://schema.org' in jf['rendered'],f'valid JSON-LD capture regressed: {jf}')
        broken=next((x for x in ins_a['fact_index'] if x['kind']=='html.internal_link' and x.get('path')=='index.html' and 'does not resolve' in x['rendered']),None)
        require(broken,'broken local link should be mechanically capturable')
        po=json.loads(run(SCRIPTS/'persist_site_observation.py',BID,'--source-ref',ins_a['source_ref'],'--fact-id',jf['id'],'--observation-type','structured_data_direct_observation','--id-suffix','jsonld-a').stdout)
        title_b=next(x for x in ins_b['fact_index'] if x['kind']=='html.title' and x['path']=='index.html')
        run(SCRIPTS/'persist_site_observation.py',BID,'--source-ref',ins_b['source_ref'],'--fact-id',title_b['id'],'--observation-type','title_direct_observation','--id-suffix','title-b-before')

        le,_=local_evidence_errors(BID);require(not le,f'valid deterministic capture should pass its own integrity checks: {le}')
        errors,_,_=validate_business(BID);require(not errors,f'valid captured evidence should pass business validation: {errors}')

        # Fact refs are mechanically verifiable, but AURA must not require the model's prose
        # to exactly equal its own canned renderer.
        opath=BASE/'intelligence/observations'/f"{po['observation_id']}.json";obs=json.loads(opath.read_text())
        obs['statement']='Direct inspection found valid Organization JSON-LD on the homepage.';opath.write_text(json.dumps(obs,indent=2)+'\n')
        le,_=local_evidence_errors(BID);require(not le,f'natural-language restatement should not fail deterministic capture integrity: {le}')
        obs=json.loads(opath.read_text());obs['extensions']['businessos_local_evidence']['fact_refs']=['fact_missing'];opath.write_text(json.dumps(obs,indent=2)+'\n')
        le,_=local_evidence_errors(BID);require(any('unknown deterministic site fact' in e for e in le),f'unknown declared deterministic fact ref should fail: {le}')
        obs['extensions']['businessos_local_evidence']['fact_refs']=[jf['id']];opath.write_text(json.dumps(obs,indent=2)+'\n')

        # A non-AURA first-party inspection path is not invalid merely because it lacks
        # businessos_local_evidence metadata. Normal evidence/truth policy governs it.
        ts=json.loads((BASE/'instance.json').read_text()).get('created_at') or '2026-01-01T00:00:00+00:00'
        manual_src={'id':f'src_{BID}_manual-site','object_type':'SourceRecord','schema_version':'1.0.0','business_id':BID,'created_at':ts,'updated_at':ts,'lineage':[],'source_type':'first_party_website_export','source_reference':str(SITE_A.relative_to(ROOT)),'origin':'browser/filesystem inspection','retrieved_at':ts,'published_at':None,'content_hash':None,'access_scope':'first_party_local','extensions':{}}
        msp=BASE/'intelligence/sources'/f"{manual_src['id']}.json";msp.write_text(json.dumps(manual_src,indent=2)+'\n')
        manual_obs={'id':f'obs_{BID}_manual-site','object_type':'Observation','schema_version':'1.0.0','business_id':BID,'created_at':ts,'updated_at':ts,'lineage':[manual_src['id']],'observation_type':'manual_first_party_observation','subject_refs':[],'statement':'The inspected homepage contains Organization structured data.','source_refs':[manual_src['id']],'observed_at':ts,'method':'browser/filesystem inspection','extraction_confidence':0.95,'extensions':{}}
        mop=BASE/'intelligence/observations'/f"{manual_obs['id']}.json";mop.write_text(json.dumps(manual_obs,indent=2)+'\n')
        le,_=local_evidence_errors(BID);require(not any(manual_src['id'] in e or manual_obs['id'] in e for e in le),f'local-evidence helper gated another evidence method: {le}')

        # Historical deterministic evidence stays valid after the source changes, while an
        # old snapshot cannot be used to manufacture a new current direct observation.
        (SITE_B/'index.html').write_text((SITE_B/'index.html').read_text().replace('Northstar HVAC</title>','Changed Northstar HVAC</title>'))
        le,_=local_evidence_errors(BID);require(not le,f'historical deterministic evidence must remain internally valid after source changes: {le}')
        stale=run(SCRIPTS/'persist_site_observation.py',BID,'--source-ref',ins_b['source_ref'],'--fact-id',title_b['id'],'--observation-type','title_direct_observation','--id-suffix','must-fail-stale',check=False)
        require(stale.returncode!=0 and 'changed after evidence capture' in (stale.stderr+stale.stdout),f'old snapshot must not support a new current Observation: {stale.stderr}{stale.stdout}')
        ins_b_after=json.loads(run(SCRIPTS/'inspect_site_evidence.py',BID,str(SITE_B.relative_to(ROOT))).stdout)
        require(ins_b_after['source_ref'] not in {ins_a['source_ref'],ins_b['source_ref']},'changed state at same locator must create a new capture identity')
        require((ROOT/ins_a['manifest_path']).exists() and (ROOT/ins_b['manifest_path']).exists(),'historical captures must not be overwritten')

        # If deterministic metadata is declared, locator binding remains strict.
        sp=BASE/'intelligence/sources'/f"{ins_b['source_ref']}.json";srec=json.loads(sp.read_text());original_ref=srec['source_reference']
        srec['source_reference']=SITE_A.relative_to(ROOT).as_posix();sp.write_text(json.dumps(srec,indent=2)+'\n')
        le,_=local_evidence_errors(BID);require(any('source_reference does not match local evidence manifest source_root' in e for e in le),f'declared deterministic locator mismatch must fail: {le}')
        srec['source_reference']=original_ref;sp.write_text(json.dumps(srec,indent=2)+'\n')

        policy=(ROOT/'core/policies/local-evidence.md').read_text()
        require('does **not** require one particular inspector' in policy and 'optional helpers' in policy and 'does not require an Observation' in policy,'local evidence policy lost harness-neutral boundary')
        plan=build_plan(BID,'seo.bootstrap.asset-state-inventory')
        require('core/policies/local-evidence.md' in plan['files'],'SEO evidence-aware Workflow plan should load local-evidence policy')
        print('local evidence regressions passed: deterministic capture integrity without making AURA the only evidence path or sentence renderer')
    finally:
        for p in (BASE,SITE_A,SITE_B):
            if p.exists():shutil.rmtree(p)
        r=ROOT/'runtime/runs'/BID
        if r.exists():shutil.rmtree(r)


if __name__=='__main__':main()
