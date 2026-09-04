#!/usr/bin/env python3
"""Persist optional organization-owned reusable Workflow knowledge.

A ProcessExtension may come from explicit organization-authored procedure or from
evidence-backed Learning worth preserving for future work. It is retrieval context,
not semantic authority, a permission boundary, an execution plan, or a product-version
contract.
"""
from pathlib import Path
import argparse,hashlib,json,re
from _common import *
from canonical_store import validate_canonical,write_canonical


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


def _validate_workflow_id(workflow_id):
    if not isinstance(workflow_id,str) or not workflow_id.strip():raise ValueError('workflow_id is required')
    workflow_id=workflow_id.strip()
    if workflow_id.startswith('custom.'):
        if not re.fullmatch(r'custom\.[a-z0-9][a-z0-9.-]*',workflow_id):raise ValueError('organization-local workflow_id must match custom.<name> using lowercase letters, numbers, dots, or hyphens')
    elif not _canonical_workflow(workflow_id):raise ValueError(f'workflow_id must identify an installed AURA Workflow or begin custom.: {workflow_id!r}')
    return workflow_id


def persist_extension(business_id,spec):
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':raise ValueError(resolved.get('reason') or 'Organization could not be resolved')
    bid=resolved['business_id']
    if not isinstance(spec,dict):raise ValueError('spec must be a JSON object')

    workflow_id=_validate_workflow_id(spec.get('workflow_id'));scope=spec.get('scope') or 'business';scope_ref=_validate_scope(scope,spec.get('scope_ref'))
    source_learning_refs=_validate_object_refs(bid,spec.get('source_learning_refs'),'source_learning_refs',object_type='Learning')
    source_refs=_validate_object_refs(bid,spec.get('source_refs'),'source_refs')

    title=str(spec.get('title') or '').strip();purpose=str(spec.get('purpose') or '').strip()
    instructions=[str(x).strip() for x in spec.get('instructions') or [] if str(x).strip()]
    verification=[str(x).strip() for x in spec.get('verification') or [] if str(x).strip()]
    if not title or not purpose or not instructions:raise ValueError('title, purpose, and at least one instruction are required')

    seed='|'.join([bid,workflow_id,scope,scope_ref or '']);oid='pex_'+hashlib.sha256(seed.encode()).hexdigest()[:20]
    path=ROOT/'instances'/bid/'learning'/'process-extensions'/f'{oid}.json';existing=json.loads(path.read_text()) if path.exists() else {};timestamp=now()
    obj={
        'id':oid,'object_type':'ProcessExtension','schema_version':'1.0.0','business_id':bid,
        'created_at':existing.get('created_at') or timestamp,'updated_at':timestamp,
        'workflow_id':workflow_id,'title':title,'purpose':purpose,
        'discovery_terms':list(dict.fromkeys(str(x).strip() for x in spec.get('discovery_terms') or [] if str(x).strip())),
        'status':spec.get('status') or 'active','scope':scope,'scope_ref':scope_ref,
        'applies_when':list(dict.fromkeys(str(x).strip() for x in spec.get('applies_when') or [] if str(x).strip())),
        'does_not_apply_when':list(dict.fromkeys(str(x).strip() for x in spec.get('does_not_apply_when') or [] if str(x).strip())),
        'instructions':instructions,'verification':verification,
        'source_learning_refs':source_learning_refs,'source_refs':source_refs,
        'evidence_refs':list(dict.fromkeys(str(x).strip() for x in spec.get('evidence_refs') or [] if str(x).strip())),
        'extensions':spec.get('extensions') or {},
    }
    validate_canonical('ProcessExtension',obj);written=write_canonical(obj,path,allow_update=path.exists());return obj,written


def main():
    parser=argparse.ArgumentParser(description='Persist optional organization-owned Workflow knowledge from explicit organizational instruction or evidence-backed Learning. Installed Workflow ids are augmented; custom.* ids define organization-local Workflows. This does not make the extension semantic or execution authority.')
    parser.add_argument('business_id');parser.add_argument('--spec-file',required=True);args=parser.parse_args()
    try:spec=json.loads(Path(args.spec_file).read_text(encoding='utf-8'));obj,path=persist_extension(args.business_id,spec)
    except (ValueError,FileExistsError,json.JSONDecodeError,OSError) as exc:raise SystemExit(str(exc))
    print(json.dumps({'process_extension_id':obj['id'],'path':storage_ref(path),'workflow_id':obj['workflow_id'],'status':obj['status']},indent=2))


if __name__=='__main__':main()
