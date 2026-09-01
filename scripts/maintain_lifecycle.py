#!/usr/bin/env python3
"""Archive old terminal semantic state without deleting durable evidence."""
from _common import *
import argparse,json,datetime


def parse(value):
    if not value:return None
    try:return datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    except Exception:return None

def age_days(timestamp,as_of):
    value=parse(timestamp);return (as_of-value).total_seconds()/86400 if value else -1


def main():
    parser=argparse.ArgumentParser(description='Move old resolved AttentionItems and superseded PlatformChanges out of the active view. No durable evidence is deleted.')
    parser.add_argument('business_id');parser.add_argument('--attention-days',type=int,default=90);parser.add_argument('--platform-days',type=int,default=180);parser.add_argument('--apply',action='store_true');parser.add_argument('--as-of');args=parser.parse_args()
    base=ROOT/'instances'/args.business_id
    if not base.exists():raise SystemExit(f'Unknown business: {args.business_id}')
    as_of=parse(args.as_of) if args.as_of else datetime.datetime.now(datetime.timezone.utc)
    if as_of.tzinfo is None:as_of=as_of.replace(tzinfo=datetime.timezone.utc)
    actions=[]
    for obj,path in iter_instance_objects(args.business_id):
        typ=obj.get('object_type');status=obj.get('status')
        if typ=='AttentionItem' and status=='resolved':days=args.attention_days;history_dir=base/'history'/'attention'/str(as_of.year)
        elif typ=='PlatformChange' and status=='superseded':days=args.platform_days;history_dir=base/'history'/'platform-changes'/str(as_of.year)
        else:continue
        if age_days(obj.get('updated_at'),as_of)<days:continue
        target=history_dir/path.name;actions.append({'id':obj['id'],'object_type':typ,'from':str(path.relative_to(ROOT)),'to':str(target.relative_to(ROOT))})
        if args.apply:
            obj['status']='archived';obj['updated_at']=as_of.isoformat();bos=obj.setdefault('extensions',{}).setdefault('businessos',{});bos['archived_from_status']=status;bos['archived_at']=as_of.isoformat()
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(obj,indent=2)+'\n')
            if path.resolve()!=target.resolve():path.unlink()
    print(json.dumps({'business_id':args.business_id,'apply':args.apply,'eligible_count':len(actions),'actions':actions},indent=2))

if __name__=='__main__':main()
