#!/usr/bin/env python3
"""Regressions for scoped preferences, operator attribution, and current-vs-frozen preference context."""
from pathlib import Path
import json, os, shutil, subprocess, sys
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from init_business import init_business
from upsert_preference_profile import upsert
from resolve_preferences import resolve_effective_preferences
from context_plan import build_plan
from validate_business import validate_business

BID='preference-resolution-test'
BASE=ROOT/'instances'/BID

def prefs_file(name,data):
    p=ROOT/'runtime'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n');return p

def assert_eq(actual,expected,label):
    if actual!=expected: raise AssertionError(f'{label}: expected {expected!r}, got {actual!r}')

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    try:
        init_business(BID,'Preference Resolution Test')
        upsert(BID,'Business presentation defaults','business',BID,{
            'presentation':{'slide_density':'balanced','speaker_notes':'brief'},
            'writing':{'tone':'professional'}
        },'prf_pref_business',0,'explicit_organization')
        upsert(BID,'Sales team defaults','team','team_sales',{
            'presentation':{'slide_density':'concise','include_appendix':True}
        },'prf_pref_sales',0,'explicit_organization')
        upsert(BID,'Presenter role defaults','role','role_presenter',{
            'writing':{'tone':'consultative'}
        },'prf_pref_presenter',0,'explicit_organization')
        upsert(BID,'Alice preferences','operator','operator_alice',{
            'presentation':{'speaker_notes':'detailed','diagrams_over_bullets':True}
        },'prf_pref_alice',0,'explicit_user',systems=['content-synthesis'])
        upsert(BID,'Bob preferences','operator','operator_bob',{
            'presentation':{'speaker_notes':'brief','diagrams_over_bullets':False}
        },'prf_pref_bob',0,'explicit_user',systems=['content-synthesis'])
        upsert(BID,'SEO-only preference','operator','operator_alice',{
            'presentation':{'slide_density':'seo-only-should-not-apply'}
        },'prf_pref_alice_seo',10,'explicit_user',systems=['seo-aeo'])

        alice=resolve_effective_preferences(BID,'operator_alice','team_sales','role_presenter','content-synthesis','content.production.presentation')
        ap=alice['effective_preferences']
        assert_eq(ap['presentation']['slide_density'],'concise','team overrides business')
        assert_eq(ap['presentation']['speaker_notes'],'detailed','operator overrides business')
        assert_eq(ap['presentation']['diagrams_over_bullets'],True,'alice operator preference')
        assert_eq(ap['presentation']['include_appendix'],True,'team preference retained')
        assert_eq(ap['writing']['tone'],'consultative','role overrides business')
        if 'prf_pref_alice_seo' in [x['id'] for x in alice['applied_profiles']]: raise AssertionError('nonmatching system preference applied')

        bob=resolve_effective_preferences(BID,'operator_bob','team_sales','role_presenter','content-synthesis','content.production.presentation')
        bp=bob['effective_preferences']
        assert_eq(bp['presentation']['speaker_notes'],'brief','bob preference differs from alice')
        assert_eq(bp['presentation']['diagrams_over_bullets'],False,'bob preference differs from alice')

        task={'presentation':{'slide_density':'ultra_sparse'}}
        task_res=resolve_effective_preferences(BID,'operator_alice','team_sales','role_presenter','content-synthesis','content.production.presentation',task_preferences=task)
        assert_eq(task_res['effective_preferences']['presentation']['slide_density'],'ultra_sparse','task preference highest optional preference precedence')
        if task_res['leaf_sources']['presentation.slide_density']['source_type']!='task_preference': raise AssertionError('task preference provenance missing')

        # create_run may preserve attribution and a frozen preference snapshot when a work
        # receipt is useful. That receipt is optional and does not own normal context retrieval.
        env=dict(os.environ);env['BUSINESSOS_OPERATOR_REF']='operator_alice';env['BUSINESSOS_TEAM_REF']='team_sales';env['BUSINESSOS_ROLE_REF']='role_presenter';env['PYTHONDONTWRITEBYTECODE']='1'
        cp=subprocess.run([sys.executable,str(ROOT/'scripts/create_run.py'),BID,'content.production.presentation','Create a client presentation','--output-type','presentation','--channel','live-meeting'],cwd=ROOT,env=env,text=True,capture_output=True,check=True)
        rid=cp.stdout.strip().splitlines()[-1]
        rp=ROOT/'runtime/runs'/BID/rid/'run.json';run=json.loads(rp.read_text())
        assert_eq(run['operator_ref'],'operator_alice','Run operator attribution')
        assert_eq(run['team_ref'],'team_sales','Run team attribution')
        assert_eq(run['role_ref'],'role_presenter','Run role attribution')
        assert_eq(run['preference_output_type'],'presentation','Run preference output type')
        assert_eq(run['preference_channel'],'live-meeting','Run preference channel')
        snap=ROOT/run['preference_snapshot_ref']
        if not snap.exists(): raise AssertionError('Run preference snapshot missing')
        sd=json.loads(snap.read_text())
        assert_eq(sd['effective_preferences']['presentation']['speaker_notes'],'detailed','Run snapshot preference')

        # Run schema remains valid with optional attribution/snapshot fields.
        schema=json.loads((ROOT/'core/schemas/runtime/run.schema.json').read_text())
        errs=list(Draft202012Validator(schema).iter_errors(run))
        if errs: raise AssertionError('Run schema errors: '+'; '.join(e.message for e in errs))

        # Context planning resolves current organization-owned preferences directly. It
        # does not need a Run id or load a Run snapshot merely to prepare useful context.
        plan=build_plan(
            BID,'content.production.presentation',
            operator_ref='operator_alice',team_ref='team_sales',role_ref='role_presenter',
            output_type='presentation',channel='live-meeting'
        )
        assert_eq(plan['operator_ref'],'operator_alice','context plan operator')
        assert_eq(plan['effective_preferences']['presentation']['speaker_notes'],'detailed','context plan current preference')
        if 'core/policies/preferences-and-adaptation.md' not in plan['files']: raise AssertionError('preference policy missing from context plan')
        if run['preference_snapshot_ref'] in plan['files']: raise AssertionError('context plan should not depend on an optional Run snapshot')

        errors,warnings,counts=validate_business(BID,False)
        if errors: raise AssertionError('business validation errors: '+'; '.join(errors))
        if counts.get('PreferenceProfile')!=6: raise AssertionError(f'expected 6 preference profiles, got {counts}')

        # Equal-scope/equal-priority conflicts must not be resolved by arbitrary file/id order.
        upsert(BID,'Alice conflicting preference','operator','operator_alice',{
            'presentation':{'speaker_notes':'minimal'}
        },'prf_pref_alice_conflict',0,'explicit_user',systems=['content-synthesis'])
        try:
            resolve_effective_preferences(BID,'operator_alice','team_sales','role_presenter','content-synthesis','content.production.presentation')
            raise AssertionError('equal-precedence conflict was silently resolved')
        except ValueError as e:
            if 'Unresolved equal-precedence preference conflict' not in str(e): raise

        # Higher priority inside one scope is intentional and deterministic.
        (BASE/'context/preferences/prf_pref_alice_conflict.json').unlink()
        upsert(BID,'Alice high-priority preference','operator','operator_alice',{
            'presentation':{'speaker_notes':'minimal'}
        },'prf_pref_alice_high',5,'explicit_user',systems=['content-synthesis'])
        hi=resolve_effective_preferences(BID,'operator_alice','team_sales','role_presenter','content-synthesis','content.production.presentation')
        assert_eq(hi['effective_preferences']['presentation']['speaker_notes'],'minimal','same-scope priority override')

        # Current retrieval should see the new durable preference, while the existing
        # optional Run receipt remains a reproducible record of the preference snapshot
        # that applied when that bounded work began.
        current_plan=build_plan(
            BID,'content.production.presentation',
            operator_ref='operator_alice',team_ref='team_sales',role_ref='role_presenter',
            output_type='presentation',channel='live-meeting'
        )
        assert_eq(current_plan['effective_preferences']['presentation']['speaker_notes'],'minimal','current context plan should use current durable preference')
        frozen=json.loads(snap.read_text())
        assert_eq(frozen['effective_preferences']['presentation']['speaker_notes'],'detailed','existing Run preference snapshot is immutable')

        print('scoped preference + multi-operator regressions passed without Run-owned context retrieval')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
        rd=ROOT/'runtime/runs'/BID
        if rd.exists(): shutil.rmtree(rd)
        try:
            if (ROOT/'runtime/runs').exists() and not any((ROOT/'runtime/runs').iterdir()): (ROOT/'runtime/runs').rmdir()
        except OSError: pass

if __name__=='__main__':main()
