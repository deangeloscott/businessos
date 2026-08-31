#!/usr/bin/env python3
"""Durable preferences must not absorb one-task action constraints or permissions."""
from pathlib import Path
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from init_business import init_business
from upsert_preference_profile import upsert
from resolve_preferences import resolve_effective_preferences
from validate_business import validate_business

BID='preference-task-constraint-separation';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime/runs'/BID;TMP=ROOT/'runtime'/BID

def req(c,m):
    if not c:raise AssertionError(m)

def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def expect_reject(fn):
    try:
        fn();raise AssertionError('one-task action constraint was accepted as durable PreferenceProfile state')
    except ValueError as e:
        req('preference' in str(e).lower(),f'unexpected rejection message: {e}')

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

        # One-task external-action constraints are instructions/context, not reusable preferences.
        expect_reject(lambda:upsert(BID,'Bad action preferences','operator','jordan-founder',{
            'communication':{'style':'concise'},
            'approval_boundaries':{'external_production_actions':'strict approval required'}
        },'prf_tasksep_bad_key'))
        expect_reject(lambda:upsert(BID,'Bad textual constraint','operator','jordan-founder',{
            'constraints':['Do not publish or deploy without explicit approval.']
        },'prf_tasksep_bad_text'))
        expect_reject(lambda:upsert(BID,'Bad contact constraint','operator','jordan-founder',{
            'workflow':{'note':'Must ask for permission before contacting customers.'}
        },'prf_tasksep_bad_contact'))

        # A current request can contain a real task constraint; it remains in task context, not PreferenceProfile.
        cp=run(S/'create_run.py',BID,'content.production.article',
               'Create a local article draft. Do not publish or contact customers without explicit approval.',
               '--operator-ref','jordan-founder')
        rid=cp.stdout.strip().splitlines()[-1]
        rp=ROOT/f'runtime/runs/{BID}/{rid}/run.json';run_obj=json.loads(rp.read_text())
        req('Do not publish' in run_obj['task'],'current task constraint was not preserved in Run task')
        snap=json.loads((ROOT/run_obj['preference_snapshot_ref']).read_text());prefs=snap['effective_preferences']
        req(prefs['communication']['style']=='concise and practical','valid operator preference missing from Run')
        flat=json.dumps(prefs).lower();req('publish' not in flat and 'approval' not in flat and 'permission' not in flat,'task constraint leaked into durable preference snapshot')

        # Task-preferences remain optional-choice overrides, not a channel for action constraints.
        tp=TMP/'bad-task-preferences.json';tp.write_text(json.dumps({'constraints':['Do not publish without approval']})+'\n')
        cp=run(S/'create_run.py',BID,'content.production.article','Create another local article draft',
               '--operator-ref','jordan-founder','--task-preferences',tp,check=False)
        req(cp.returncode!=0,'one-task action constraint was accepted through --task-preferences')
        req('preference' in (cp.stderr+cp.stdout).lower(),'task-preference rejection should explain the semantic separation')

        # Direct schema-valid writes must also be caught by active-business semantic validation.
        bad={
          'id':'prf_tasksep_manual_bad','object_type':'PreferenceProfile','schema_version':'1.8.4','business_id':BID,
          'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],
          'name':'Manual bad preference','scope':'operator','subject_ref':'jordan-founder','status':'active','priority':0,
          'source_kind':'explicit_user','source_refs':[],'applies_to':{},
          'preferences':{'workflow':{'external_actions':'No customer contact without approval'}},'notes':None,'extensions':{}
        }
        bp=BASE/'context/preferences/prf_tasksep_manual_bad.json';bp.write_text(json.dumps(bad,indent=2)+'\n')
        errors,_,_=validate_business(BID,False)
        req(any('preference' in e.lower() for e in errors),f'manual invalid preference was not detected: {errors}')
        bp.unlink()

        # Valid preferences survive across sessions without turning a past task restriction into standing state.
        errors,warnings,counts=validate_business(BID,False);req(not errors,f'valid preference-only business should validate: {errors}')
        resolved=resolve_effective_preferences(BID,operator_ref='jordan-founder',system='content-synthesis',contract='content.production.article')
        effective=resolved['effective_preferences'];req(effective['communication']['style']=='concise and practical','later session lost valid durable preference')
        text=json.dumps(effective).lower();req('publish' not in text and 'approval' not in text and 'permission' not in text,'later session inherited a stale one-task action constraint')
        req(counts.get('PreferenceProfile')==1,f'expected one valid PreferenceProfile, got {counts}')

        print('preference/task-constraint separation regressions passed')
    finally:
        for p in [BASE,RUNS,TMP]:
            if p.exists():shutil.rmtree(p)

if __name__=='__main__':main()
