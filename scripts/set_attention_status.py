#!/usr/bin/env python3
from _common import *
import argparse,json

def find_item(bid,aid):
    for obj,p in iter_instance_objects(bid):
        if obj.get('object_type')=='AttentionItem' and obj.get('id')==aid:return obj,p
    return None,None

def main():
    ap=argparse.ArgumentParser(description='Acknowledge, resolve, or supersede one AttentionItem.')
    ap.add_argument('business_id'); ap.add_argument('attention_id'); ap.add_argument('status',choices=['open','acknowledged','resolved','superseded']); ap.add_argument('--resolution-ref',action='append',default=[]); ap.add_argument('--superseded-by'); ap.add_argument('--note'); ap.add_argument('--at'); a=ap.parse_args(); ts=a.at or now()
    obj,p=find_item(a.business_id,a.attention_id)
    if not obj: raise SystemExit('AttentionItem not found')
    old=obj['status']; new=a.status
    machines=json.loads((ROOT/'core/references/state-machines.json').read_text()); allowed=machines['AttentionItem']['transitions'].get(old,[])
    if new!=old and new not in allowed: raise SystemExit(f'Invalid AttentionItem transition {old} -> {new}; allowed={allowed}')
    if new=='resolved' and not (a.resolution_ref or a.note): raise SystemExit('resolved requires --resolution-ref or --note')
    if new=='superseded' and not a.superseded_by: raise SystemExit('superseded requires --superseded-by')
    bos=obj.setdefault('extensions',{}).setdefault('businessos',{});hist=bos.setdefault('transition_history',[])
    if old!=new:
        hist.append({'from':old,'to':new,'at':ts,'note':a.note});
        if len(hist)>50: del hist[:-50]
    obj['status']=new;obj['updated_at']=ts
    if new=='acknowledged':obj['acknowledged_at']=ts
    if new=='resolved': obj['resolved_at']=ts;obj['resolution_refs']=sorted(set(obj.get('resolution_refs',[])+a.resolution_ref));obj['next_review_at']=None
    if new=='superseded':obj['superseded_by']=a.superseded_by;obj['next_review_at']=None
    if new=='open': obj['resolved_at']=None;obj['superseded_by']=None
    p.write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({'attention_id':obj['id'],'from':old,'to':new,'path':str(p.relative_to(ROOT))},indent=2))
if __name__=='__main__': main()
