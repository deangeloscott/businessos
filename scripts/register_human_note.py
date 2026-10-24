#!/usr/bin/env python3
"""Register a human knowledge note as noncanonical source material with provenance."""
from _common import *
from canonical_store import validate_canonical, write_canonical
import argparse,hashlib,json,os


def register_note(business_id,note_ref):
    base=instance_dir(business_id)
    if not base.exists(): raise ValueError(f'Unknown business: {business_id}')
    notes=(knowledge_root()/business_id/'notes').resolve()
    raw=Path(note_ref)
    path=raw.resolve() if raw.is_absolute() else (notes/raw).resolve()
    if not path.is_relative_to(notes): raise ValueError('Human note must be inside knowledge/<business-id>/notes/')
    if not path.exists() or not path.is_file(): raise ValueError(f'Human note not found: {path}')
    if path.suffix.lower() not in {'.md','.txt'}: raise ValueError('Human note must be Markdown or plain text')
    content=path.read_bytes();text=content.decode('utf-8');digest=hashlib.sha256(content).hexdigest();logical=storage_ref(path)
    oid='src_human_note_'+hashlib.sha256((business_id+'\0'+logical+'\0'+digest).encode()).hexdigest()[:20]
    obj={
        'id':oid,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
        'source_type':'human_knowledge_note','source_reference':logical,'origin':'human_authored_workspace_note',
        'retrieved_at':now(),'published_at':None,'content_hash':'sha256:'+digest,'access_scope':'business-private',
        'content_hash_target':'captured_text','access_class':'private',
        'extensions':{
            'businessos_evidence':{
                'capture_status':'captured','capture_method':'text_snapshot','acquisition_method':'user_provided',
                'acquisition_reference':logical,'captured_text':text,
                'capture_notes':'Exact UTF-8 note bytes read at registration; supplied statements are not independently verified facts.'
            },
            'businessos':{
                'canonical_truth':False,'source_material_only':True,
                'rule':'Registering a human note preserves provenance but does not make its statements canonical business truth.'
            }
        }
    }
    out=base/'intelligence/sources'/f'{oid}.json';out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():
        existing=json.loads(out.read_text(encoding='utf-8'))
        # Re-registering unchanged bytes can complete the old native writer's
        # capture metadata without changing identity, history or authored fields.
        if existing.get('content_hash')!=obj['content_hash'] or existing.get('source_reference')!=logical:
            raise ValueError('Existing human-note source does not match the registered bytes/reference')
        upgraded=json.loads(json.dumps(existing))
        upgraded.setdefault('access_class','private')
        if not upgraded.get('extensions',{}).get('businessos_evidence') and not upgraded.get('content_hash_target'):
            upgraded['content_hash_target']='captured_text'
            upgraded.setdefault('extensions',{})['businessos_evidence']=obj['extensions']['businessos_evidence']
        if upgraded!=existing:
            validate_canonical('SourceRecord',upgraded)
            write_canonical(upgraded,out,allow_update=True)
        return upgraded,out,False
    validate_canonical('SourceRecord',obj)
    write_canonical(obj,out)
    return obj,out,True


def main():
    p=argparse.ArgumentParser(description='Register a note from knowledge/<business-id>/notes as noncanonical SourceRecord evidence. This does not promote the note to business truth.')
    p.add_argument('business_id');p.add_argument('note');p.add_argument('--json',action='store_true');a=p.parse_args()
    try:obj,path,created=register_note(a.business_id,a.note)
    except ValueError as e:raise SystemExit(str(e))
    result={'created':created,'source_record_id':obj['id'],'source_reference':obj['source_reference'],'path':storage_ref(path),'canonical_truth':False}
    print(json.dumps(result,indent=2) if a.json else f"registered human note source: {obj['id']} -> {obj['source_reference']} (canonical_truth=false)")

if __name__=='__main__':main()
