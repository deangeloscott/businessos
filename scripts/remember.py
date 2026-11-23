#!/usr/bin/env python3
"""Persist caller-authored durable organizational meaning without requiring a Run.

The active model/user supplies semantic content. AURA supplies only mechanical identity,
timestamps, local-reference resolution, canonical paths, schema validation, safe atomic
writes, business isolation, and rollback. Updates may explicitly remove obsolete semantic
fields; AURA does not infer what should change. A Run or playbook contract is optional
context, not a prerequisite for organizational memory.
"""
from pathlib import Path
import argparse,hashlib,json,re,secrets,collections

from _common import *
from canonical_store import canonical_path,schema_entry,validate_canonical,write_canonical
from validate_business import validate_business
from correction_impacts import correction_event
from generate_knowledge_layer import knowledge_layer_freshness

MECHANICAL_FIELDS={'id','object_type','schema_version','business_id','created_at','updated_at','lineage'}
SPECIALIZED_TYPES={
    'AttentionItem':'Use scripts/upsert_attention.py so semantic deduplication and recurrence history are preserved.',
    'PlatformChange':'Use scripts/record_platform_change.py so current/superseded platform state is versioned safely.',
    'PreferenceProfile':'Use scripts/upsert_preference_profile.py so applicability and preference semantics remain governed.',
}


def _item_type(item,index,number):
    existing_ref=item.get('object_ref');typ=item.get('object_type')
    if existing_ref:
        if existing_ref not in index:raise ValueError(f'Unknown canonical object_ref for update: {existing_ref}. scripts/enter.py lists current records; to add a new one, give object_type instead of object_ref.')
        existing_type=index[existing_ref][0].get('object_type')
        if typ is None:typ=existing_type
        elif typ!=existing_type:raise ValueError(f'object_ref {existing_ref} is {existing_type}, not {typ}.')
    if not isinstance(typ,str) or not typ:raise ValueError(f'objects[{number-1}] requires object_type when creating a new canonical object.')
    schema_entry(typ);return typ


def _id_prefix(object_type):
    _,schema=schema_entry(object_type)
    pattern=((schema.get('properties') or {}).get('id') or {}).get('pattern','')
    match=re.match(r'^\^([A-Za-z0-9]+)_',pattern)
    if not match:raise ValueError(f'{object_type} schema does not expose a supported canonical ID prefix.')
    return match.group(1)


def _new_id(object_type,business_id,known_ids):
    prefix=_id_prefix(object_type);stem=re.sub(r'[^a-z0-9_-]+','-',business_id.lower()).strip('-_')[:24] or 'business'
    while True:
        oid=f'{prefix}_{stem}_{secrets.token_hex(6)}'
        if oid not in known_ids:return oid


def _resolve_local(value,aliases):
    if isinstance(value,str) and value.startswith('@'):
        key=value[1:]
        if key not in aliases:raise ValueError(f'Unknown local memory reference: {value}')
        return aliases[key]
    if isinstance(value,list):return [_resolve_local(item,aliases) for item in value]
    if isinstance(value,dict):return {key:_resolve_local(item,aliases) for key,item in value.items()}
    return value


def _merge_extensions(existing,supplied):
    out=dict(existing or {})
    for key,value in (supplied or {}).items():
        if key=='businessos' and isinstance(value,dict):
            bos=dict(out.get('businessos') or {});bos.update(value);out['businessos']=bos
        else:out[key]=value
    return out


def _receipt(rows):
    created=sum(row['operation']=='created' for row in rows);updated=sum(row['operation']=='updated' for row in rows)
    types=collections.Counter(row['object_type'] for row in rows)
    return {'status':'saved','objects':len(rows),'created':created,'updated':updated,'object_types':dict(sorted(types.items())),'validation':'passed'}


def _stated(payload,index=None):
    """With the person's own message as "said", AURA keeps it as the source of the facts they stated in this save and
    fills in what such a fact needs (its source, authority, kind, status and quote). The caller writes only each
    fact's statement, in the person's words; the usual check that those words are theirs still applies. A correction
    to a fact the person stated earlier is sourced to the new message too, since that is now where its words come from."""
    said=payload.get('said') if isinstance(payload,dict) else None
    if said is None:return payload,False
    if not isinstance(said,str) or not said.strip():raise ValueError('"said" must be the person’s message, as text.')
    items=[];used=False
    for item in payload.get('objects') or []:
        existing=(index or {}).get(item.get('object_ref'),(None,))[0] if isinstance(item,dict) else None
        if (isinstance(existing,dict) and existing.get('object_type')=='BusinessClaim' and existing.get('authority')=='explicit_user'
                and isinstance(item.get('content'),dict) and 'statement' in item['content']):
            content=dict(item['content'])
            content.setdefault('support_quote',str(content.get('statement') or '').strip().rstrip('.!'))
            content.setdefault('source_ref','@said');used=True
            item={**item,'content':content}
        elif isinstance(item,dict) and item.get('object_type')=='BusinessClaim' and not item.get('object_ref') and isinstance(item.get('content'),dict):
            content=dict(item['content'])
            for key,value in (('claim_kind','approved_business_claim'),('status','approved'),('authority','explicit_user')):content.setdefault(key,value)
            if content['authority']=='explicit_user':
                content.setdefault('support_quote',str(content.get('statement') or '').strip().rstrip('.!'))
                content.setdefault('source_ref','@said');used=True
            item={**item,'content':content}
        items.append(item)
    if used:
        items.insert(0,{'key':'said','object_type':'SourceRecord','content':{
            'source_type':'user_statement','source_reference':'Told in chat','origin':'active user conversation','retrieved_at':now(),
            'access_scope':'business-private','access_class':'private','content_hash':hashlib.sha256(said.encode('utf-8')).hexdigest(),
            'content_hash_target':'captured_text','extensions':{'authority':'explicit_user','verbatim_user_statement':said,
            'businessos_evidence':{'capture_status':'captured','capture_method':'text_excerpt','acquisition_method':'user_provided','captured_text':said}}}})
    return {**payload,'objects':items},used


@organization_transaction
def remember(business_id,payload):
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':raise ValueError(resolved.get('reason') or 'Organization could not be resolved.')
    bid=resolved['business_id'];index=object_index(bid)
    payload,stated=_stated(payload,index)
    items=payload.get('objects') if isinstance(payload,dict) else None
    if not isinstance(items,list) or not items:raise ValueError('Input requires a non-empty objects list.')
    provenance=payload.get('provenance') if isinstance(payload.get('provenance'),dict) else None

    known_ids=set(index);aliases={};prepared=[];targets=set()
    for number,item in enumerate(items,1):
        if not isinstance(item,dict):raise ValueError(f'objects[{number-1}] must be an object.')
        existing_ref=item.get('object_ref');typ=_item_type(item,index,number);content=item.get('content')
        if typ in SPECIALIZED_TYPES:raise ValueError(f'{typ} uses a specialized supported interface. {SPECIALIZED_TYPES[typ]}')
        if not isinstance(content,dict):raise ValueError(f'objects[{number-1}].content must contain caller-authored semantic fields.')
        if 'replace_extensions' in item and (not isinstance(item['replace_extensions'],bool) or not existing_ref or 'extensions' not in content):
            raise ValueError('replace_extensions requires an existing object and an explicit extensions object.')
        if 'correction_summary' in item and (not existing_ref or not isinstance(item['correction_summary'],str) or not item['correction_summary'].strip()):
            raise ValueError('correction_summary requires an existing object_ref and a non-empty explanation.')
        forbidden=sorted(MECHANICAL_FIELDS & set(content))
        if forbidden:raise ValueError('Mechanical fields belong to AURA, not content: '+', '.join(forbidden))
        remove_fields=item.get('remove_fields',[])
        if not isinstance(remove_fields,list) or not all(isinstance(field,str) and field for field in remove_fields):
            raise ValueError(f'objects[{number-1}].remove_fields must be a list of non-empty top-level field names.')
        if len(remove_fields)!=len(set(remove_fields)):
            raise ValueError(f'objects[{number-1}].remove_fields contains duplicates.')
        mechanical_removals=sorted(MECHANICAL_FIELDS & set(remove_fields))
        if mechanical_removals:raise ValueError('Mechanical fields may not be removed: '+', '.join(mechanical_removals))
        overlap=sorted(set(remove_fields) & set(content))
        if overlap:raise ValueError('A field cannot be updated and removed in the same object: '+', '.join(overlap))
        if remove_fields and not existing_ref:
            raise ValueError(f'objects[{number-1}].remove_fields is only valid when updating an existing canonical object.')
        key=item.get('key') or existing_ref or f'object_{number}'
        if not isinstance(key,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',key):
            raise ValueError(f'objects[{number-1}] key must be simple letters/numbers/_/-. Omit it when local cross-object references are not needed.')
        if key in aliases:raise ValueError(f'Duplicate local memory key: {key}')
        if existing_ref:
            existing,path=index[existing_ref]
            missing=[field for field in remove_fields if field not in existing]
            if missing:raise ValueError('Cannot remove fields that are not present on the current object: '+', '.join(sorted(missing)))
            oid=existing_ref
        else:
            existing={};path=None;oid=_new_id(typ,bid,known_ids);known_ids.add(oid)
        if oid in targets:raise ValueError(f'Canonical object is targeted more than once in one input: {oid}')
        targets.add(oid);aliases[key]=oid
        prepared.append({'item':item,'type':typ,'content':content,'remove_fields':remove_fields,'existing':existing,'path':path,'id':oid,'key':key})

    ts=now();objects=[]
    for row in prepared:
        item=row['item'];typ=row['type'];existing=row['existing'];content=_resolve_local(dict(row['content']),aliases)
        remove_fields=set(row['remove_fields'])
        lineage=_resolve_local(item.get('lineage_refs',[]),aliases)
        if not isinstance(lineage,list) or not all(isinstance(x,str) and x for x in lineage):
            raise ValueError(f'{row["key"]} lineage_refs must be a list of canonical refs or @local keys.')
        _,schema=schema_entry(typ);properties=schema.get('properties') or {}
        obj=dict(existing)
        for field in remove_fields:obj.pop(field,None)
        old_extensions=obj.get('extensions') if isinstance(obj.get('extensions'),dict) and not item.get('replace_extensions') else {}
        supplied_extensions=content.pop('extensions',{})
        if not isinstance(supplied_extensions,dict):raise ValueError(f'{row["key"]} content.extensions must be an object when supplied.')
        obj.update(content)
        obj.update({
            'id':row['id'],'object_type':typ,'schema_version':existing.get('schema_version','1.0.0'),
            'business_id':bid,
        })
        if 'created_at' in properties:obj['created_at']=existing.get('created_at',ts)
        if 'updated_at' in properties:obj['updated_at']=ts
        if 'lineage' in properties:
            prior_lineage=existing.get('lineage') if isinstance(existing.get('lineage'),list) else []
            if not existing or 'lineage' in existing or lineage:
                obj['lineage']=list(dict.fromkeys([*prior_lineage,*lineage]))
        elif lineage:
            raise ValueError(f'{typ} does not support lineage_refs; preserve provenance in a schema-supported field instead.')
        if 'extensions' in properties:
            if 'extensions' in remove_fields and not supplied_extensions and not provenance:
                obj.pop('extensions',None)
            elif not existing or 'extensions' in existing or supplied_extensions or provenance:
                obj['extensions']=_merge_extensions(old_extensions,supplied_extensions)
                if provenance:
                    bos=obj['extensions'].setdefault('businessos',{});bos['memory_provenance']=dict(provenance)
        elif supplied_extensions or provenance:
            raise ValueError(f'{typ} does not support extensions/provenance payloads.')
        if 'observed_at' in properties and not obj.get('observed_at'):obj['observed_at']=ts
        # Defaults describe a new deliverable, never override later explicit edits.
        if typ=='Asset' and not existing:
            from workspace_projects import asset_context
            obj=asset_context(bid,obj)
        elif not existing and 'extensions' in properties:
            from workspace_projects import saved_during
            obj=saved_during(bid,obj)
        try:validate_canonical(typ,obj)
        except ValueError as exc:raise ValueError(f'{row["key"]} ({typ}): {exc}. See the {typ} schema and docs/operator-guide.md memory examples.') from exc
        row['object']=obj;objects.append(obj)

    paths=[];snapshots={};corrections=[]
    try:
        for row,obj in zip(prepared,objects):
            path=Path(row['path']) if row['path'] else canonical_path(bid,obj)
            if path.exists():snapshots[path]=path.read_bytes()
            written=write_canonical(obj,path,allow_update=bool(row['existing']))
            paths.append(written);row['path']=written
        for row in prepared:
            if not row['existing']:continue
            event=correction_event(bid,row['existing'],row['object'],row['item'].get('correction_summary'),_new_id('ChangeEvent',bid,known_ids),ts)
            if event:
                validate_canonical('ChangeEvent',event)
                path=write_canonical(event);paths.append(path)
                corrections.append(describe_object(event,path))
        errors,warnings,counts=validate_business(bid)
        if errors:raise ValueError('Post-persistence validation failed: '+'; '.join(errors[:12]))
    except Exception:
        for path in reversed(paths):
            if path in snapshots:path.write_bytes(snapshots[path])
            elif path.exists():path.unlink()
        raise

    # Optional feedback observes a confirmed save; it never changes persistence semantics.
    try:
        from workspace_memory_feedback import record
        feedback=record(bid,[row for row in prepared if not (stated and row['key']=='said')],snapshots)
    except (OSError,ValueError,TypeError,KeyError):feedback=[]

    rows=[{
        'key':row['key'],'id':row['id'],'object_type':row['type'],
        'operation':'updated' if row['existing'] else 'created','removed_fields':list(row['remove_fields']),'path':storage_ref(row['path'])
    } for row in prepared]
    return {
        'format_version':'1.0','status':'persisted','business_id':bid,'objects':rows,'receipt':_receipt(rows),
        'corrections':corrections,'memory_feedback':[r['id'] for r in feedback],
        'knowledge_view':knowledge_layer_freshness(bid),
        'validation':{'status':'clean','warnings':warnings[:5],'canonical_object_counts':counts,'scope':'Schema, reference/provenance integrity and organization isolation; not factual accuracy, artifact quality, deployment or measured effect.'},
        'semantic_boundary':'Only caller-authored organizational meaning was persisted; AURA supplied mechanical canonical wrapping, explicit field removal, storage, and integrity validation.',
    }


def main():
    ap=argparse.ArgumentParser(description='Remember durable organization-owned meaning without requiring a Run or AURA playbook.')
    ap.add_argument('business_id');ap.add_argument('--input',required=True,help='JSON file, - for stdin, or inline JSON with a non-empty objects list and optional provenance object. New objects require object_type; updates can infer it from object_ref. key is optional unless @local references are needed.')
    a=ap.parse_args()
    try:payload=read_json_input(a.input);result=remember(a.business_id,payload)
    except (ValueError,FileExistsError,json.JSONDecodeError,OSError) as exc:raise SystemExit(str(exc))
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
