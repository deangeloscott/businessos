#!/usr/bin/env python3
"""Validate structural evidence/inference boundaries in canonical Opportunities.

This validator checks reference integrity and evidence typing. It deliberately does not
interpret Opportunity prose or decide whether natural-language reasoning is semantically
correct; that judgment belongs to the capable model/user applying the grounding policy.
"""
from _common import object_index
import argparse

STATUS_REQUIRES_BASIS={'qualified','prioritized','committed','active'}
MEASURED_TYPES={'MetricObservation','OutcomeEvaluation','ProofRecord','Observation','Insight'}


def _is_local_direct_observation(obj):
    if obj.get('object_type')!='Observation':return False
    ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
    le=ext.get('businessos_local_evidence') if isinstance(ext.get('businessos_local_evidence'),dict) else {}
    return bool(le)


def opportunity_grounding_errors(business_id,objects=None):
    idx=object_index(business_id);errors=[];warnings=[]
    if objects is None:opportunities=[(obj,path) for obj,path in idx.values() if obj.get('object_type')=='Opportunity']
    else:opportunities=[(obj,path) for obj,path in objects if obj.get('object_type')=='Opportunity']
    for op,path in opportunities:
        oid=op.get('id','<opportunity>');basis=op.get('reasoning_basis') if isinstance(op.get('reasoning_basis'),dict) else None
        if op.get('status') in STATUS_REQUIRES_BASIS and not basis:
            errors.append(f'{oid} {op.get("status")} Opportunity requires reasoning_basis separating fact_refs, measured_refs, inferences, and unknowns')
            continue
        if not basis:continue
        fact_refs=basis.get('fact_refs') if isinstance(basis.get('fact_refs'),list) else []
        measured_refs=basis.get('measured_refs') if isinstance(basis.get('measured_refs'),list) else []
        all_basis=set(fact_refs)|set(measured_refs)
        for rid in sorted(all_basis):
            if rid not in idx:errors.append(f'{oid} reasoning_basis references missing canonical object {rid}')
        for inf in basis.get('inferences') or []:
            for rid in inf.get('basis_refs') or []:
                if rid not in idx:errors.append(f'{oid} inference references missing canonical object {rid}')
                elif rid not in all_basis:errors.append(f'{oid} inference basis_ref {rid} must also appear in reasoning_basis.fact_refs or measured_refs')
        for rid in measured_refs:
            if rid not in idx:continue
            obj=idx[rid][0]
            if obj.get('object_type') not in MEASURED_TYPES:
                errors.append(f'{oid} measured_ref {rid} is {obj.get("object_type")}, not outcome/performance evidence')
            elif _is_local_direct_observation(obj):
                errors.append(f'{oid} measured_ref {rid} is deterministic local-site configuration evidence, not measured outcome/performance evidence')
    return errors,warnings


def main():
    ap=argparse.ArgumentParser(description='Validate structural Opportunity grounding without interpreting natural-language semantics.')
    ap.add_argument('business_id');a=ap.parse_args();errors,warnings=opportunity_grounding_errors(a.business_id)
    print(f'business={a.business_id} opportunity_grounding_errors={len(errors)} warnings={len(warnings)}')
    for w in warnings:print('WARNING',w)
    for e in errors:print('ERROR',e)
    if errors:raise SystemExit(1)
    print('opportunity grounding validation passed')

if __name__=='__main__':main()
