#!/usr/bin/env python3
"""Regressions for multi-source onboarding, explicit Brand grounding, and pre-Run preference persistence."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'; sys.path.insert(0,str(S))
from validate_business import validate_business

BID='onboarding-context-hardening'; BASE=ROOT/'instances'/BID; RUNS=ROOT/'runtime'/'runs'/BID; TMP=ROOT/'runtime'/BID

def req(c,m):
    if not c: raise AssertionError(m)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def main():
    for p in [BASE,RUNS,TMP]:
        if p.exists(): shutil.rmtree(p)
    try:
        run(S/'init_business.py',BID,'--name','CrewBeacon')
        TMP.mkdir(parents=True,exist_ok=True)
        overview=TMP/'BUSINESS-OVERVIEW.md'
        overview.write_text(
            'CrewBeacon is a B2B SaaS product for small home-service companies. '
            'CrewBeacon helps office teams prioritize inbound leads. '
            'The current objective is to increase qualified demo bookings from existing website traffic. '
            'CrewBeacon works alongside the existing CRM and is not a replacement CRM.\n')
        brand=TMP/'BRAND-NOTES.md'
        brand.write_text(
            'CrewBeacon brand rules: use plain English. Sound calm and practical. '
            'Prefer concrete explanations over broad hype. Avoid unsupported superlatives.\n')
        facts={
            'business_models':['B2B SaaS'],
            'markets':['small home-service companies'],
            'services':['helps office teams prioritize inbound leads'],
            'objectives':['increase qualified demo bookings from existing website traffic'],
            'claim_constraints':['CrewBeacon works alongside the existing CRM and is not a replacement CRM.'],
            'brand':{
                'name':'CrewBeacon',
                'voice':{'tone':['plain English','calm','practical']},
                'brand_rules':['Prefer concrete explanations over broad hype'],
                'prohibited_styles':['unsupported superlatives']
            }
        }
        facts_path=TMP/'facts.json'; facts_path.write_text(json.dumps(facts,indent=2)+'\n')
        pref={
            'name':"Jordan's communication preferences",
            'scope':'operator','subject_ref':'jordan-founder','source_kind':'explicit_user',
            'applies_to':{'workflows':['core.diagnosis.business-problem']},
            'preferences':{'communication':{'concise':True,'practical':True},'output':{'visual_or_structured_when_helpful':True}},
            'notes':'Explicit reusable operator preference supplied during onboarding.'
        }
        pref_path=TMP/'prefs.json'; pref_path.write_text(json.dumps(pref,indent=2)+'\n')
        statement='I prefer concise practical communication and visual or structured outputs when they help.'
        cp=run(S/'bootstrap_explicit_context.py',BID,'--facts-file',facts_path,
               '--source-file',overview,'--source-file',brand,'--source-text',statement,
               '--preference-profile-file',pref_path)
        payload=json.loads(cp.stdout)
        req(len(payload.get('preference_profiles_written') or [])==1,'onboarding must persist reusable preference before returning')
        req(payload['preference_profiles_written'][0]['subject_ref']=='jordan-founder','operator preference subject lost')

        sources=[]
        for p in sorted((BASE/'intelligence/sources').glob('*.json')):
            sources.append(json.loads(p.read_text()))
        bundle=next((x for x in sources if x.get('source_type')=='user_supplied_source_bundle'),None)
        req(bundle is not None,f'multi-source bootstrap should persist a source bundle, got {[x.get("source_type") for x in sources]}')
        members=(bundle.get('extensions') or {}).get('source_members') or []
        req(len(members)==3,f'expected 3 original source members, got {members}')
        byref={m['reference']:m for m in members}
        for fp in [overview,brand]:
            rel=fp.relative_to(ROOT).as_posix()
            req(rel in byref,f'original source ref not preserved: {rel}')
            req(byref[rel]['content_hash']==hashlib.sha256(fp.read_bytes()).hexdigest(),f'original source hash mismatch: {rel}')

        bp=BASE/'context/brand'/f'brd_{BID}.json'
        req(bp.exists(),'explicit organization Brand was not persisted')
        b=json.loads(bp.read_text());bos=(b.get('extensions') or {}).get('businessos',{})
        req(bos.get('authority')=='explicit_user' and bos.get('explicit_brand_profile') is True,'Brand must be deterministically grounded explicit setup state')

        prfs=list((BASE/'context/preferences').glob('*.json'))
        req(len(prfs)==1,'expected one onboarding PreferenceProfile')
        profile=json.loads(prfs[0].read_text())
        req((profile.get('applies_to') or {}).get('workflows')==['core.diagnosis.business-problem'],'Workflow applicability was not preserved')
        req('contracts' not in (profile.get('applies_to') or {}),'Contract-era preference applicability reappeared')

        # The first downstream Run can immediately snapshot the already-persisted operator preference.
        rid=run(S/'create_run.py',BID,'core.diagnosis.business-problem','Diagnose first useful growth problem','--operator-ref','jordan-founder').stdout.strip()
        snap=ROOT/f'runtime/runs/{BID}/{rid}/artifacts/effective-preferences.json'
        sd=json.loads(snap.read_text())
        req(sd['effective_preferences']['communication']['concise'] is True,'first downstream Run missed onboarding preference')
        req(sd['effective_preferences']['communication']['practical'] is True,'first downstream Run missed onboarding preference')
        req(sd['context']['workflow']=='core.diagnosis.business-problem','preference snapshot did not preserve Workflow applicability context')
        req('contract' not in sd['context'],'Contract-era preference context reappeared')

        errors,warnings,counts=validate_business(BID,True)
        req(not errors,f'active business must validate after multi-source onboarding: {errors}')
        req(counts.get('Brand')==1 and counts.get('PreferenceProfile')==1,'expected Brand + PreferenceProfile canonical state')
        print('onboarding context hardening regressions passed')
    finally:
        for p in [BASE,RUNS,TMP]:
            if p.exists(): shutil.rmtree(p)

if __name__=='__main__':main()
