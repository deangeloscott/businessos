#!/usr/bin/env python3
"""Set semantic monitoring watch status without deleting accumulated intelligence."""
from _common import *
from jsonschema import Draft202012Validator
import argparse,json,os

STATUSES={'seed','candidate','active','paused','deprioritized','blocked','unavailable'}


def _schema():return json.loads((ROOT/'core/schemas/intelligence/source-profile.schema.json').read_text())

def _profiles(business_id):
    root=instance_dir(business_id)/'intelligence'/'source-profiles';out=[]
    if not root.exists():return out
    for path in sorted(root.glob('*.json')):
        try:obj=json.loads(path.read_text())
        except Exception:continue
        if obj.get('object_type')=='SourceProfile' and obj.get('business_id')==business_id:out.append((obj,path))
    return out


def set_status(business_id,status,subject_key=None,source_profile_id=None):
    if not instance_dir(business_id).exists():raise ValueError(f'Unknown business: {business_id}')
    if status not in STATUSES:raise ValueError(f'Unknown watch status: {status}')
    if bool(subject_key)==bool(source_profile_id):raise ValueError('Choose exactly one of --subject-key or --source-profile-id')
    selected=[]
    for obj,path in _profiles(business_id):
        if subject_key and obj.get('subject_key')==subject_key:selected.append((obj,path))
        if source_profile_id and obj.get('id')==source_profile_id:selected.append((obj,path))
    if not selected:raise ValueError('No matching SourceProfile found')
    validator=Draft202012Validator(_schema());updated=[];timestamp=now()
    for obj,path in selected:
        before=obj.get('watch_status');obj['watch_status']=status;obj['updated_at']=timestamp
        errors=sorted(validator.iter_errors(obj),key=lambda error:list(error.path))
        if errors:raise ValueError('SourceProfile invalid: '+'; '.join(f'{list(error.path)} {error.message}' for error in errors))
        temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n');os.replace(temporary,path)
        updated.append({'id':obj['id'],'before':before,'after':status,'ref':storage_ref(path)})
    return updated


def main():
    parser=argparse.ArgumentParser(description='Pause/resume or otherwise change organization-owned monitoring intent while preserving accumulated intelligence.')
    parser.add_argument('business_id');parser.add_argument('status',choices=sorted(STATUSES));parser.add_argument('--subject-key');parser.add_argument('--source-profile-id');args=parser.parse_args()
    try:rows=set_status(args.business_id,args.status,args.subject_key,args.source_profile_id)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps({'business_id':args.business_id,'updated':rows,'rule':'Only organization-owned monitoring intent changed. AURA does not know whether an external scheduler exists and does not mutate scheduler/runtime state.'},indent=2))

if __name__=='__main__':main()
