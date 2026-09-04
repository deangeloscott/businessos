#!/usr/bin/env python3
"""Archive explicitly selected resolved/superseded organization state.

This helper performs a mechanical retention action after the active model/user has already
made the semantic decision that an eligible object should leave the normal active view.
It does not infer usefulness from age, schedule housekeeping, or decide what knowledge is
safe to forget.
"""
from _common import *
from canonical_store import validate_canonical
import argparse,json,os

ELIGIBLE_STATUS={
    'AttentionItem':'resolved',
    'PlatformChange':'superseded',
}


def _archive_one(business_id,object_ref,reason,archived_at):
    index=object_index(business_id);item=index.get(object_ref)
    if not item:raise ValueError(f'Unknown active organization object: {object_ref}')
    obj,path=item;object_type=obj.get('object_type');required_status=ELIGIBLE_STATUS.get(object_type)
    if not required_status:
        raise ValueError(f'{object_type or "Unknown"} is not eligible for this explicit history archive helper')
    if obj.get('status')!=required_status:
        raise ValueError(f'{object_ref} may be archived only after status={required_status}; current status={obj.get("status")!r}')

    data=json.loads(json.dumps(obj));data['status']='archived';data['updated_at']=archived_at
    ext=data.get('extensions') if isinstance(data.get('extensions'),dict) else {}
    ext=dict(ext);ext['archived_at']=archived_at;ext['archive_reason']=reason;data['extensions']=ext
    validate_canonical(object_type,data)

    history=instance_dir(business_id)/'history'/object_type;history.mkdir(parents=True,exist_ok=True);out=history/path.name
    if out.exists():raise FileExistsError(f'Refusing to overwrite existing historical object: {storage_ref(out)}')
    tmp=out.with_suffix(out.suffix+'.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');os.replace(tmp,out);path.unlink()
    return data,path,out


def archive_objects(business_id,object_refs,reason,archived_at=None):
    if not (instance_dir(business_id)).exists():raise ValueError(f'Unknown business: {business_id}')
    refs=list(dict.fromkeys(str(ref).strip() for ref in object_refs or [] if str(ref).strip()))
    if not refs:raise ValueError('At least one explicit organization object reference is required')
    reason=str(reason or '').strip()
    if not reason:raise ValueError('An explicit archive reason is required')
    archived_at=archived_at or now();moved=[]
    for ref in refs:
        data,src,dst=_archive_one(business_id,ref,reason,archived_at)
        moved.append({'object_ref':data['id'],'object_type':data['object_type'],'from':storage_ref(src),'to':storage_ref(dst)})
    return moved


def main():
    parser=argparse.ArgumentParser(description='Move explicitly selected resolved/superseded organization state out of the active view. This helper never decides archival from object age.')
    parser.add_argument('business_id');parser.add_argument('object_ref',nargs='+');parser.add_argument('--reason',required=True);parser.add_argument('--at',dest='archived_at')
    args=parser.parse_args()
    try:moved=archive_objects(args.business_id,args.object_ref,args.reason,args.archived_at)
    except (ValueError,FileExistsError,OSError,json.JSONDecodeError) as exc:raise SystemExit(str(exc))
    print(json.dumps({'business_id':args.business_id,'archived_count':len(moved),'moved':moved,'selection_authority':False,'rule':'Objects are archived only because the caller explicitly selected already-resolved/superseded organization state; AURA does not infer retention value from age.'},indent=2))


if __name__=='__main__':main()
