#!/usr/bin/env python3
"""RC17 regression: durable preferences must not become authorization/approval state."""
from pathlib import Path
import json, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'; sys.path.insert(0,str(S))
from init_business import init_business
from upsert_preference_profile import upsert
from resolve_preferences import resolve_effective_preferences
from validate_business import validate_business

BID='preference-authorization-separation'; BASE=ROOT/'instances'/BID; RUNS=ROOT/'runtime/runs'/BID; TMP=ROOT/'runtime'/BID

def req(c,m):
    if not c: raise AssertionError(m)

def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def expect_reject(fn,contains='authorization/approval'):
    try:
        fn(); raise AssertionError('authorization semantics were accepted as PreferenceProfile state')
    except ValueError as e:
        req(contains.lower() in str(e).lower(),f'unexpected rejection message: {e}')

def main():
    for p in [BASE,RUNS,TMP]:
        if p.exists(): shutil.rmtree(p)
    try:
        init_business(BID,'Preference Authorization Separation')
        TMP.mkdir(parents=True,exist_ok=True)

        # Valid reusable preference: style/work-method only.
        upsert(BID,'Jordan communication preferences','operator','jordan-founder',{
            'communication':{'style':'concise and practical'},
            'output':{'visual_or_structured_when_helpful':True}
        },'prf_authsep_jordan')

        # The exact class of bug observed in the live resume test must fail closed.
        expect_reject(lambda: upsert(BID,'Bad approval preferences','operator','jordan-founder',{
            'communication':{'style':'concise'},
            'approval_boundaries':{'external_production_actions':'strict approval required'}
        },'prf_authsep_bad_key'))
        expect_reject(lambda: upsert(BID,'Bad textual boundary','operator','jordan-founder',{
            'constraints':['Do not publish or deploy without explicit approval.']
        },'prf_authsep_bad_text'))
        expect_reject(lambda: upsert(BID,'Bad contact boundary','operator','jordan-founder',{
            'workflow':{'note':'Must ask for permission before contacting customers.'}
        },'prf_authsep_bad_contact'))

        # A current task can still contain a mandatory authorization boundary; it is not a preference.
        cp=run(S/'create_run.py',BID,'content.production.article',
               'Create a local article draft. Do not publish or contact customers without explicit approval.',
               '--operator-ref','jordan-founder')
        rid=cp.stdout.strip().splitlines()[-1]
        rp=ROOT/f'runtime/runs/{BID}/{rid}/run.json'; run_obj=json.loads(rp.read_text())
        req('Do not publish' in run_obj['task'],'current task authorization boundary was not preserved in Run task')
        snap=json.loads((ROOT/run_obj['preference_snapshot_ref']).read_text())
        prefs=snap['effective_preferences']
        req(prefs['communication']['style']=='concise and practical','valid operator preference missing from Run')
        flat=json.dumps(prefs).lower()
        req('publish' not in flat and 'approval' not in flat and 'permission' not in flat,'task authorization leaked into preference snapshot')

        # Task-preferences are optional-choice overrides too, not a permission channel.
        tp=TMP/'bad-task-preferences.json'; tp.write_text(json.dumps({'constraints':['Do not publish without approval']})+'\n')
        cp=run(S/'create_run.py',BID,'content.production.article','Create another local article draft',
               '--operator-ref','jordan-founder','--task-preferences',tp,check=False)
        req(cp.returncode!=0,'authorization semantics accepted through --task-preferences')
        req('authorization/approval' in (cp.stderr+cp.stdout).lower(),'task-preference rejection should explain boundary separation')

        # Direct/manual schema-valid PreferenceProfile writes must also be caught by active-business validation.
        bad={
          'id':'prf_authsep_manual_bad','object_type':'PreferenceProfile','schema_version':'1.8.4','business_id':BID,
          'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],
          'name':'Manual bad preference','scope':'operator','subject_ref':'jordan-founder','status':'active','priority':0,
          'source_kind':'explicit_user','source_refs':[],'applies_to':{},
          'preferences':{'workflow':{'external_actions':'No customer contact without approval'}},'notes':None,'extensions':{}
        }
        bp=BASE/'context/preferences/prf_authsep_manual_bad.json'; bp.write_text(json.dumps(bad,indent=2)+'\n')
        errors,_,_=validate_business(BID,False)
        req(any('authorization/approval boundary' in e or 'authorization/approval state' in e for e in errors),f'manual invalid preference was not detected: {errors}')
        bp.unlink()

        # With only valid preference state, business validates and later sessions resolve style without stale authority.
        errors,warnings,counts=validate_business(BID,False)
        req(not errors,f'valid preference-only business should validate: {errors}')
        resolved=resolve_effective_preferences(BID,operator_ref='jordan-founder',system='content-synthesis',contract='content.production.article')
        req(resolved['effective_preferences']['communication']['style']=='concise and practical','later session lost valid durable preference')
        req('approval' not in json.dumps(resolved['effective_preferences']).lower(),'later session inherited stale approval through preference')
        req(counts.get('PreferenceProfile')==1,f'expected one valid PreferenceProfile, got {counts}')

        print('preference/authorization separation regressions passed')
    finally:
        for p in [BASE,RUNS,TMP]:
            if p.exists(): shutil.rmtree(p)

if __name__=='__main__': main()
