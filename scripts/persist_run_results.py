#!/usr/bin/env python3
"""Persist AI-authored canonical business results without schema/provenance scaffolding.

The caller supplies substantive fields. AURA supplies only mechanical identity, IDs,
timestamps, local-reference resolution, storage, Run provenance, schema validation, and
focused active-Run validation. No business conclusion or action is synthesized here.
"""
from pathlib import Path
import argparse, json, os, re, secrets

from _common import *
from canonical_store import canonical_path, schema_entry, validate_canonical, write_canonical
from validate_business import validate_business


MECHANICAL_FIELDS={'id','object_type','schema_version','business_id','created_at','updated_at','lineage'}
MECHANICAL_PROVENANCE_FIELDS={'run_ref','run_id','run_contract_id','run_binding','run_history_refs','contract_chain'}
SPECIALIZED_TYPES={
    'AttentionItem':'Use scripts/upsert_attention.py so semantic deduplication and recurrence history are preserved.',
    'PlatformChange':'Use scripts/record_platform_change.py so current/superseded platform state is versioned safely.',
    'SourceRecord':'Use scripts/persist_research_bundle.py so acquisition, capture, hashes, and evidence support remain governed.',
    'PreferenceProfile':'Use scripts/upsert_preference_profile.py so applicability and preference semantics remain governed.',
    'Business':'Use scripts/bootstrap_explicit_context.py or a governed ContextUpdateProposal; do not rewrite explicit business truth through a Run-result wrapper.',
    'Brand':'Use scripts/bootstrap_explicit_context.py or a governed ContextUpdateProposal; do not self-assert Brand authority.',
    'BusinessClaim':'Use scripts/bootstrap_explicit_context.py or a governed ContextUpdateProposal; do not self-assert claim authority.',
}


def _selector_types(values):
    out=set()
    for value in values or []:
        typ=value.get('type') if isinstance(value,dict) else value
        if isinstance(typ,str) and typ.strip():out.add(typ.strip())
    return out


def _run_state(business_id,run_id):
    rd=run_dir_path(business_id,run_id);rp=rd/'run.json';mp=rd/'contract-execution.json'
    if not rp.exists() or not mp.exists():raise ValueError(f'Unknown or incomplete Run: {run_id}')
    run=json.loads(rp.read_text());manifest=json.loads(mp.read_text())
    if run.get('business_id')!=business_id or manifest.get('business_id')!=business_id or manifest.get('run_id')!=run_id:
        raise ValueError('Run identity does not match the requested business/Run.')
    if run.get('status')!='active' or manifest.get('root_status')!='active':
        raise ValueError(f'Run is not active: {run_id}')
    contracts={row['id']:row for row in load_registry().get('contracts',[]) if row.get('id')}
    root_id=manifest.get('root_contract_id');root=contracts.get(root_id)
    if not root:raise ValueError(f'Installed root contract metadata is missing: {root_id!r}')
    required=[]
    for cid in manifest.get('required_subcontracts') or []:
        contract=contracts.get(cid)
        if not contract:raise ValueError(f'Installed subcontract metadata is missing: {cid!r}')
        required.append(contract)
    allowed=_selector_types(root.get('writes'))
    for contract in required:allowed.update(_selector_types(contract.get('writes')))
    return rd,run,manifest,root,required,allowed


def _id_prefix(object_type):
    _,schema=schema_entry(object_type);pattern=((schema.get('properties') or {}).get('id') or {}).get('pattern','')
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
        if key not in aliases:raise ValueError(f'Unknown local result reference: {value}')
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


def _contract_chain(object_type,item,root,required):
    root_id=root['id'];required_by_id={contract['id']:contract for contract in required}
    explicit=item.get('contract_refs')
    if explicit is not None:
        if not isinstance(explicit,list) or not all(isinstance(x,str) and x for x in explicit):
            raise ValueError('contract_refs must be a list of required subcontract IDs when supplied.')
        unknown=sorted(set(explicit)-set(required_by_id))
        if unknown:raise ValueError('contract_refs contains contracts outside this Run: '+', '.join(unknown))
        wrong=sorted(cid for cid in explicit if object_type not in _selector_types(required_by_id[cid].get('writes')))
        if wrong:raise ValueError(f'{object_type} is not a declared write type for contract_refs: '+', '.join(wrong))
        return [root_id,*dict.fromkeys(explicit)]
    matching=[contract['id'] for contract in required if object_type in _selector_types(contract.get('writes'))]
    # A unique matching required contract is mechanical provenance, not a semantic
    # choice. Multiple matching contracts require the AI to state contract_refs.
    if len(matching)==1:return [root_id,matching[0]]
    if object_type=='Asset' and root.get('artifact_role')=='customer_facing_production_root':
        return [root_id,*[contract['id'] for contract in required]]
    return [root_id]


def _stamp_provenance(obj,business_id,run_id,root_id,chain):
    extensions=obj.setdefault('extensions',{});bos=extensions.setdefault('businessos',{})
    prior=bos.get('run_ref');history=list(bos.get('run_history_refs') or [])
    if prior and prior not in history:history.append(prior)
    run_ref=f'runtime/runs/{business_id}/{run_id}'
    if run_ref not in history:history.append(run_ref)
    bos.update({
        'run_ref':run_ref,'run_id':run_id,'run_contract_id':root_id,
        'run_binding':'persisted_active_run_result','run_history_refs':history,
        'contract_chain':chain,
    })


def persist_run_results(business_id,run_id,payload,workspace=None):
    if workspace:os.environ['BUSINESSOS_WORKSPACE']=str(Path(workspace).expanduser().resolve())
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':raise ValueError(resolved.get('reason') or 'Business could not be resolved.')
    bid=resolved['business_id'];rd,run,manifest,root,required,allowed=_run_state(bid,run_id)
    items=payload.get('objects') if isinstance(payload,dict) else None
    if not isinstance(items,list) or not items:raise ValueError('Input requires a non-empty objects list.')

    index=object_index(bid);known_ids=set(index);aliases={};prepared=[];seen_targets=set()
    for number,item in enumerate(items,1):
        if not isinstance(item,dict):raise ValueError(f'objects[{number-1}] must be an object.')
        typ=item.get('object_type');content=item.get('content');existing_ref=item.get('object_ref')
        if typ not in allowed:raise ValueError(f'{typ!r} is not a declared write type for this Run. Allowed: {", ".join(sorted(allowed)) or "none"}')
        if typ in SPECIALIZED_TYPES:raise ValueError(f'{typ} uses a specialized supported interface. {SPECIALIZED_TYPES[typ]}')
        if not isinstance(content,dict):raise ValueError(f'objects[{number-1}].content must contain the AI-authored semantic fields.')
        forbidden=sorted(MECHANICAL_FIELDS & set(content))
        if forbidden:raise ValueError('Mechanical fields belong to AURA, not content: '+', '.join(forbidden))
        key=item.get('key') or existing_ref
        if not isinstance(key,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',key):
            raise ValueError(f'objects[{number-1}] requires a simple unique key (letters/numbers/_/-).')
        if key in aliases:raise ValueError(f'Duplicate local result key: {key}')
        if existing_ref:
            if existing_ref not in index:raise ValueError(f'Unknown canonical object_ref for update: {existing_ref}')
            existing,path=index[existing_ref]
            if existing.get('object_type')!=typ:raise ValueError(f'object_ref {existing_ref} is {existing.get("object_type")}, not {typ}.')
            try:stored=json.loads(Path(path).read_text())
            except Exception as exc:raise ValueError(f'Cannot read canonical update target {existing_ref}: {exc}')
            if not isinstance(stored,dict) or stored.get('id')!=existing_ref:
                raise ValueError(f'Canonical update target {existing_ref} is not stored as one independently writable object; use its owning specialized interface.')
            oid=existing_ref
        else:
            existing={};oid=_new_id(typ,bid,known_ids);path=None;known_ids.add(oid)
        if oid in seen_targets:raise ValueError(f'Canonical object is targeted more than once in one input: {oid}')
        seen_targets.add(oid);aliases[key]=oid
        prepared.append({'item':item,'type':typ,'content':content,'existing':existing,'path':path,'id':oid,'key':key})

    ts=now();objects=[]
    for row in prepared:
        item=row['item'];typ=row['type'];existing=row['existing'];content=_resolve_local(row['content'],aliases)
        lineage=_resolve_local(item.get('lineage_refs',[]),aliases)
        if not isinstance(lineage,list) or not all(isinstance(x,str) and x for x in lineage):
            raise ValueError(f'{row["key"]} lineage_refs must be a list of canonical refs or @local keys.')
        obj=dict(existing);old_extensions=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        supplied_extensions=content.pop('extensions',{})
        if not isinstance(supplied_extensions,dict):raise ValueError(f'{row["key"]} content.extensions must be an object when supplied.')
        supplied_bos=supplied_extensions.get('businessos') if isinstance(supplied_extensions.get('businessos'),dict) else {}
        protected=sorted(MECHANICAL_PROVENANCE_FIELDS & set(supplied_bos))
        if protected:raise ValueError(f'{row["key"]} extensions.businessos contains AURA-owned provenance fields: '+', '.join(protected))
        obj.update(content)
        obj.update({
            'id':row['id'],'object_type':typ,'schema_version':existing.get('schema_version','1.0.0'),
            'business_id':bid,'created_at':existing.get('created_at',ts),'updated_at':ts,
        })
        prior_lineage=existing.get('lineage') if isinstance(existing.get('lineage'),list) else []
        obj['lineage']=list(dict.fromkeys([*prior_lineage,*lineage,run_id]))
        obj['extensions']=_merge_extensions(old_extensions,supplied_extensions)
        _,schema=schema_entry(typ);properties=schema.get('properties') or {};owner=root.get('owner_system') or 'core'
        if 'owner_system' in properties and not obj.get('owner_system'):obj['owner_system']=owner
        if 'producer_system' in properties and not obj.get('producer_system'):obj['producer_system']=owner
        if 'requesting_system' in properties and not obj.get('requesting_system'):obj['requesting_system']=owner
        if 'observed_at' in properties and not obj.get('observed_at'):obj['observed_at']=ts
        chain=_contract_chain(typ,item,root,required)
        _stamp_provenance(obj,bid,run_id,root['id'],chain)
        validate_canonical(typ,obj);row['object']=obj;objects.append(obj)

    paths=[];snapshots={}
    try:
        for row,obj in zip(prepared,objects):
            path=Path(row['path']) if row['path'] else canonical_path(bid,obj)
            if path.exists():snapshots[path]=path.read_bytes()
            written=write_canonical(obj,path,allow_update=bool(row['existing']))
            paths.append(written);row['path']=written
        errors,warnings,counts=validate_business(bid,active_run_id=run_id)
        if errors:raise ValueError('Focused pre-finalization validation failed: '+'; '.join(errors[:12]))
    except Exception:
        for path in reversed(paths):
            if path in snapshots:write_json_atomic(path,json.loads(snapshots[path].decode('utf-8')))
            elif path.exists():path.unlink()
        raise
    return {
        'format_version':'1.0','status':'persisted','business_id':bid,'run_id':run_id,
        'objects':[{'key':row['key'],'id':row['id'],'object_type':row['type'],'operation':'updated' if row['existing'] else 'created','path':storage_ref(row['path'])} for row in prepared],
        'pre_finalization_validation':{
            'status':'clean','error_count':0,'warning_count':len(warnings),'warnings':warnings[:5],
            'canonical_object_counts':counts,
            'deferred_integrity_conditions':['active Run completion status','final completion-evidence recording'],
        },
        'next':{'interface':'scripts/finalize_run.py','command':f'python3 scripts/finalize_run.py {bid} {run_id}'},
        'semantic_boundary':'Only caller-supplied business meaning was persisted; AURA supplied mechanical canonical wrapping and validation.',
    }


def main():
    ap=argparse.ArgumentParser(description='Persist AI-authored semantic Run results through canonical schema/storage/provenance mechanics.')
    ap.add_argument('business_id');ap.add_argument('run_id');ap.add_argument('--input',required=True,help='JSON file in the Run work directory using the compact handoff input_shape')
    ap.add_argument('--workspace',help='Optional organization workspace root')
    args=ap.parse_args()
    try:
        payload=json.loads(Path(args.input).read_text(encoding='utf-8'))
        result=persist_run_results(args.business_id,args.run_id,payload,args.workspace)
    except (ValueError,FileExistsError,json.JSONDecodeError,OSError) as exc:
        result={'format_version':'1.0','status':'invalid_or_incomplete_result','category':'semantic_content_or_canonical_validation','reason':str(exc),'mutation':'rolled_back_or_not_started'}
    print(json.dumps(result,indent=2,ensure_ascii=False))
    raise SystemExit(0 if result.get('status')=='persisted' else 2)


if __name__=='__main__':main()
