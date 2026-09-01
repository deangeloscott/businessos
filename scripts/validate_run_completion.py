#!/usr/bin/env python3
"""Validate optional AURA work receipts without turning them into an execution gate.

A Run is continuity only. Validation checks identity, method provenance, resolvable refs,
and truthful indexing after completion. It does not require a Run for valid work and does
not certify subcontract execution, QA, provider state, permissions, launch readiness, or
business outcomes.
"""
from pathlib import Path
import json
from jsonschema import Draft202012Validator

from _common import *

INTERNAL_MARKETING_ROLES={'internal_brief','internal_strategy','internal_analysis','internal_research','internal_planning'}


def _contracts():
    try:return {c['id']:c for c in load_registry().get('contracts',[]) if c.get('id')}
    except Exception:return {}


def _method_type(run):return run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')


def _continuity_refs(run):
    continuity=run.get('continuity') if isinstance(run.get('continuity'),dict) else {}
    refs=set()
    for key in ('evidence_refs','result_refs','decision_refs'):
        refs.update(str(Path(x)) for x in (continuity.get(key) or []) if isinstance(x,str) and x.strip())
    return refs


def _load_run(rr):
    d=resolve_storage_ref(rr);rp=d/'run.json'
    if not d.exists() or not d.is_dir():return d,None,f'run_ref does not resolve to a Run directory: {rr}'
    if not rp.exists():return d,None,f'Run lacks run.json: {rr}'
    try:r=json.loads(rp.read_text())
    except Exception as e:return d,None,f'invalid Run state: {e}'
    return d,r,None


def _run_files_errors(business_id,contracts):
    errors=[];root=runtime_root()/'runs'/business_id
    if not root.exists():return errors
    schema=json.loads((PRODUCT_ROOT/'core/schemas/runtime/run.schema.json').read_text())
    for rp in sorted(root.glob('*/run.json')):
        try:r=json.loads(rp.read_text())
        except Exception as exc:
            errors.append(f'{storage_ref(rp)} invalid Run JSON: {exc}');continue
        for e in Draft202012Validator(schema).iter_errors(r):errors.append(f'{storage_ref(rp)} {list(e.path)}: {e.message}')
        if r.get('business_id')!=business_id:errors.append(f'{storage_ref(rp)} business_id mismatch')
        rd=rp.parent
        if (rd/'contract-execution.json').exists():errors.append(f'{storage_ref(rd)} contains retired contract-execution.json; Runs are receipts, not execution ledgers')
        if r.get('completion_policy_ref') is not None:errors.append(f'{storage_ref(rp)} contains retired completion_policy_ref')
        method=_method_type(r);cid=r.get('contract_id');mref=r.get('method_ref')
        if method=='aura_playbook':
            if not cid or cid not in contracts:errors.append(f'{storage_ref(rp)} aura_playbook Run references unavailable playbook {cid!r}')
            if mref not in {None,cid}:errors.append(f'{storage_ref(rp)} aura_playbook method_ref must equal contract_id')
        elif cid is not None:errors.append(f'{storage_ref(rp)} non-AURA Run must not carry contract_id')
        continuity=r.get('continuity') if isinstance(r.get('continuity'),dict) else {}
        if continuity:
            if continuity.get('purpose')!='organizational_work_receipt':errors.append(f'{storage_ref(rp)} continuity purpose is not organizational_work_receipt')
            if continuity.get('method_type') and continuity.get('method_type')!=method:errors.append(f'{storage_ref(rp)} continuity method_type does not match Run method_type')
            state=continuity.get('state')
            if r.get('status')=='completed' and state!='completed':errors.append(f'{storage_ref(rp)} completed Run must have continuity.state=completed')
            for key in ('evidence_refs','result_refs','decision_refs'):
                for ref in continuity.get(key) or []:
                    try:p=resolve_storage_ref(ref)
                    except Exception:
                        errors.append(f'{storage_ref(rp)} continuity {key} contains invalid ref {ref!r}');continue
                    if not p.exists() or not p.is_file():errors.append(f'{storage_ref(rp)} continuity {key} does not resolve: {ref}')
    return errors


def _object_receipt_errors(business_id,objects,contracts):
    errors=[]
    for obj,path in objects:
        typ=obj.get('object_type')
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}

        if typ=='Asset' and obj.get('owner_system')=='marketing-synthesis' and bos.get('customer_facing',True) is False:
            role=str(obj.get('business_role') or '').strip().lower()
            if role not in INTERNAL_MARKETING_ROLES:
                errors.append(f'{path} marketing-synthesis Asset may set customer_facing=false only for an explicitly internal support role ({", ".join(sorted(INTERNAL_MARKETING_ROLES))}); an unpublished customer-facing draft remains customer-facing by intended use')

        rr=bos.get('run_ref')
        if not rr:continue
        _,run,problem=_load_run(rr)
        if problem:errors.append(f'{path} {typ} {problem}');continue
        if run.get('business_id')!=business_id:errors.append(f'{path} {typ} Run business_id mismatch: {rr}')
        rid=run.get('run_id');method=_method_type(run)
        if bos.get('run_id') and bos.get('run_id')!=rid:errors.append(f'{path} {typ} extensions.businessos.run_id does not match referenced Run')
        if bos.get('run_method_type') and bos.get('run_method_type')!=method:errors.append(f'{path} {typ} run_method_type does not match referenced Run')
        if bos.get('run_method_ref') and bos.get('run_method_ref')!=(run.get('method_ref') or run.get('contract_id')):errors.append(f'{path} {typ} run_method_ref does not match referenced Run')
        if method=='aura_playbook':
            cid=run.get('contract_id')
            if cid not in contracts:errors.append(f'{path} {typ} linked AURA playbook is unavailable: {cid!r}')
            if bos.get('run_contract_id') and bos.get('run_contract_id')!=cid:errors.append(f'{path} {typ} run_contract_id does not match linked playbook')

        # Active receipts never invalidate current organizational state. Once a receipt is
        # completed, however, anything that claims linkage to it must actually be indexed by
        # that receipt so the preserved continuity is truthful.
        if run.get('status')!='completed':continue
        refs=_continuity_refs(run);objref=str(Path(path))
        if objref not in refs:errors.append(f'{path} {typ} is linked to completed Run {rr} but is not indexed by its receipt')
        if typ=='Asset' and isinstance(obj.get('location_reference'),str):
            try:locref=str(Path(storage_ref(resolve_storage_ref(obj['location_reference']))))
            except Exception:locref=str(Path(obj['location_reference']))
            if locref not in refs:errors.append(f'{path} Asset location is linked to completed Run {rr} but is not indexed by its receipt: {locref}')
    return errors


def run_completion_errors(business_id,objects,active_run_id=None):
    # active_run_id is intentionally ignored. Active receipts are allowed to coexist with
    # valid organizational state; the receipt is not a permission or completion gate.
    contracts=_contracts();errors=[]
    errors.extend(_run_files_errors(business_id,contracts))
    errors.extend(_object_receipt_errors(business_id,objects,contracts))
    return errors
