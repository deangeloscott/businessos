#!/usr/bin/env python3
"""Validate optional Run receipts and conditional AURA playbook conformance.

A Run is useful continuity/provenance, not a prerequisite for doing or persisting work.
When organization state links to a Run, the receipt must be truthful and internally
consistent. Contract/subcontract rules apply only to Runs that explicitly claim an
AURA playbook method.
"""
from _common import *
from run_provenance import RUN_BOUND_TYPES
from completion_evidence import qa_record_ok, subcontract_manifest_errors, validate_evidence
import json

CUSTOMER_FACING_ROLE='customer_facing_production_root'
INTERNAL_MARKETING_ROLES={'internal_brief','internal_strategy','internal_analysis','internal_research','internal_planning'}


def _contract_index():
    try:return {c['id']:c for c in load_registry().get('contracts',[]) if c.get('id')}
    except Exception:return {}


def _method_type(run):
    return run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')


def _continuity_refs(run):
    continuity=run.get('continuity') if isinstance(run.get('continuity'),dict) else {}
    refs=set()
    for key in ('evidence_refs','result_refs','decision_refs'):
        refs.update(str(Path(x)) for x in (continuity.get(key) or []) if isinstance(x,str) and x.strip())
    return refs


def _load_run(rr):
    d=resolve_storage_ref(rr);rp=d/'run.json'
    if not d.exists() or not d.is_dir():return d,None,None,f'run_ref does not resolve to a Run directory: {rr}'
    if not rp.exists():return d,None,None,f'Run lacks run.json: {rr}'
    try:r=json.loads(rp.read_text())
    except Exception as e:return d,None,None,f'invalid Run state: {e}'
    mp=d/'contract-execution.json';m=None
    if mp.exists():
        try:m=json.loads(mp.read_text())
        except Exception as e:return d,r,None,f'invalid contract-execution state: {e}'
    return d,r,m,None


def _generic_run_errors(business_id,objects,contracts,active_run_id=None):
    errors=[]
    for obj,path in objects:
        typ=obj.get('object_type')
        if typ not in RUN_BOUND_TYPES:continue
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        rr=bos.get('run_ref')
        if not rr:continue
        _,r,m,problem=_load_run(rr)
        if problem:errors.append(f'{path} {typ} {problem}');continue
        if r.get('business_id')!=business_id:errors.append(f'{path} {typ} Run business_id mismatch: {rr}')
        rid=r.get('run_id')
        if bos.get('run_id') and bos.get('run_id')!=rid:errors.append(f'{path} {typ} extensions.businessos.run_id does not match referenced Run: {bos.get("run_id")!r} vs {rid!r}')
        method=_method_type(r)
        if bos.get('run_method_type') and bos.get('run_method_type')!=method:errors.append(f'{path} {typ} run_method_type does not match referenced Run: {bos.get("run_method_type")!r} vs {method!r}')
        expected_active=bool(active_run_id and rid==active_run_id and r.get('status')=='active')
        if not expected_active and r.get('status')!='completed':errors.append(f'{path} {typ} references a Run that is not completed: {rr}')
        if not expected_active and str(Path(path)) not in _continuity_refs(r):errors.append(f'{path} {typ} is not indexed by its completed Run work receipt: {rr}')
        if method!='aura_playbook':continue
        if not isinstance(m,dict):errors.append(f'{path} {typ} AURA playbook Run lacks contract-execution.json: {rr}');continue
        if m.get('business_id')!=business_id:errors.append(f'{path} {typ} contract-execution business_id mismatch: {rr}')
        root_id=m.get('root_contract_id')
        if not root_id or r.get('contract_id')!=root_id:errors.append(f'{path} {typ} Run root contract mismatch between run.json and contract-execution.json: {rr}')
        root=contracts.get(root_id)
        if not root:errors.append(f'{path} {typ} Run root contract is missing from the installed registry: {root_id!r}')
        else:
            owner=obj.get('owner_system');root_owner=root.get('owner_system')
            if owner and root_owner not in {None,'core',owner}:errors.append(f'{path} {typ} owner_system does not match linked AURA playbook owner: {owner} vs {root_owner}')
        if bos.get('run_contract_id') and bos.get('run_contract_id')!=root_id:errors.append(f'{path} {typ} run_contract_id does not match AURA playbook root: {bos.get("run_contract_id")!r} vs {root_id!r}')
        expected_aura_active=bool(expected_active and m.get('root_status')=='active')
        if not expected_aura_active and m.get('root_status')!='completed':errors.append(f'{path} {typ} AURA playbook contract execution is not completed: {rr}')
    return errors


def _semantic_aura_run_errors(business_id,objects,contracts):
    errors=[];seen=set()
    for obj,_ in objects:
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        rr=bos.get('run_ref')
        if not rr or rr in seen:continue
        seen.add(rr);_,r,m,problem=_load_run(rr)
        if problem or not r or _method_type(r)!='aura_playbook' or not isinstance(m,dict):continue
        if m.get('root_status')!='completed' or r.get('status')!='completed':continue
        root_id=m.get('root_contract_id');root=contracts.get(root_id);rid=r.get('run_id')
        if not root or not rid:continue
        sem=validate_evidence(root,m.get('root_evidence_refs') or [],business_id,rid,phase='root',manifest=m)
        errors.extend(f'{rr} completion evidence invalid for {root_id}: {e}' for e in sem)
        sub=subcontract_manifest_errors(m,business_id,rid,contracts)
        errors.extend(f'{rr} required subcontract evidence invalid: {e}' for e in sub)
    return errors


def _asset_run_errors(business_id,objects,contracts,active_run_id=None):
    errors=[]
    for asset,path in objects:
        if asset.get('object_type')!='Asset' or asset.get('owner_system') not in {'content-synthesis','marketing-synthesis'}:continue
        bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
        customer_facing=bos.get('customer_facing',True);rr=bos.get('run_ref')
        if asset.get('owner_system')=='marketing-synthesis' and customer_facing is False:
            role=str(asset.get('business_role') or '').strip().lower()
            if role not in INTERNAL_MARKETING_ROLES:errors.append(f'{path} marketing-synthesis Asset may set customer_facing=false only for an explicitly internal support role ({", ".join(sorted(INTERNAL_MARKETING_ROLES))}); an unpublished customer-facing draft remains customer-facing by intended use')
        if not rr:continue
        _,r,m,problem=_load_run(rr)
        if problem:errors.append(f'{path} Asset {problem}');continue
        if r.get('business_id')!=business_id:errors.append(f'{path} Run business_id mismatch: {rr}')
        rid=r.get('run_id');expected_active=bool(active_run_id and rid==active_run_id and r.get('status')=='active')
        if not expected_active and r.get('status')!='completed':errors.append(f'{path} production Asset references a Run that is not completed: {rr}')
        continuity_refs=_continuity_refs(r)
        if not expected_active and str(Path(path)) not in continuity_refs:errors.append(f'{path} production Asset is not indexed by its completed Run work receipt: {rr}')
        loc=asset.get('location_reference')
        if not expected_active and loc:
            try:locrel=str(Path(storage_ref(resolve_storage_ref(loc))))
            except Exception:locrel=str(Path(loc))
            if locrel not in continuity_refs:errors.append(f'{path} completed Run work receipt does not include Asset location result: {locrel}')
        if _method_type(r)!='aura_playbook':continue
        if not isinstance(m,dict):errors.append(f'{path} AURA playbook production Run lacks contract-execution.json: {rr}');continue
        expected_aura_active=bool(expected_active and m.get('root_status')=='active')
        root_id=m.get('root_contract_id')
        if not root_id or r.get('contract_id')!=root_id:errors.append(f'{path} Run root contract mismatch between run.json and contract-execution.json: {rr}')
        root=contracts.get(root_id)
        if not root:errors.append(f'{path} Run root contract is missing from the installed contract registry: {root_id!r}')
        else:
            if root.get('owner_system')!=asset.get('owner_system'):errors.append(f'{path} Asset owner_system does not match linked AURA playbook owner: {asset.get("owner_system")} vs {root.get("owner_system")}')
            if root.get('artifact_role')==CUSTOMER_FACING_ROLE and customer_facing is False:errors.append(f'{path} Asset produced under customer-facing production root {root_id!r} cannot opt out with customer_facing=false; draft/publication status does not change intended audience')
            if customer_facing is not False and root.get('artifact_role')!=CUSTOMER_FACING_ROLE:errors.append(f'{path} customer-facing Asset using an AURA playbook must reference a root marked artifact_role={CUSTOMER_FACING_ROLE}; got {root_id!r}')
        required=m.get('required_subcontracts',[]);steps=m.get('contracts',{})
        for cid in required:
            st=steps.get(cid,{})
            if st.get('status')!='completed' and not expected_aura_active:errors.append(f'{path} required subcontract not completed for AURA playbook Asset Run: {cid}')
            refs=st.get('evidence_refs') or []
            if not refs and (st.get('status')=='completed' or not expected_aura_active):errors.append(f'{path} completed subcontract lacks evidence refs: {cid}')
            for rel in refs:
                if not resolve_storage_ref(rel).exists():errors.append(f'{path} subcontract evidence ref missing: {cid} -> {rel}')
            if ('.qa' in cid or cid.endswith('.qa')) and (st.get('status')=='completed' or not expected_aura_active) and not qa_record_ok(cid,refs,business_id,rid):errors.append(f'{path} QA subcontract lacks structured matching JSON pass evidence: {cid}')
        if not expected_aura_active and m.get('root_status')!='completed':errors.append(f'{path} AURA playbook production contract execution is not completed: {rr}')
        root_refs=m.get('root_evidence_refs') or []
        if not root_refs and not expected_aura_active:errors.append(f'{path} completed AURA playbook production Run lacks root deliverable evidence: {rr}')
        for rel in root_refs:
            if not resolve_storage_ref(rel).exists():errors.append(f'{path} root completion evidence ref missing: {rel}')
        if customer_facing is not False and loc:
            try:locrel=storage_ref(resolve_storage_ref(loc))
            except Exception:locrel=str(loc)
            if not expected_aura_active and str(Path(locrel)) not in {str(Path(x)) for x in root_refs}:errors.append(f'{path} AURA playbook root evidence does not include the customer-facing Asset file: {locrel}')
        chain=bos.get('contract_chain')
        if not isinstance(chain,list):errors.append(f'{path} AURA playbook production Asset requires extensions.businessos.contract_chain including the root and required subcontracts')
        else:
            if root_id and root_id not in chain:errors.append(f'{path} Asset contract_chain omits linked root contract: {root_id}')
            missing=[x for x in required if x not in chain]
            if missing:errors.append(f'{path} Asset contract_chain omits required subcontract(s): {", ".join(missing)}')
    return errors


def run_completion_errors(business_id,objects,active_run_id=None):
    contracts=_contract_index();errors=[]
    errors.extend(_generic_run_errors(business_id,objects,contracts,active_run_id))
    errors.extend(_semantic_aura_run_errors(business_id,objects,contracts))
    errors.extend(_asset_run_errors(business_id,objects,contracts,active_run_id))
    return errors
