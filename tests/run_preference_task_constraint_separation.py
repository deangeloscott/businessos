#!/usr/bin/env python3
"""Preferences stay a typed customization surface without AURA interpreting prose."""
from pathlib import Path
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from init_business import init_business
from upsert_preference_profile import upsert
from resolve_preferences import resolve_effective_preferences
from validate_business import validate_business
from preference_semantics import preference_semantic_errors

BID='preference-task-constraint-separation';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime/runs'/BID;TMP=ROOT/'runtime'/BID

def req(c,m):
    if not c:raise AssertionError(m)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def expect_reject(fn):
    try:
        fn();raise AssertionError('permission/authority namespace was accepted as PreferenceProfile state')
    except ValueError as e:
        req('preference' in str(e).lower() or 'permission' in str(e).lower(),f'unexpected rejection message: {e}')

def main():
    for p in [BASE,RUNS,TMP]:
        if p.exists():shutil.rmtree(p)
    try:
        init_business(BID,'Preference Task Constraint Separation');TMP.mkdir(parents=True,exist_ok=True)

        # Valid reusable preference: expression/work-method only.
        upsert(BID,'Jordan communication preferences','operator','jordan-founder',{
            'communication':{'style':'concise and practical'},
            'output':{'visual_or_structured_when_helpful':True}
        },'prf_tasksep_jordan')

        # Clearly permission-shaped namespaces are structurally not PreferenceProfile data.
        expect_reject(lambda:upsert(BID,'Bad action preferences','operator','jordan-founder',{
            'communication':{'style':'concise'},
            'approval_boundaries':{'external_production_actions':'strict approval required'}
        },'prf_tasksep_bad_key'))

        # AURA must not parse arbitrary prose to infer whether it is a temporary task
        # constraint, durable policy/decision, or preference. The capable model/user owns
        # that classification. Only the structural namespace is checked here.
        prose={'workflow':{'note':'Must ask before contacting customers on this task.'}}
        req(not preference_semantic_errors(prose),'preference validator reintroduced natural-language intent classification')

        # A current request can contain a real task constraint; it stays in task context
        # unless the model/user intentionally persists some durable organizational meaning.
        cp=run(S/'create_run.py',BID,'content.production.article',
               'Create a local article draft. Do not publish or contact customers without explicit approval.',
               '--operator-ref','jordan-founder')
        rid=cp.stdout.strip().splitlines()[-1]
        rp=ROOT/f'runtime/runs/{BID}/{rid}/run.json';run_obj=json.loads(rp.read_text())
        req('Do not publish' in run_obj['task'],'current task constraint was not preserved in Run task')
        snap=json.loads((ROOT/run_obj['preference_snapshot_ref']).read_text());prefs=snap['effective_preferences']
        req(prefs['communication']['style']=='concise and practical','valid operator preference missing from Run')
        flat=json.dumps(prefs).lower();req('publish' not in flat and 'approval' not in flat and 'permission' not in flat,'current task text was automatically copied into durable preference state')

        # Direct writes that use a categorically wrong permission namespace remain invalid.
        bad={
          'id':'prf_tasksep_manual_bad','object_type':'PreferenceProfile','schema_version':'1.8.4','business_id':BID,
          'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],
          'name':'Manual bad preference','scope':'operator','subject_ref':'jordan-founder','status':'active','priority':0,
          'source_kind':'explicit_user','source_refs':[],'applies_to':{},
          'preferences':{'approval_boundaries':{'customer_contact':'required'}},'notes':None,'extensions':{}
        }
        bp=BASE/'context/preferences/prf_tasksep_manual_bad.json';bp.write_text(json.dumps(bad,indent=2)+'\n')
        errors,_,_=validate_business(BID,False)
        req(any('permission' in e.lower() or 'preference' in e.lower() for e in errors),f'manual invalid preference namespace was not detected: {errors}')
        bp.unlink()

        # Valid preferences survive without turning a past task restriction into standing state.
        errors,warnings,counts=validate_business(BID,False);req(not errors,f'valid preference-only business should validate: {errors}')
        resolved=resolve_effective_preferences(BID,operator_ref='jordan-founder',system='content-synthesis',contract='content.production.article')
        effective=resolved['effective_preferences'];req(effective['communication']['style']=='concise and practical','later session lost valid durable preference')
        text=json.dumps(effective).lower();req('publish' not in text and 'approval' not in text and 'permission' not in text,'later session inherited a past task constraint')
        req(counts.get('PreferenceProfile')==1,f'expected one valid PreferenceProfile, got {counts}')

        print('preference boundary regressions passed: typed namespace protected without natural-language semantic policing')
    finally:
        for p in [BASE,RUNS,TMP]:
            if p.exists():shutil.rmtree(p)

if __name__=='__main__':main()
