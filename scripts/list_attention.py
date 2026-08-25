#!/usr/bin/env python3
from _common import *
import argparse,json
SEV={'informational':0,'low':1,'medium':2,'high':3,'critical':4}

def list_items(bid,statuses=None,min_severity='informational'):
    statuses=set(statuses or ['open','acknowledged']); out=[]
    for obj,p in iter_instance_objects(bid):
        if obj.get('object_type')!='AttentionItem' or obj.get('status') not in statuses: continue
        if SEV.get(obj.get('severity','informational'),0)<SEV[min_severity]: continue
        out.append((obj,p))
    out.sort(key=lambda x:(-SEV.get(x[0].get('severity','informational'),0),x[0].get('next_review_at') or '9999',x[0].get('first_seen') or ''))
    return out

def main():
    ap=argparse.ArgumentParser(description='List current BusinessOS attention without assuming a notification channel.')
    ap.add_argument('business_id'); ap.add_argument('--status',action='append',choices=['open','acknowledged','resolved','superseded','archived']); ap.add_argument('--min-severity',choices=SEV,default='informational'); ap.add_argument('--json',action='store_true'); ap.add_argument('--count',action='store_true'); a=ap.parse_args()
    if not (ROOT/'instances'/a.business_id).exists(): raise SystemExit(f'Unknown business: {a.business_id}')
    rows=list_items(a.business_id,a.status,a.min_severity)
    if a.count: print(len(rows)); return
    compact=[{'id':o['id'],'severity':o['severity'],'status':o['status'],'attention_type':o['attention_type'],'title':o['title'],'reason':o['reason'],'recommended_action':o.get('recommended_action'),'occurrence_count':o['occurrence_count'],'first_seen':o['first_seen'],'last_seen':o['last_seen'],'next_review_at':o.get('next_review_at'),'path':str(p.relative_to(ROOT))} for o,p in rows]
    if a.json: print(json.dumps({'business_id':a.business_id,'count':len(compact),'items':compact},indent=2)); return
    if not compact: print('No matching attention items.'); return
    for x in compact: print(f"[{x['severity'].upper()}] {x['id']} {x['title']} (status={x['status']}, seen={x['occurrence_count']}x)\n  {x['reason']}" + (f"\n  next: {x['recommended_action']}" if x.get('recommended_action') else ''))
if __name__=='__main__': main()
