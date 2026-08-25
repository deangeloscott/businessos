#!/usr/bin/env python3
from _common import *
import argparse,json

def main():
    ap=argparse.ArgumentParser(description='List current verified external platform/topic state.')
    ap.add_argument('business_id');ap.add_argument('--platform');ap.add_argument('--all-history',action='store_true');ap.add_argument('--json',action='store_true');a=ap.parse_args()
    rows=[]
    for o,p in iter_instance_objects(a.business_id):
        if o.get('object_type')!='PlatformChange':continue
        if not a.all_history and o.get('status')!='current':continue
        if a.platform and o.get('platform','').lower()!=a.platform.lower():continue
        rows.append((o,p))
    rows.sort(key=lambda x:(x[0].get('platform','').lower(),x[0].get('topic','').lower(),x[0].get('last_verified_at','')))
    data=[{'id':o['id'],'platform':o['platform'],'topic':o['topic'],'semantic_key':o['semantic_key'],'status':o['status'],'state_summary':o['state_summary'],'authority':o['authority'],'materiality':o['materiality'],'last_verified_at':o['last_verified_at'],'verification_count':o['verification_count'],'supersedes':o.get('supersedes'),'superseded_by':o.get('superseded_by'),'path':str(p.relative_to(ROOT))} for o,p in rows]
    if a.json:print(json.dumps({'business_id':a.business_id,'count':len(data),'items':data},indent=2));return
    if not data:print('No matching platform state.');return
    for x in data:print(f"{x['platform']} / {x['topic']}: {x['state_summary']} [{x['status']}, verified {x['verification_count']}x, last {x['last_verified_at']}]")
if __name__=='__main__':main()
