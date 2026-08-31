#!/usr/bin/env python3
"""Create/update one deduplicated AURA AttentionItem."""
from _common import *
import argparse,json,hashlib

SEV={'informational':0,'low':1,'medium':2,'high':3,'critical':4}

def _merge(a,b):return sorted(set((a or [])+(b or [])))
def _id(bid,key):return f"att_{bid}_{hashlib.sha256(f'{bid}\0{key}'.encode()).hexdigest()[:16]}"
def _path(bid,aid):
    p=ROOT/'instances'/bid/'operations'/'attention'/f'{aid}.json';p.parent.mkdir(parents=True,exist_ok=True);return p

def _find(bid,key):
    for obj,p in iter_instance_objects(bid):
        if obj.get('object_type')=='AttentionItem' and obj.get('dedupe_key')==key:return obj,p
    return None,None

def upsert(bid,key,attention_type,severity,title,reason,recommended_action=None,owner_system='core',source_refs=None,evidence_refs=None,lineage=None,next_review_at=None,retention_class='operational',seen_at=None):
    seen_at=seen_at or now();source_refs=source_refs or [];evidence_refs=evidence_refs or [];lineage=lineage or []
    obj,p=_find(bid,key);created=False;reopened=False
    if obj is None:
        aid=_id(bid,key);p=_path(bid,aid);created=True
        obj={'id':aid,'object_type':'AttentionItem','schema_version':'1.0.0','business_id':bid,'created_at':seen_at,'updated_at':seen_at,'lineage':sorted(set(lineage)),'owner_system':owner_system,'dedupe_key':key,'attention_type':attention_type,'severity':severity,'status':'open','title':title,'reason':reason,'recommended_action':recommended_action,'source_refs':sorted(set(source_refs)),'evidence_refs':sorted(set(evidence_refs)),'first_seen':seen_at,'last_seen':seen_at,'occurrence_count':1,'next_review_at':next_review_at,'acknowledged_at':None,'resolved_at':None,'resolution_refs':[],'supersedes':[],'superseded_by':None,'retention_class':retention_class,'extensions':{'aura':{'transition_history':[],'reopen_count':0}}}
    else:
        old_status=obj.get('status')
        if old_status in {'resolved','archived'}:
            reopened=True;aura=obj.setdefault('extensions',{}).setdefault('aura',{});hist=aura.setdefault('transition_history',[]);hist.append({'from':old_status,'to':'open','at':seen_at,'reason':'condition_recurred'})
            if len(hist)>50:del hist[:-50]
            aura['reopen_count']=int(aura.get('reopen_count',0))+1;obj['status']='open';obj['resolved_at']=None;obj['acknowledged_at']=None;obj['superseded_by']=None
        elif old_status=='superseded':raise ValueError(f'attention item {obj["id"]} is superseded; use the current replacement or a new semantic dedupe_key')
        obj['updated_at']=seen_at;obj['last_seen']=seen_at;obj['occurrence_count']=int(obj.get('occurrence_count',0))+1
        if SEV.get(severity,-1)>SEV.get(obj.get('severity','informational'),0):obj['severity']=severity
        obj['attention_type']=attention_type;obj['title']=title;obj['reason']=reason
        if recommended_action is not None:obj['recommended_action']=recommended_action
        obj['source_refs']=_merge(obj.get('source_refs'),source_refs);obj['evidence_refs']=_merge(obj.get('evidence_refs'),evidence_refs);obj['lineage']=_merge(obj.get('lineage'),lineage)
        if next_review_at is not None:obj['next_review_at']=next_review_at
    old_path=p;p=_path(bid,obj['id']) if p is None or '/history/' in p.as_posix() else p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
    if old_path is not None and old_path.resolve()!=p.resolve() and old_path.exists():old_path.unlink()
    return obj,p,created,reopened

def main():
    ap=argparse.ArgumentParser(description='Create/update one deduplicated AURA AttentionItem. It records a material condition needing awareness, not a permission/blocking gate.')
    ap.add_argument('business_id');ap.add_argument('--dedupe-key',required=True);ap.add_argument('--type',dest='attention_type',required=True);ap.add_argument('--severity',choices=SEV,required=True);ap.add_argument('--title',required=True);ap.add_argument('--reason',required=True);ap.add_argument('--recommended-action');ap.add_argument('--owner-system',default='core');ap.add_argument('--source-ref',action='append',default=[]);ap.add_argument('--evidence-ref',action='append',default=[]);ap.add_argument('--lineage-ref',action='append',default=[]);ap.add_argument('--next-review-at');ap.add_argument('--retention-class',choices=['operational','durable'],default='operational');ap.add_argument('--seen-at');a=ap.parse_args()
    if not (ROOT/'instances'/a.business_id).exists():raise SystemExit(f'Unknown business: {a.business_id}')
    try:obj,p,created,reopened=upsert(a.business_id,a.dedupe_key,a.attention_type,a.severity,a.title,a.reason,a.recommended_action,a.owner_system,a.source_ref,a.evidence_ref,a.lineage_ref,a.next_review_at,a.retention_class,a.seen_at)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'attention_id':obj['id'],'status':obj['status'],'created':created,'reopened':reopened,'occurrence_count':obj['occurrence_count'],'path':str(p.relative_to(ROOT))},indent=2))
if __name__=='__main__':main()
