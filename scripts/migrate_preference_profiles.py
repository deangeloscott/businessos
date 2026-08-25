#!/usr/bin/env python3
"""Migrate legacy PreferenceProfiles that contain authorization semantics.

RC18 migration is intentionally conservative: remove only PreferenceProfile
values rejected by the current preference semantic guard, preserve legitimate
preferences, and never synthesize Approval or other authority from historical
restrictions.
"""
from _common import *
from jsonschema import Draft202012Validator
from preference_semantics import sanitize_legacy_preferences, preference_semantic_errors
import argparse, copy, hashlib, json, os

MIGRATION_ID='rc18-preference-authorization-separation-v1'


def _json_hash(value):
    raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def _schema():
    return json.loads((ROOT/'core/schemas/context/preference-profile.schema.json').read_text())


def _validate_profile(obj):
    errs=sorted(Draft202012Validator(_schema()).iter_errors(obj),key=lambda e:list(e.path))
    if errs:
        raise ValueError('; '.join((('/'.join(map(str,e.path)) or '<root>')+': '+e.message) for e in errs[:10]))
    sem=preference_semantic_errors(obj.get('preferences') or {})
    if sem:
        raise ValueError('; '.join(sem[:10]))


def _profile_files(business_id):
    base=ROOT/'instances'/business_id
    if not base.exists():
        raise ValueError(f'Unknown business: {business_id}')
    out=[]
    for p in sorted(base.rglob('*.json')):
        try: data=json.loads(p.read_text())
        except Exception: continue
        if isinstance(data,dict) and data.get('object_type')=='PreferenceProfile' and data.get('business_id')==business_id:
            out.append(p)
    return out


def _atomic_write(path,obj):
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    os.replace(tmp,path)


def migrate_profile(path,apply=False):
    obj=json.loads(path.read_text())
    prefs=obj.get('preferences') or {}
    cleaned,removals=sanitize_legacy_preferences(prefs)
    if not removals:
        return {'path':str(path.relative_to(ROOT)),'changed':False,'removed':[]}

    migrated=copy.deepcopy(obj)
    migrated['preferences']=cleaned
    before_hash=_json_hash(prefs); after_hash=_json_hash(cleaned)
    ext=copy.deepcopy(migrated.get('extensions') or {})
    history=list(ext.get('preference_migrations') or [])
    if not any(x.get('id')==MIGRATION_ID for x in history if isinstance(x,dict)):
        history.append({
            'id':MIGRATION_ID,
            'applied_at':now(),
            'removed':copy.deepcopy(removals),
            'before_preferences_sha256':before_hash,
            'after_preferences_sha256':after_hash,
            'authority_migrated':False,
            'note':'Legacy authorization/approval semantics were removed from PreferenceProfile only; no Approval or standing authority was inferred.'
        })
    ext['preference_migrations']=history
    migrated['extensions']=ext
    migrated['updated_at']=now()
    _validate_profile(migrated)
    if apply:
        _atomic_write(path,migrated)
    return {
        'path':str(path.relative_to(ROOT)),
        'changed':True,
        'applied':bool(apply),
        'removed':removals,
        'before_preferences_sha256':before_hash,
        'after_preferences_sha256':after_hash,
    }


def migrate_business(business_id,apply=False):
    reports=[migrate_profile(p,apply=apply) for p in _profile_files(business_id)]
    return {
        'business_id':business_id,
        'apply':bool(apply),
        'profiles_scanned':len(reports),
        'profiles_changed':sum(1 for r in reports if r.get('changed')),
        'removed_values':sum(len(r.get('removed') or []) for r in reports),
        'profiles':reports,
    }


def main():
    ap=argparse.ArgumentParser(description='Safely remove legacy authorization/approval semantics from PreferenceProfile without creating authority elsewhere.')
    ap.add_argument('business_id',nargs='?')
    ap.add_argument('--all',action='store_true',help='scan every initialized business under instances/')
    ap.add_argument('--apply',action='store_true',help='write the migration; without this flag the command is a dry run')
    ap.add_argument('--json',action='store_true')
    a=ap.parse_args()
    if bool(a.business_id)==bool(a.all):
        raise SystemExit('Specify exactly one business_id or --all')
    bids=[a.business_id] if a.business_id else sorted(p.name for p in (ROOT/'instances').iterdir() if p.is_dir() and p.name!='_template' and (p/'instance.json').exists())
    results=[]
    try:
        for bid in bids: results.append(migrate_business(bid,apply=a.apply))
    except (ValueError,json.JSONDecodeError) as e:
        raise SystemExit(str(e))
    if a.json:
        print(json.dumps(results[0] if len(results)==1 else results,indent=2))
        return
    for r in results:
        mode='APPLY' if a.apply else 'DRY-RUN'
        print(f"{mode} business={r['business_id']} profiles_scanned={r['profiles_scanned']} profiles_changed={r['profiles_changed']} removed_values={r['removed_values']}")
        for p in r['profiles']:
            if not p.get('changed'): continue
            print('MIGRATE',p['path'])
            for item in p.get('removed') or []:
                print(f"  REMOVE {item['path']} ({item['reason']}, sha256={item['value_sha256'][:12]}...)")
    if not a.apply and any(r['profiles_changed'] for r in results):
        print('No files changed. Re-run with --apply after reviewing the dry-run output.')

if __name__=='__main__': main()
