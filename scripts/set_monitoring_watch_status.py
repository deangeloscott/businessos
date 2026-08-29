#!/usr/bin/env python3
"""Set semantic monitoring watch status without deleting accumulated intelligence."""
from _common import *
from jsonschema import Draft202012Validator
import argparse,json,os

STATUSES={'seed','candidate','active','paused','deprioritized','blocked','unavailable'}


def _schema():return json.loads((ROOT/'core/schemas/intelligence/source-profile.schema.json').read_text())


def _profiles(business_id):
    root=instance_dir(business_id)/'intelligence'/'source-profiles'
    out=[]
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
    validator=Draft202012Validator(_schema());updated=[];ts=now()
    for obj,path in selected:
        before=obj.get('watch_status');obj['watch_status']=status;obj['updated_at']=ts
        errors=sorted(validator.iter_errors(obj),key=lambda e:list(e.path))
        if errors:raise ValueError('SourceProfile invalid: '+'; '.join(f'{list(e.path)} {e.message}' for e in errors))
        tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n');os.replace(tmp,path)
        updated.append({'id':obj['id'],'before':before,'after':status,'ref':storage_ref(path)})
    return updated


def main():
    p=argparse.ArgumentParser(description='Pause/resume or otherwise change semantic SourceProfile watch state while preserving accumulated intelligence.')
    p.add_argument('business_id');p.add_argument('status',choices=sorted(STATUSES));p.add_argument('--subject-key');p.add_argument('--source-profile-id')
    a=p.parse_args()
    try:rows=set_status(a.business_id,a.status,a.subject_key,a.source_profile_id)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'business_id':a.business_id,'updated':rows,'rule':'Semantic watch state changed without deleting evidence/history. If an actual scheduler binding exists, the host scheduler must also be changed and its receipt/status updated separately.'},indent=2))

if __name__=='__main__':main()
