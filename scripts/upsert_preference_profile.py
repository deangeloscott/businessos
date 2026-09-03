#!/usr/bin/env python3
from _common import *
from jsonschema import Draft202012Validator
import argparse,json
from preference_semantics import validate_preference_semantics


def _load_preferences(path):
    p=Path(path);p=p if p.is_absolute() else ROOT/p
    if not p.exists(): raise ValueError(f'Preferences file not found: {path}')
    d=json.loads(p.read_text())
    if not isinstance(d,dict): raise ValueError('Preferences file must contain one JSON object')
    validate_preference_semantics(d)
    return d


def _validate(obj):
    schema=json.loads((ROOT/'core/schemas/context/preference-profile.schema.json').read_text())
    errs=sorted(Draft202012Validator(schema).iter_errors(obj),key=lambda e:list(e.path))
    if errs: raise ValueError('; '.join((('/'.join(map(str,e.path)) or '<root>')+': '+e.message) for e in errs[:10]))


def upsert(business_id,name,scope,subject_ref,preferences,profile_id=None,priority=0,source_kind='explicit_user',source_refs=None,systems=None,workflows=None,output_types=None,channels=None,notes=None):
    base=ROOT/'instances'/business_id
    if not base.exists(): raise ValueError('Unknown business')
    if scope=='business' and not subject_ref:subject_ref=business_id
    if not subject_ref: raise ValueError('subject_ref is required outside business scope')
    validate_preference_semantics(preferences)
    if not profile_id:
        raw=f'{business_id}-{scope}-{subject_ref}-{name}'
        sid=slug(raw)[:72].rstrip('-_') or 'preference'
        profile_id='prf_'+sid
    if not re.fullmatch(r'prf_[A-Za-z0-9_-]+',profile_id): raise ValueError('profile_id must match prf_[A-Za-z0-9_-]+')
    d=base/'context/preferences';d.mkdir(parents=True,exist_ok=True);path=d/(profile_id+'.json')
    ts=now();created=ts;lineage=[]
    if path.exists():
        old=json.loads(path.read_text());created=old.get('created_at') or ts;lineage=list(old.get('lineage') or [])
    applies={}
    for key,val in [('systems',systems),('workflows',workflows),('output_types',output_types),('channels',channels)]:
        if val: applies[key]=sorted(set(val))
    obj={
        'id':profile_id,'object_type':'PreferenceProfile','schema_version':os_version(),'business_id':business_id,
        'created_at':created,'updated_at':ts,'lineage':lineage,'name':name,'scope':scope,'subject_ref':subject_ref,
        'status':'active','priority':int(priority),'source_kind':source_kind,'source_refs':sorted(set(source_refs or [])),
        'applies_to':applies,'preferences':preferences,'notes':notes,'extensions':{}
    }
    _validate(obj);path.write_text(json.dumps(obj,indent=2)+'\n');return path,obj


def main():
    p=argparse.ArgumentParser(description='Create/update one business-scoped PreferenceProfile. Preferences customize valid choices but do not authorize actions or constrain model judgment.')
    p.add_argument('business_id');p.add_argument('--name',required=True);p.add_argument('--scope',choices=['business','team','role','operator'],required=True);p.add_argument('--subject-ref')
    p.add_argument('--preferences-file',required=True);p.add_argument('--id');p.add_argument('--priority',type=int,default=0);p.add_argument('--source-kind',choices=['explicit_user','explicit_organization','imported_configuration'],default='explicit_user')
    p.add_argument('--source-ref',action='append',default=[]);p.add_argument('--system',action='append',default=[]);p.add_argument('--workflow',action='append',default=[]);p.add_argument('--output-type',action='append',default=[]);p.add_argument('--channel',action='append',default=[]);p.add_argument('--notes')
    a=p.parse_args()
    try:
        prefs=_load_preferences(a.preferences_file)
        path,obj=upsert(a.business_id,a.name,a.scope,a.subject_ref,prefs,a.id,a.priority,a.source_kind,a.source_ref,a.system,a.workflow,a.output_type,a.channel,a.notes)
    except (ValueError,json.JSONDecodeError) as e: raise SystemExit(str(e))
    print(path.relative_to(ROOT));print(obj['id'])
if __name__=='__main__':main()
