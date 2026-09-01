#!/usr/bin/env python3
"""Create or refresh one deduplicated durable AttentionItem."""
from _common import *
import argparse,json,hashlib

SEVERITY={'informational':0,'low':1,'medium':2,'high':3,'critical':4}


def _merge(a,b):return sorted(set((a or [])+(b or [])))
def _id(business_id,key):return f"att_{business_id}_{hashlib.sha256(f'{business_id}\0{key}'.encode()).hexdigest()[:16]}"
def _path(business_id,attention_id):
    path=ROOT/'instances'/business_id/'operations'/'attention'/f'{attention_id}.json';path.parent.mkdir(parents=True,exist_ok=True);return path

def _find(business_id,key):
    for obj,path in iter_instance_objects(business_id):
        if obj.get('object_type')=='AttentionItem' and obj.get('dedupe_key')==key:return obj,path
    return None,None


def upsert(business_id,key,attention_type,severity,title,reason,recommended_action=None,owner_system='core',source_refs=None,evidence_refs=None,lineage=None,next_review_at=None,retention_class='operational',seen_at=None):
    seen_at=seen_at or now();source_refs=source_refs or [];evidence_refs=evidence_refs or [];lineage=lineage or []
    obj,path=_find(business_id,key);created=False;reopened=False
    if obj is None:
        attention_id=_id(business_id,key);path=_path(business_id,attention_id);created=True
        obj={'id':attention_id,'object_type':'AttentionItem','schema_version':'1.0.0','business_id':business_id,'created_at':seen_at,'updated_at':seen_at,'lineage':sorted(set(lineage)),'owner_system':owner_system,'dedupe_key':key,'attention_type':attention_type,'severity':severity,'status':'open','title':title,'reason':reason,'recommended_action':recommended_action,'source_refs':sorted(set(source_refs)),'evidence_refs':sorted(set(evidence_refs)),'first_seen':seen_at,'last_seen':seen_at,'occurrence_count':1,'next_review_at':next_review_at,'acknowledged_at':None,'resolved_at':None,'resolution_refs':[],'retention_class':retention_class,'extensions':{}}
    else:
        old_status=obj.get('status')
        if old_status in {'resolved','archived'}:
            reopened=True;obj['status']='open';obj['resolved_at']=None;obj['acknowledged_at']=None
        obj['updated_at']=seen_at;obj['last_seen']=seen_at;obj['occurrence_count']=int(obj.get('occurrence_count',0))+1
        if SEVERITY.get(severity,-1)>SEVERITY.get(obj.get('severity','informational'),0):obj['severity']=severity
        obj['attention_type']=attention_type;obj['title']=title;obj['reason']=reason
        if recommended_action is not None:obj['recommended_action']=recommended_action
        obj['source_refs']=_merge(obj.get('source_refs'),source_refs);obj['evidence_refs']=_merge(obj.get('evidence_refs'),evidence_refs);obj['lineage']=_merge(obj.get('lineage'),lineage)
        if next_review_at is not None:obj['next_review_at']=next_review_at
    old_path=path;path=_path(business_id,obj['id']) if path is None or '/history/' in path.as_posix() else path
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')
    if old_path is not None and old_path.resolve()!=path.resolve() and old_path.exists():old_path.unlink()
    return obj,path,created,reopened


def main():
    parser=argparse.ArgumentParser(description='Create/update one deduplicated AURA AttentionItem. It records a material condition needing awareness, not a permission or task gate.')
    parser.add_argument('business_id');parser.add_argument('--dedupe-key',required=True);parser.add_argument('--type',dest='attention_type',required=True);parser.add_argument('--severity',choices=SEVERITY,required=True);parser.add_argument('--title',required=True);parser.add_argument('--reason',required=True);parser.add_argument('--recommended-action');parser.add_argument('--owner-system',default='core');parser.add_argument('--source-ref',action='append',default=[]);parser.add_argument('--evidence-ref',action='append',default=[]);parser.add_argument('--lineage-ref',action='append',default=[]);parser.add_argument('--next-review-at');parser.add_argument('--retention-class',choices=['operational','durable'],default='operational');parser.add_argument('--seen-at');args=parser.parse_args()
    if not (ROOT/'instances'/args.business_id).exists():raise SystemExit(f'Unknown business: {args.business_id}')
    try:obj,path,created,reopened=upsert(args.business_id,args.dedupe_key,args.attention_type,args.severity,args.title,args.reason,args.recommended_action,args.owner_system,args.source_ref,args.evidence_ref,args.lineage_ref,args.next_review_at,args.retention_class,args.seen_at)
    except ValueError as exc:raise SystemExit(str(exc))
    print(json.dumps({'attention_id':obj['id'],'status':obj['status'],'created':created,'reopened':reopened,'occurrence_count':obj['occurrence_count'],'path':str(path.relative_to(ROOT))},indent=2))

if __name__=='__main__':main()
