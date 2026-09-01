#!/usr/bin/env python3
"""Validate optional AURA work receipts without turning them into an execution gate.

A Run is continuity only. Validation checks identity, method provenance, resolvable refs,
and truthful indexing after completion. It does not require a Run for valid work and does
not certify QA, provider state, permissions, launch readiness, or business outcomes.
"""
from pathlib import Path
import json
from jsonschema import Draft202012Validator

from _common import *

INTERNAL_MARKETING_ROLES={'internal_brief','internal_strategy','internal_analysis','internal_research','internal_planning'}


def _contracts():
    out={}
    for path in contract_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        cid=meta.get('id')
        if isinstance(cid,str) and cid:out[cid]=meta
    return out


def _method_type(run):return run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')


def _continuity_refs(run):
    continuity=run.get('continuity') if isinstance(run.get('continuity'),dict) else {};refs=set()
    for key in ('evidence_refs','result_refs','decision_refs'):
        refs.update(str(Path(x)) for x in (continuity.get(key) or []) if isinstance(x,str) and x.strip())
    return refs


def _load_run(ref):
    directory=resolve_storage_ref(ref);path=directory/'run.json'
    if not directory.exists() or not directory.is_dir():return directory,None,f'run_ref does not resolve to a Run directory: {ref}'
    if not path.exists():return directory,None,f'Run lacks run.json: {ref}'
    try:run=json.loads(path.read_text())
    except Exception as exc:return directory,None,f'invalid Run state: {exc}'
    return directory,run,None


def _run_files_errors(business_id,contracts):
    errors=[];root=runtime_root()/'runs'/business_id
    if not root.exists():return errors
    schema=json.loads((PRODUCT_ROOT/'core/schemas/runtime/run.schema.json').read_text())
    for path in sorted(root.glob('*/run.json')):
        try:run=json.loads(path.read_text())
        except Exception as exc:errors.append(f'{storage_ref(path)} invalid Run JSON: {exc}');continue
        for error in Draft202012Validator(schema).iter_errors(run):errors.append(f'{storage_ref(path)} {list(error.path)}: {error.message}')
        if run.get('business_id')!=business_id:errors.append(f'{storage_ref(path)} business_id mismatch')
        directory=path.parent
        if (directory/'contract-execution.json').exists():errors.append(f'{storage_ref(directory)} contains retired contract-execution.json; Runs are receipts, not execution ledgers')
        method=_method_type(run);contract_id=run.get('contract_id');method_ref=run.get('method_ref')
        if method=='aura_playbook':
            if not contract_id or contract_id not in contracts:errors.append(f'{storage_ref(path)} aura_playbook Run references unavailable playbook {contract_id!r}')
            if method_ref not in {None,contract_id}:errors.append(f'{storage_ref(path)} aura_playbook method_ref must equal contract_id')
        elif contract_id is not None:errors.append(f'{storage_ref(path)} non-AURA Run must not carry contract_id')
        continuity=run.get('continuity') if isinstance(run.get('continuity'),dict) else {}
        if not continuity:continue
        if continuity.get('purpose')!='organizational_work_receipt':errors.append(f'{storage_ref(path)} continuity purpose is not organizational_work_receipt')
        if continuity.get('method_type') and continuity.get('method_type')!=method:errors.append(f'{storage_ref(path)} continuity method_type does not match Run method_type')
        if run.get('status')=='completed' and continuity.get('state')!='completed':errors.append(f'{storage_ref(path)} completed Run must have continuity.state=completed')
        for key in ('evidence_refs','result_refs','decision_refs'):
            for ref in continuity.get(key) or []:
                try:target=resolve_storage_ref(ref)
                except Exception:errors.append(f'{storage_ref(path)} continuity {key} contains invalid ref {ref!r}');continue
                if not target.exists() or not target.is_file():errors.append(f'{storage_ref(path)} continuity {key} does not resolve: {ref}')
    return errors


def _object_receipt_errors(business_id,objects,contracts):
    errors=[]
    for obj,path in objects:
        typ=obj.get('object_type');ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {};bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        if typ=='Asset' and obj.get('owner_system')=='marketing-synthesis' and bos.get('customer_facing',True) is False:
            role=str(obj.get('business_role') or '').strip().lower()
            if role not in INTERNAL_MARKETING_ROLES:errors.append(f'{path} marketing-synthesis Asset may set customer_facing=false only for an explicitly internal support role ({", ".join(sorted(INTERNAL_MARKETING_ROLES))}); an unpublished customer-facing draft remains customer-facing by intended use')

        run_ref=bos.get('run_ref')
        if not run_ref:continue
        _,run,problem=_load_run(run_ref)
        if problem:errors.append(f'{path} {typ} {problem}');continue
        if run.get('business_id')!=business_id:errors.append(f'{path} {typ} Run business_id mismatch: {run_ref}')
        run_id=run.get('run_id');method=_method_type(run)
        if bos.get('run_id') and bos.get('run_id')!=run_id:errors.append(f'{path} {typ} extensions.businessos.run_id does not match referenced Run')
        if bos.get('run_method_type') and bos.get('run_method_type')!=method:errors.append(f'{path} {typ} run_method_type does not match referenced Run')
        if bos.get('run_method_ref') and bos.get('run_method_ref')!=(run.get('method_ref') or run.get('contract_id')):errors.append(f'{path} {typ} run_method_ref does not match referenced Run')
        if method=='aura_playbook':
            contract_id=run.get('contract_id')
            if contract_id not in contracts:errors.append(f'{path} {typ} linked AURA playbook is unavailable: {contract_id!r}')
            if bos.get('run_contract_id') and bos.get('run_contract_id')!=contract_id:errors.append(f'{path} {typ} run_contract_id does not match linked playbook')

        # Active receipts never invalidate current organizational state. Completed receipts
        # must truthfully index any durable object/file that claims linkage to them.
        if run.get('status')!='completed':continue
        refs=_continuity_refs(run);object_ref=str(Path(path))
        if object_ref not in refs:errors.append(f'{path} {typ} is linked to completed Run {run_ref} but is not indexed by its receipt')
        if typ=='Asset' and isinstance(obj.get('location_reference'),str):
            try:location_ref=str(Path(storage_ref(resolve_storage_ref(obj['location_reference']))))
            except Exception:location_ref=str(Path(obj['location_reference']))
            if location_ref not in refs:errors.append(f'{path} Asset location is linked to completed Run {run_ref} but is not indexed by its receipt: {location_ref}')
    return errors


def run_completion_errors(business_id,objects):
    contracts=_contracts();return [*_run_files_errors(business_id,contracts),*_object_receipt_errors(business_id,objects,contracts)]
