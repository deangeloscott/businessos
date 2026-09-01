#!/usr/bin/env python3
"""Update the current semantic state of one durable AttentionItem."""
from _common import *
import argparse,json

STATUSES={'open','acknowledged','resolved'}


def find_item(business_id,attention_id):
    for obj,path in iter_instance_objects(business_id):
        if obj.get('object_type')=='AttentionItem' and obj.get('id')==attention_id:return obj,path
    return None,None


def set_status(business_id,attention_id,status,resolution_refs=None,note=None,at=None):
    if status not in STATUSES:raise ValueError(f'Unknown AttentionItem status: {status}')
    obj,path=find_item(business_id,attention_id)
    if not obj:raise ValueError('AttentionItem not found')
    timestamp=at or now();old=obj.get('status');resolution_refs=resolution_refs or []
    if status=='resolved' and not (resolution_refs or note):raise ValueError('resolved requires a resolution reference or note')
    obj['status']=status;obj['updated_at']=timestamp
    if status=='open':
        obj['acknowledged_at']=None;obj['resolved_at']=None;obj['next_review_at']=obj.get('next_review_at')
    elif status=='acknowledged':
        obj['acknowledged_at']=timestamp;obj['resolved_at']=None
    else:
        obj['resolved_at']=timestamp;obj['next_review_at']=None
        obj['resolution_refs']=sorted(set((obj.get('resolution_refs') or [])+resolution_refs))
        if note:
            bos=obj.setdefault('extensions',{}).setdefault('businessos',{})
            bos['resolution_note']=note
    path.write_text(json.dumps(obj,indent=2)+'\n')
    return {'attention_id':obj['id'],'from':old,'to':status,'path':str(path.relative_to(ROOT))}


def main():
    parser=argparse.ArgumentParser(description='Mark one durable AttentionItem open, acknowledged, or resolved. This changes organizational memory, not execution permission.')
    parser.add_argument('business_id');parser.add_argument('attention_id');parser.add_argument('status',choices=sorted(STATUSES));parser.add_argument('--resolution-ref',action='append',default=[]);parser.add_argument('--note');parser.add_argument('--at');args=parser.parse_args()
    try:result=set_status(args.business_id,args.attention_id,args.status,args.resolution_ref,args.note,args.at)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
