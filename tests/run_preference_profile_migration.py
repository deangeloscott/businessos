#!/usr/bin/env python3
"""RC18 regression: legacy invalid PreferenceProfile state migrates safely and idempotently."""
from pathlib import Path
import hashlib, json, shutil, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'; sys.path.insert(0,str(S))
from init_business import init_business
from migrate_preference_profiles import migrate_business, MIGRATION_ID
from preference_semantics import preference_semantic_errors
from validate_business import validate_business

BID='legacy-preference-migration'; BASE=ROOT/'instances'/BID; RUNS=ROOT/'runtime/runs'/BID; TMP=ROOT/'runtime'/BID


def req(c,m):
    if not c: raise AssertionError(m)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for p in [BASE,RUNS,TMP]:
        if p.exists(): shutil.rmtree(p)
    try:
        init_business(BID,'Legacy Preference Migration')
        prefdir=BASE/'context/preferences'; prefdir.mkdir(parents=True,exist_ok=True)
        profile={
          'id':'prf_legacy_migration_jordan','object_type':'PreferenceProfile','schema_version':'1.8.4','business_id':BID,
          'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],
          'name':'Jordan Preferences','scope':'operator','subject_ref':'jordan-founder','status':'active','priority':0,
          'source_kind':'explicit_user','source_refs':[],'applies_to':{},
          'preferences':{
            'communication_style':'concise_practical',
            'output_style':'visual_and_simple',
            'workflow':{'notes':['evidence first','Do not publish without explicit approval.']},
            'authorization':{
              'require_approval_for':['publish_content','spend_money'],
              'authorized_local':['analyze_supplied_materials','create_local_drafts']
            }
          },
          'notes':None,'extensions':{'existing_extension':{'keep':True}}
        }
        pp=prefdir/(profile['id']+'.json'); pp.write_text(json.dumps(profile,indent=2)+'\n')

        # Sentinel history/state outside PreferenceProfile must remain byte-identical.
        sentinel=BASE/'context'/'migration-sentinel.txt'; sentinel.write_text('existing business history must remain untouched\n')
        instance_hash=sha(BASE/'instance.json'); sentinel_hash=sha(sentinel)
        original_profile_bytes=pp.read_bytes()

        # Dry run is inspectable and never changes state.
        dry=migrate_business(BID,apply=False)
        req(dry['profiles_changed']==1 and dry['removed_values']==2,f'unexpected dry-run report: {dry}')
        req(pp.read_bytes()==original_profile_bytes,'dry-run changed the PreferenceProfile')
        req(sha(BASE/'instance.json')==instance_hash and sha(sentinel)==sentinel_hash,'dry-run changed unrelated business state')

        # Apply strips only invalid semantics and creates no authorization object elsewhere.
        applied=migrate_business(BID,apply=True)
        req(applied['profiles_changed']==1 and applied['removed_values']==2,f'unexpected apply report: {applied}')
        migrated=json.loads(pp.read_text())
        prefs=migrated['preferences']
        req(prefs['communication_style']=='concise_practical','legitimate communication preference changed')
        req(prefs['output_style']=='visual_and_simple','legitimate output preference changed')
        req(prefs['workflow']['notes']==['evidence first'],'valid mixed-list preference was not preserved exactly')
        req('authorization' not in prefs,'legacy authorization subtree survived migration')
        req(not preference_semantic_errors(prefs),f'migrated preferences still invalid: {preference_semantic_errors(prefs)}')
        req(migrated['extensions']['existing_extension']=={'keep':True},'existing extension state was overwritten')
        audits=migrated['extensions'].get('preference_migrations') or []
        req(len(audits)==1 and audits[0]['id']==MIGRATION_ID,'migration audit missing or duplicated')
        req(audits[0].get('authority_migrated') is False,'migration must explicitly avoid inferring authority')
        req({x['path'] for x in audits[0]['removed']}=={'preferences.authorization','preferences.workflow.notes[1]'},f'unexpected removed paths: {audits[0]["removed"]}')
        req(sha(BASE/'instance.json')==instance_hash and sha(sentinel)==sentinel_hash,'migration changed unrelated business history/state')
        req(not (BASE/'operations/approvals').exists() or not any((BASE/'operations/approvals').glob('*.json')),'migration synthesized Approval state')

        errors,warnings,counts=validate_business(BID,False)
        req(not errors,f'migrated business should validate: {errors}')
        req(counts.get('PreferenceProfile')==1,f'expected one PreferenceProfile, got {counts}')

        # Second apply is a no-op, including byte-for-byte profile stability.
        migrated_bytes=pp.read_bytes()
        second=migrate_business(BID,apply=True)
        req(second['profiles_changed']==0 and second['removed_values']==0,f'second migration was not a no-op: {second}')
        req(pp.read_bytes()==migrated_bytes,'idempotent second migration rewrote profile')
        req(sha(BASE/'instance.json')==instance_hash and sha(sentinel)==sentinel_hash,'second migration changed unrelated state')

        print('legacy PreferenceProfile migration regressions passed')
    finally:
        for p in [BASE,RUNS,TMP]:
            if p.exists(): shutil.rmtree(p)

if __name__=='__main__': main()
