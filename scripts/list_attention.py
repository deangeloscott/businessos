#!/usr/bin/env python3
from _common import *
import argparse,json
SEVERITY={'informational':0,'low':1,'medium':2,'high':3,'critical':4}


def list_items(business_id,statuses=None,min_severity='informational'):
    statuses=set(statuses or ['open','acknowledged']);out=[]
    for obj,path in iter_instance_objects(business_id):
        if obj.get('object_type')!='AttentionItem' or obj.get('status') not in statuses:continue
        if SEVERITY.get(obj.get('severity','informational'),0)<SEVERITY[min_severity]:continue
        out.append((obj,path))
    out.sort(key=lambda x:(-SEVERITY.get(x[0].get('severity','informational'),0),x[0].get('next_review_at') or '9999',x[0].get('first_seen') or ''))
    return out


def main():
    parser=argparse.ArgumentParser(description='List durable organizational attention without assuming a notification channel or task queue.')
    parser.add_argument('business_id');parser.add_argument('--status',action='append',choices=['open','acknowledged','resolved','archived']);parser.add_argument('--min-severity',choices=SEVERITY,default='informational');parser.add_argument('--json',action='store_true');parser.add_argument('--count',action='store_true');args=parser.parse_args()
    if not (ROOT/'instances'/args.business_id).exists():raise SystemExit(f'Unknown business: {args.business_id}')
    rows=list_items(args.business_id,args.status,args.min_severity)
    if args.count:print(len(rows));return
    compact=[{'id':obj['id'],'severity':obj['severity'],'status':obj['status'],'attention_type':obj['attention_type'],'title':obj['title'],'reason':obj['reason'],'recommended_action':obj.get('recommended_action'),'occurrence_count':obj['occurrence_count'],'first_seen':obj['first_seen'],'last_seen':obj['last_seen'],'next_review_at':obj.get('next_review_at'),'path':str(path.relative_to(ROOT))} for obj,path in rows]
    if args.json:print(json.dumps({'business_id':args.business_id,'count':len(compact),'items':compact},indent=2));return
    if not compact:print('No matching attention items.');return
    for item in compact:print(f"[{item['severity'].upper()}] {item['id']} {item['title']} (status={item['status']}, seen={item['occurrence_count']}x)\n  {item['reason']}"+(f"\n  next: {item['recommended_action']}" if item.get('recommended_action') else ''))

if __name__=='__main__':main()
