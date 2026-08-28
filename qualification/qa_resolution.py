#!/usr/bin/env python3
"""Contract-resolved QA helpers for qualification.

Qualification identifies which QA contracts a customer-facing production Run actually
requires. Structural validity stays owned by the shared completion-evidence validator;
this module deliberately does not duplicate QA-record rules.
"""


def required_qa_contract_ids(run_audit,contracts,completion_spec,root_contract_id=None):
    out=[]
    for audit in run_audit or []:
        run=audit.get('run') or {}; manifest=audit.get('manifest') or {}
        if root_contract_id and run.get('contract_id')!=root_contract_id:continue
        declared=manifest.get('required_subcontracts') or list((manifest.get('contracts') or {}).keys())
        for cid in declared:
            contract=contracts.get(cid)
            if not contract:continue
            if completion_spec(contract).get('profile')!='qa':continue
            if cid not in out:out.append(cid)
    return out


def recorded_required_qa_refs(run_audit,qa_contract_ids,root_contract_id=None):
    """Return recorded evidence refs for each required QA contract.

    Evidence content is validated elsewhere by subcontract_manifest_errors/validate_evidence.
    """
    out={cid:[] for cid in qa_contract_ids}
    for audit in run_audit or []:
        run=audit.get('run') or {}; manifest=audit.get('manifest') or {}
        if root_contract_id and run.get('contract_id')!=root_contract_id:continue
        contracts=manifest.get('contracts') or {}
        for cid in qa_contract_ids:
            entry=contracts.get(cid) or {}
            if entry.get('status')!='completed':continue
            refs=[x for x in (entry.get('evidence_refs') or []) if isinstance(x,str) and x.strip()]
            out[cid].extend(refs)
    return out


def structured_required_qa_refs(workspace,run_audit,qa_contract_ids):
    """Compatibility name used by evaluate_run; structure is validated by shared evidence rules."""
    return recorded_required_qa_refs(run_audit,qa_contract_ids)
