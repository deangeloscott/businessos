#!/usr/bin/env python3
"""RC16 regressions for first-class Brand onboarding and downstream Brand resolution."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'
sys.path.insert(0,str(S))
from context_plan import build_plan
from validate_business import validate_business

BID='brand-onboarding-test'
BAD='brand-onboarding-ungrounded'
TMP=ROOT/'runtime'/'brand-onboarding-test'

def req(cond,msg):
    if not cond: raise AssertionError(msg)

def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def clean(bid):
    for p in [ROOT/'instances'/bid, ROOT/'runtime'/'runs'/bid]:
        if p.exists(): shutil.rmtree(p)

def main():
    clean(BID);clean(BAD)
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
               '--brand-profile-file',brand_path,'--initialization-only')
        payload=json.loads(cp.stdout)
        req(payload.get('brand_profile_files_used')==[str(brand_path.relative_to(ROOT))],f'brand profile file not reported: {payload}')

        bp=ROOT/'instances'/BID/'context/brand'/f'brd_{BID}.json'
        req(bp.exists(),'first-class Brand object missing after explicit Brand onboarding')
        b=json.loads(bp.read_text());bos=(b.get('extensions') or {}).get('businessos',{})
        req(b.get('voice',{}).get('tone')==['plain English','competent','practical','calm','useful'],'Brand voice lost')
        req(b.get('content_style',{}).get('guidance')=='Prefer concrete explanations over broad hype','Brand content style lost')
        req(b.get('prohibited_styles')==['portray customers as incompetent or careless'],'Brand prohibited style lost')
        req(bos.get('authority')=='explicit_user' and bos.get('explicit_brand_profile') is True,'Brand authority/provenance incorrect')

        # Brand guidance belongs in Brand, not as a fake generic claim-constraint substitute.
        claims=list((ROOT/'instances'/BID/'context/claims').glob('*.json'))
        req(not claims,f'brand-only guidance unexpectedly flattened into BusinessClaim objects: {claims}')

        rid=run(S/'create_run.py',BID,'marketing.assets.landing-page','Draft a local homepage').stdout.strip().splitlines()[-1]
        plan=build_plan(BID,'marketing.assets.landing-page',run_id=rid)
        brand_rel=str(bp.relative_to(ROOT))
        req(f'brd_{BID}' in plan.get('object_refs',[]),f'downstream Run did not resolve Brand object: {plan.get("object_refs")}')
        req(brand_rel in plan.get('files',[]),f'downstream context plan omitted Brand file: {plan.get("files")}')

        errors,warnings,counts=validate_business(BID,True)
        req(not errors,f'Brand-onboarded business must validate: {errors}')
        req(counts.get('Brand')==1,'expected exactly one canonical Brand')

        # Ungrounded Brand expansion must still fail even through the dedicated Brand manifest path.
        bad_brand=dict(brand)
        bad_brand['voice']={'tone':['aggressive luxury']}
        bad_path=TMP/'brand-profile-ungrounded.json';bad_path.write_text(json.dumps(bad_brand,indent=2)+'\n')
        run(S/'init_business.py',BAD,'--name','CrewBeacon')
        bad=run(S/'bootstrap_explicit_context.py',BAD,'--facts-file',facts_path,
                '--source-file',overview,'--source-file',brand_notes,
                '--brand-profile-file',bad_path,'--initialization-only',check=False)
        req(bad.returncode!=0,'ungrounded Brand expansion should be rejected')
        req('Unsupported brand' in (bad.stdout+bad.stderr) or 'not grounded' in (bad.stdout+bad.stderr),f'unexpected ungrounded Brand failure: {bad.stdout} {bad.stderr}')
        req(not (ROOT/'instances'/BAD/'context/brand'/f'brd_{BAD}.json').exists(),'failed Brand bootstrap must not persist Brand state')

        print('first-class Brand onboarding regressions passed')
    finally:
        clean(BID);clean(BAD)
        if TMP.exists(): shutil.rmtree(TMP)

if __name__=='__main__': main()
