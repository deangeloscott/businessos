#!/usr/bin/env python3
"""Persist explicitly organization-authored local operating knowledge.

This is the direct counterpart to Learning-driven playbook evolution. Use it when the
organization supplies or intentionally defines its own SOP/instructions. Do not create a
fake Learning merely to make the process recordable.
"""
from pathlib import Path
import argparse,hashlib,json
from _common import *
from canonical_store import validate_canonical,write_canonical,canonical_path


def _canonical_contract(contract_id):
    for path in contract_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        if meta.get('id')==contract_id:return meta
    return None


def _validate_sources(business_id,refs):
    refs=list(dict.fromkeys(refs or []))
    if not refs:raise ValueError('organization-authored operating knowledge requires at least one source_ref to organization-owned source material or decision state')
    idx=object_index(business_id);missing=[ref for ref in refs if ref not in idx]
    if missing:raise ValueError('Unknown organization source_ref(s): '+', '.join(missing))
    return refs


def _validate_scope(scope,scope_ref):
    if scope=='business':
        if scope_ref not in (None,''):raise ValueError('business-scoped operating knowledge must not set scope_ref')
        return None
    if scope not in {'team','role','operator'}:raise ValueError(f'Unsupported scope: {scope!r}')
    if not isinstance(scope_ref,str) or not scope_ref.strip():raise ValueError(f'{scope}-scoped operating knowledge requires scope_ref')
    return scope_ref.strip()


def persist_extension(business_id,spec):
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':raise ValueError(resolved.get('reason') or 'Organization could not be resolved')
    bid=resolved['business_id']
    if not isinstance(spec,dict):raise ValueError('spec must be a JSON object')
    mode=spec.get('mode') or 'local_playbook';owner=spec.get('owner_system') or 'core'
    if owner not in installed_modules():raise ValueError(f'owner_system is not installed: {owner}')
    source_refs=_validate_sources(bid,spec.get('source_refs'))
    scope=spec.get('scope') or 'business';scope_ref=_validate_scope(scope,spec.get('scope_ref'))
    target=spec.get('target_contract_id');local_id=spec.get('local_contract_id')
    if mode=='augment_contract':
        meta=_canonical_contract(target)
        if not meta:raise ValueError(f'augment_contract requires an installed target_contract_id: {target!r}')
        extra_writes=sorted(set(spec.get('writes') or [])-{selector_type(x) for x in meta.get('writes',[])})
        if extra_writes:raise ValueError('augment_contract may not introduce canonical write types outside its target playbook: '+', '.join(extra_writes))
        local_id=None
    elif mode=='local_playbook':
        if not isinstance(local_id,str) or not re.fullmatch(r'custom\.[a-z0-9][a-z0-9.-]*',local_id):raise ValueError('local_playbook requires local_contract_id beginning custom.')
        target=None
    else:raise ValueError(f'Unsupported ProcessExtension mode: {mode!r}')

    title=str(spec.get('title') or '').strip();purpose=str(spec.get('purpose') or '').strip()
    instructions=[str(x).strip() for x in spec.get('instructions') or [] if str(x).strip()]
    verification=[str(x).strip() for x in spec.get('verification') or [] if str(x).strip()]
    if not title or not purpose or not instructions or not verification:raise ValueError('title, purpose, at least one instruction, and at least one verification item are required')

    seed='|'.join([bid,mode,target or '',local_id or '',scope,scope_ref or '']);oid='pex_'+hashlib.sha256(seed.encode()).hexdigest()[:20]
    path=ROOT/'instances'/bid/'learning'/'process-extensions'/f'{oid}.json';existing=json.loads(path.read_text()) if path.exists() else {};ts=now()
    obj={
        'id':oid,'object_type':'ProcessExtension','schema_version':'1.0.0','business_id':bid,
        'created_at':existing.get('created_at') or ts,'updated_at':ts,
        'extension_version':spec.get('extension_version') or existing.get('extension_version') or '1.0.0',
        'mode':mode,'owner_system':owner,'target_contract_id':target,'local_contract_id':local_id,
        'title':title,'purpose':purpose,'route_terms':list(dict.fromkeys(spec.get('route_terms') or [])),
        'status':spec.get('status') or 'active','scope':scope,'scope_ref':scope_ref,'priority':int(spec.get('priority',100)),
        'applies_when':list(dict.fromkeys(spec.get('applies_when') or [])),
        'does_not_apply_when':list(dict.fromkeys(spec.get('does_not_apply_when') or [])),
        'reads':list(dict.fromkeys(spec.get('reads') or [])),'writes':list(dict.fromkeys(spec.get('writes') or [])),
        'required_capabilities':list(dict.fromkeys(spec.get('required_capabilities') or [])),
        'optional_capabilities':list(dict.fromkeys(spec.get('optional_capabilities') or [])),
        'instructions':instructions,'verification':verification,
        'source_kind':'organization_authored','source_learning_refs':[], 'source_refs':source_refs,
        'evidence_refs':list(dict.fromkeys(spec.get('evidence_refs') or [])),
        'compatibility':spec.get('compatibility') or {'aura_min':os_version(),'aura_max':None},
        'extensions':spec.get('extensions') or {},
    }
    validate_canonical('ProcessExtension',obj)
    written=write_canonical(obj,path,allow_update=path.exists())
    return obj,written


def main():
    p=argparse.ArgumentParser(description='Persist explicit organization-authored local SOP/instructions as AURA ProcessExtension without fabricating Learning.')
    p.add_argument('business_id');p.add_argument('--spec-file',required=True);a=p.parse_args()
    try:spec=json.loads(Path(a.spec_file).read_text(encoding='utf-8'));obj,path=persist_extension(a.business_id,spec)
    except (ValueError,FileExistsError,json.JSONDecodeError,OSError) as exc:raise SystemExit(str(exc))
    print(json.dumps({'process_extension_id':obj['id'],'path':storage_ref(path),'mode':obj['mode'],'status':obj['status'],'source_kind':obj['source_kind']},indent=2))

if __name__=='__main__':main()
