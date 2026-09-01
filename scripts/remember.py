#!/usr/bin/env python3
"""Persist caller-authored durable organizational meaning without requiring a Run.

The active model/user supplies semantic content. AURA supplies only mechanical identity,
timestamps, local-reference resolution, canonical paths, schema validation, safe atomic
writes, business isolation, and rollback. A Run or playbook contract is optional context,
not a prerequisite for organizational memory.
"""
from pathlib import Path
import argparse,json,re,secrets

from _common import *
from canonical_store import canonical_path,schema_entry,validate_canonical,write_canonical
from validate_business import validate_business

MECHANICAL_FIELDS={'id','object_type','schema_version','business_id','created_at','updated_at','lineage'}
SPECIALIZED_TYPES={
    'AttentionItem':'Use scripts/upsert_attention.py so semantic deduplication and recurrence history are preserved.',
    'PlatformChange':'Use scripts/record_platform_change.py so current/superseded platform state is versioned safely.',
    'PreferenceProfile':'Use scripts/upsert_preference_profile.py so applicability and preference semantics remain governed.',
}


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


def remember(business_id,payload):
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':raise ValueError(resolved.get('reason') or 'Organization could not be resolved.')
    bid=resolved['business_id'];items=payload.get('objects') if isinstance(payload,dict) else None
    if not isinstance(items,list) or not items:raise ValueError('Input requires a non-empty objects list.')
    provenance=payload.get('provenance') if isinstance(payload.get('provenance'),dict) else None

    index=object_index(bid);known_ids=set(index);aliases={};prepared=[];targets=set()
    for number,item in enumerate(items,1):
        if not isinstance(item,dict):raise ValueError(f'objects[{number-1}] must be an object.')
        typ=item.get('object_type');content=item.get('content');existing_ref=item.get('object_ref')
        if not isinstance(typ,str) or not typ:raise ValueError(f'objects[{number-1}] requires object_type.')
        schema_entry(typ)
        if typ in SPECIALIZED_TYPES:raise ValueError(f'{typ} uses a specialized supported interface. {SPECIALIZED_TYPES[typ]}')
        if not isinstance(content,dict):raise ValueError(f'objects[{number-1}].content must contain caller-authored semantic fields.')
        forbidden=sorted(MECHANICAL_FIELDS & set(content))
        if forbidden:raise ValueError('Mechanical fields belong to AURA, not content: '+', '.join(forbidden))
        key=item.get('key') or existing_ref
        if not isinstance(key,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',key):
            raise ValueError(f'objects[{number-1}] requires a simple unique key (letters/numbers/_/-).')
        if key in aliases:raise ValueError(f'Duplicate local memory key: {key}')
        if existing_ref:
            if existing_ref not in index:raise ValueError(f'Unknown canonical object_ref for update: {existing_ref}')
            existing,path=index[existing_ref]
            if existing.get('object_type')!=typ:raise ValueError(f'object_ref {existing_ref} is {existing.get("object_type")}, not {typ}.')
            oid=existing_ref
        else:
            existing={};path=None;oid=_new_id(typ,bid,known_ids);known_ids.add(oid)
        if oid in targets:raise ValueError(f'Canonical object is targeted more than once in one input: {oid}')
        targets.add(oid);aliases[key]=oid
        prepared.append({'item':item,'type':typ,'content':content,'existing':existing,'path':path,'id':oid,'key':key})

    ts=now();objects=[]
    for row in prepared:
        item=row['item'];typ=row['type'];existing=row['existing'];content=_resolve_local(dict(row['content']),aliases)
        lineage=_resolve_local(item.get('lineage_refs',[]),aliases)
        if not isinstance(lineage,list) or not all(isinstance(x,str) and x for x in lineage):
            raise ValueError(f'{row["key"]} lineage_refs must be a list of canonical refs or @local keys.')
        obj=dict(existing);old_extensions=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        supplied_extensions=content.pop('extensions',{})
        if not isinstance(supplied_extensions,dict):raise ValueError(f'{row["key"]} content.extensions must be an object when supplied.')
        obj.update(content)
        obj.update({
            'id':row['id'],'object_type':typ,'schema_version':existing.get('schema_version','1.0.0'),
            'business_id':bid,'created_at':existing.get('created_at',ts),'updated_at':ts,
        })
        prior_lineage=existing.get('lineage') if isinstance(existing.get('lineage'),list) else []
        obj['lineage']=list(dict.fromkeys([*prior_lineage,*lineage]))
        obj['extensions']=_merge_extensions(old_extensions,supplied_extensions)
        if provenance:
            bos=obj['extensions'].setdefault('businessos',{})
            bos['memory_provenance']=dict(provenance)
        _,schema=schema_entry(typ);properties=schema.get('properties') or {}
        if 'observed_at' in properties and not obj.get('observed_at'):obj['observed_at']=ts
        validate_canonical(typ,obj);row['object']=obj;objects.append(obj)

    paths=[];snapshots={}
    try:
        for row,obj in zip(prepared,objects):
            path=Path(row['path']) if row['path'] else canonical_path(bid,obj)
            if path.exists():snapshots[path]=path.read_bytes()
            written=write_canonical(obj,path,allow_update=bool(row['existing']))
            paths.append(written);row['path']=written
        errors,warnings,counts=validate_business(bid)
        if errors:raise ValueError('Post-persistence validation failed: '+'; '.join(errors[:12]))
    except Exception:
        for path in reversed(paths):
            if path in snapshots:path.write_bytes(snapshots[path])
            elif path.exists():path.unlink()
        raise

    rows=[{
        'key':row['key'],'id':row['id'],'object_type':row['type'],
        'operation':'updated' if row['existing'] else 'created','path':storage_ref(row['path'])
    } for row in prepared]
    return {
        'format_version':'1.0','status':'persisted','business_id':bid,'objects':rows,
        'validation':{'status':'clean','warnings':warnings[:5],'canonical_object_counts':counts},
        'semantic_boundary':'Only caller-authored organizational meaning was persisted; AURA supplied mechanical canonical wrapping, storage, and integrity validation.',
    }


def main():
    ap=argparse.ArgumentParser(description='Remember durable organization-owned meaning without requiring a Run or AURA playbook.')
    ap.add_argument('business_id');ap.add_argument('--input',required=True,help='JSON file containing a non-empty objects list and optional provenance object.')
    a=ap.parse_args()
    try:payload=json.loads(Path(a.input).read_text(encoding='utf-8'));result=remember(a.business_id,payload)
    except (ValueError,FileExistsError,json.JSONDecodeError,OSError) as exc:raise SystemExit(str(exc))
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
