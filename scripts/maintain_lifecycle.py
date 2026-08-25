#!/usr/bin/env python3
from _common import *
import argparse,json,datetime,shutil

def parse(s):
    if not s:return None
    try:return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
    except Exception:return None

def age_days(ts,asof):
    d=parse(ts);return (asof-d).total_seconds()/86400 if d else -1

def main():
    ap=argparse.ArgumentParser(description='Archive old terminal attention/platform state. No durable evidence is deleted.')
    ap.add_argument('business_id');ap.add_argument('--attention-days',type=int,default=90);ap.add_argument('--platform-days',type=int,default=180);ap.add_argument('--apply',action='store_true');ap.add_argument('--as-of');a=ap.parse_args()
    base=ROOT/'instances'/a.business_id
    if not base.exists():raise SystemExit(f'Unknown business: {a.business_id}')
    asof=parse(a.as_of) if a.as_of else datetime.datetime.now(datetime.timezone.utc)
    if asof.tzinfo is None:asof=asof.replace(tzinfo=datetime.timezone.utc)
    actions=[]
    for obj,p in iter_instance_objects(a.business_id):
        typ=obj.get('object_type');status=obj.get('status');days=None;histdir=None
        if typ=='AttentionItem' and status in {'resolved','superseded'}:days=a.attention_days;histdir=base/'history'/'attention'/str(asof.year)
        elif typ=='PlatformChange' and status=='superseded':days=a.platform_days;histdir=base/'history'/'platform-changes'/str(asof.year)
        else:continue
        if age_days(obj.get('updated_at'),asof)<days:continue
        target=histdir/p.name
        actions.append({'id':obj['id'],'object_type':typ,'from':str(p.relative_to(ROOT)),'to':str(target.relative_to(ROOT))})
        if a.apply:
            obj['status']='archived';obj['updated_at']=asof.isoformat();bos=obj.setdefault('extensions',{}).setdefault('businessos',{});bos['archived_from_status']=status;bos['archived_at']=asof.isoformat()
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(obj,indent=2)+'\n')
            if p.resolve()!=target.resolve():p.unlink()
    print(json.dumps({'business_id':a.business_id,'apply':a.apply,'eligible_count':len(actions),'actions':actions},indent=2))
if __name__=='__main__':main()
