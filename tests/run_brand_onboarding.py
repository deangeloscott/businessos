#!/usr/bin/env python3
"""Regressions for first-class Brand onboarding, provenance, and downstream retrieval."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'
sys.path.insert(0,str(S))
from context_plan import build_plan
from validate_business import validate_business

BID='brand-onboarding-test'
TMP=ROOT/'runtime'/'brand-onboarding-test'

def req(cond,msg):
    if not cond: raise AssertionError(msg)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def clean(bid):
    for p in [ROOT/'instances'/bid, ROOT/'runtime'/'runs'/bid]:
        if p.exists(): shutil.rmtree(p)

def main():
    clean(BID)
    if TMP.exists(): shutil.rmtree(TMP)
    try:
        TMP.mkdir(parents=True,exist_ok=True)
        overview=TMP/'BUSINESS-OVERVIEW.md'
        overview.write_text(
            'CrewBeacon is a B2B SaaS product for small home-service companies. '
            'CrewBeacon helps office teams prioritize inbound leads. '
            'The current objective is to increase qualified demo bookings from existing website traffic.\n')
        brand_notes=TMP/'BRAND-NOTES.md'
        brand_notes.write_text(
            'CrewBeacon brand guidance. Use plain English. Sound competent, practical, calm, and useful. '
            'Prefer concrete explanations over broad hype. '
            'Primary audience is owners, operators, office managers, and dispatch leaders at small home-service companies. '
            'Do not portray customers as incompetent or careless.\n')
        facts={
            'business_models':['B2B SaaS'],
            'markets':['small home-service companies'],
            'services':['helps office teams prioritize inbound leads'],
            'objectives':['increase qualified demo bookings from existing website traffic']
        }
        facts_path=TMP/'facts.json';facts_path.write_text(json.dumps(facts,indent=2)+'\n')
        brand={
            'name':'CrewBeacon',
            'voice':{'tone':['plain English','competent','practical','calm','useful']},
            'content_style':{'guidance':'Prefer concrete explanations over broad hype'},
            'prohibited_styles':['portray customers as incompetent or careless'],
            'brand_rules':['Primary audience is owners, operators, office managers, and dispatch leaders at small home-service companies']
        }
        brand_path=TMP/'brand-profile.json';brand_path.write_text(json.dumps(brand,indent=2)+'\n')

        run(S/'init_business.py',BID,'--name','CrewBeacon')
        cp=run(S/'bootstrap_explicit_context.py',BID,'--facts-file',facts_path,
               '--source-file',overview,'--source-file',brand_notes,
               '--brand-profile-file',brand_path)
        payload=json.loads(cp.stdout)
        req(payload.get('brand_profile_files_used')==[brand_path.relative_to(ROOT).as_posix()],f'brand profile file not reported: {payload}')

        bp=ROOT/'instances'/BID/'context/brand'/f'brd_{BID}.json'
        req(bp.exists(),'first-class Brand object missing after explicit Brand onboarding')
        b=json.loads(bp.read_text());bos=(b.get('extensions') or {}).get('businessos',{})
        req(b.get('voice',{}).get('tone')==['plain English','competent','practical','calm','useful'],'Brand voice lost')
        req(b.get('content_style',{}).get('guidance')=='Prefer concrete explanations over broad hype','Brand content style lost')
        req(b.get('prohibited_styles')==['portray customers as incompetent or careless'],'Brand prohibited style lost')
        req(bos.get('authority')=='explicit_user' and bos.get('explicit_brand_profile') is True,'Brand explicit-source provenance incorrect')
        req(bool(bos.get('source_ref')),'Brand must retain its explicit source reference')

        # Brand guidance belongs in Brand, not as a fake generic claim-constraint substitute.
        claims=list((ROOT/'instances'/BID/'context/claims').glob('*.json'))
        req(not claims,f'brand-only guidance unexpectedly flattened into BusinessClaim objects: {claims}')

        # Downstream AURA context retrieval should find Brand directly from durable
        # organization memory. No Run is required merely to retrieve relevant context.
        plan=build_plan(BID,'marketing.assets.landing-page')
        brand_rel=bp.relative_to(ROOT).as_posix()
        req(f'brd_{BID}' in plan.get('object_refs',[]),f'downstream context did not resolve Brand object: {plan.get("object_refs")}')
        req(brand_rel in plan.get('files',[]),f'downstream context plan omitted Brand file: {plan.get("files")}')
        req(not (ROOT/'runtime'/'runs'/BID).exists(),'Brand retrieval should not create or require Run state')

        errors,warnings,counts=validate_business(BID,True)
        req(not errors,f'Brand-onboarded business must validate: {errors}')
        req(counts.get('Brand')==1,'expected exactly one canonical Brand')

        # AURA does not use word-overlap heuristics to decide whether a model's Brand
        # interpretation is semantically equivalent to its source. It *can* prove that
        # explicit-user Brand state points to a real explicit-user source. Protect that.
        original=bp.read_text();broken=json.loads(original)
        broken['extensions']['businessos']['source_ref']='src_missing_brand_source'
        bp.write_text(json.dumps(broken,indent=2)+'\n')
        errors,_,_=validate_business(BID,True)
        req(any('requires an existing SourceRecord source_ref' in e for e in errors),f'missing Brand source provenance should fail: {errors}')
        bp.write_text(original)

        print('first-class Brand onboarding regressions passed with provenance-owned, model-semantic boundary')
    finally:
        clean(BID)
        if TMP.exists(): shutil.rmtree(TMP)

if __name__=='__main__': main()
