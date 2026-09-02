#!/usr/bin/env python3
"""Persist optional organization-owned reusable Workflow knowledge.

A ProcessExtension may come from an explicit organization-authored procedure or from
strong evidence-backed Learning worth preserving for future work. It is retrieval context,
not semantic authority, a permission boundary, or an execution plan.
"""
from pathlib import Path
import argparse,hashlib,json,re
from _common import *
from canonical_store import INSTANCE_PATHS,validate_canonical,write_canonical


def _canonical_workflow(workflow_id):
    for path in workflow_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        if meta.get('id')==workflow_id and meta.get('type')=='workflow':return meta
    return None


def _validate_object_refs(business_id,refs,label,required=False,object_type=None):
    refs=list(dict.fromkeys(refs or []))
    if required and not refs:raise ValueError(f'{label} requires at least one organization-owned reference')
    index=object_index(business_id);missing=[ref for ref in refs if ref not in index]
    if missing:raise ValueError(f'Unknown {label} reference(s): '+', '.join(missing))
    if object_type:
        wrong=[ref for ref in refs if index[ref][0].get('object_type')!=object_type]
        if wrong:raise ValueError(f'{label} reference(s) must point to {object_type}: '+', '.join(wrong))
    return refs


def _validate_scope(scope,scope_ref):
    if scope=='business':
        if scope_ref not in (None,''):raise ValueError('business-scoped operating knowledge must not set scope_ref')
        return None
    if scope not in {'team','role','operator'}:raise ValueError(f'Unsupported scope: {scope!r}')
    if not isinstance(scope_ref,str) or not scope_ref.strip():raise ValueError(f'{scope}-scoped operating knowledge requires scope_ref')
    return scope_ref.strip()


def _validate_method_metadata(reads,writes):
    valid_types=set(INSTANCE_PATHS)
    unknown_reads=sorted(set(reads)-valid_types);unknown_writes=sorted(set(writes)-valid_types)
    if unknown_reads:raise ValueError('Unknown canonical read type(s): '+', '.join(unknown_reads))
    if unknown_writes:raise ValueError('Unknown canonical write type(s): '+', '.join(unknown_writes))


def persist_extension(business_id,spec):
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':raise ValueError(resolved.get('reason') or 'Organization could not be resolved')
    bid=resolved['business_id']
    if not isinstance(spec,dict):raise ValueError('spec must be a JSON object')

    mode=spec.get('mode') or 'local_workflow';owner=spec.get('owner_system') or 'core';scope=spec.get('scope') or 'business';scope_ref=_validate_scope(scope,spec.get('scope_ref'))
    source_learning_refs=list(dict.fromkeys(spec.get('source_learning_refs') or []));source_kind=spec.get('source_kind') or ('learning_evolved' if source_learning_refs else 'organization_authored')
    if source_kind=='learning_evolved':
        source_learning_refs=_validate_object_refs(bid,source_learning_refs,'source_learning_refs',required=True,object_type='Learning')
        source_refs=_validate_object_refs(bid,spec.get('source_refs'),'source_refs')
    elif source_kind=='organization_authored':
        source_learning_refs=[]
        source_refs=_validate_object_refs(bid,spec.get('source_refs'),'source_refs',required=True)
    else:raise ValueError(f'Unsupported ProcessExtension source_kind: {source_kind!r}')

    target=spec.get('target_workflow_id');local_id=spec.get('local_workflow_id')
    if mode=='augment_workflow':
        if not _canonical_workflow(target):raise ValueError(f'augment_workflow requires an installed target Workflow id: {target!r}')
        local_id=None
    elif mode=='local_workflow':
        if not isinstance(local_id,str) or not re.fullmatch(r'custom\.[a-z0-9][a-z0-9.-]*',local_id):raise ValueError('local_workflow requires local_workflow_id beginning custom.')
        target=None
    else:raise ValueError(f'Unsupported ProcessExtension mode: {mode!r}')

    title=str(spec.get('title') or '').strip();purpose=str(spec.get('purpose') or '').strip();instructions=[str(x).strip() for x in spec.get('instructions') or [] if str(x).strip()];verification=[str(x).strip() for x in spec.get('verification') or [] if str(x).strip()]
    if not title or not purpose or not instructions or not verification:raise ValueError('title, purpose, at least one instruction, and at least one verification item are required')
    reads=list(dict.fromkeys(spec.get('reads') or []));writes=list(dict.fromkeys(spec.get('writes') or []));_validate_method_metadata(reads,writes)

    seed='|'.join([bid,mode,target or '',local_id or '',scope,scope_ref or '']);oid='pex_'+hashlib.sha256(seed.encode()).hexdigest()[:20]
    path=ROOT/'instances'/bid/'learning'/'process-extensions'/f'{oid}.json';existing=json.loads(path.read_text()) if path.exists() else {};timestamp=now()
    obj={
        'id':oid,'object_type':'ProcessExtension','schema_version':'1.0.0','business_id':bid,
        'created_at':existing.get('created_at') or timestamp,'updated_at':timestamp,
        'mode':mode,'owner_system':owner,'target_workflow_id':target,'local_workflow_id':local_id,
        'title':title,'purpose':purpose,'discovery_terms':list(dict.fromkeys(spec.get('discovery_terms') or [])),
        'status':spec.get('status') or 'active','scope':scope,'scope_ref':scope_ref,
        'applies_when':list(dict.fromkeys(spec.get('applies_when') or [])),'does_not_apply_when':list(dict.fromkeys(spec.get('does_not_apply_when') or [])),
        'reads':reads,'writes':writes,'instructions':instructions,'verification':verification,
        'source_kind':source_kind,'source_learning_refs':source_learning_refs,'source_refs':source_refs,
        'evidence_refs':list(dict.fromkeys(spec.get('evidence_refs') or [])),'compatibility':spec.get('compatibility') or {'aura_min':os_version(),'aura_max':None},'extensions':spec.get('extensions') or {},
    }
    validate_canonical('ProcessExtension',obj);written=write_canonical(obj,path,allow_update=path.exists());return obj,written


def main():
    parser=argparse.ArgumentParser(description='Persist optional organization-owned local Workflow knowledge from explicit organizational instruction or evidence-backed Learning. This does not make the extension semantic or execution authority.')
    parser.add_argument('business_id');parser.add_argument('--spec-file',required=True);args=parser.parse_args()
    try:spec=json.loads(Path(args.spec_file).read_text(encoding='utf-8'));obj,path=persist_extension(args.business_id,spec)
    except (ValueError,FileExistsError,json.JSONDecodeError,OSError) as exc:raise SystemExit(str(exc))
    print(json.dumps({'process_extension_id':obj['id'],'path':storage_ref(path),'mode':obj['mode'],'status':obj['status'],'source_kind':obj['source_kind']},indent=2))

if __name__=='__main__':main()
