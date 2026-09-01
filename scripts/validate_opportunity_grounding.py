#!/usr/bin/env python3
"""Validate evidence -> inference -> unknown boundaries in canonical Opportunities."""
from _common import object_index, refs_in_object
import argparse, json, re

STATUS_REQUIRES_BASIS={'qualified','prioritized','committed','active'}
MEASURED_TYPES={'MetricObservation','OutcomeEvaluation','ProofRecord','Observation','Insight'}
ECONOMIC_METRIC_RE=re.compile(r'\b(revenue|profit|margin|contribution|lifetime value|ltv|deal value|order value|average ticket|lead value|customer value)\b',re.I)
ECONOMIC_CLAIM_PATTERNS=[
    re.compile(r'\b(highest[- ]value|most valuable|highest[- ]revenue|most profitable|highest[- ]margin|biggest revenue(?: driver)?|top revenue(?: driver)?)\b',re.I),
    re.compile(r'\bhigh[- ]value\s+(?:service|product|page|offer|customer|segment|lead)\b',re.I),
    re.compile(r'\bcore revenue\s+(?:page|service|product|offer)\b',re.I),
]
ABSOLUTE_OUTCOME_PATTERNS=[
    re.compile(r'\b(?:cannot|can\'t|will not|won\'t)\s+(?:rank|be indexed|index|be cited|be recommended|appear in (?:ai|search))\b',re.I),
    re.compile(r'\b(?:preventing|prevents|prevent)\b[^.!?]{0,90}\b(?:ranking|rankings|indexing|ai[- ]answer citations?|ai citations?)\b',re.I),
    re.compile(r'\binvisible to\b[^.!?]{0,80}\b(?:search engines?|ai(?: answer)? systems?)\b',re.I),
    re.compile(r'\bno\s+(?:search engine|ai(?: answer)? system)\s+can\s+(?:cite|use|discover|index)\b',re.I),
]
PERFORMANCE_RE=re.compile(
    r'\b(traffic|impressions?|clicks?|ctr|rankings?|organic visibility|leads?|conversions?|revenue|search volume|ai[- ]answer (?:mentions?|citations?|presence)|competitor visibility)\b'
    r'[^.!?]{0,70}\b(is|are|was|were|has|have|fell|fallen|dropped|declined|decreased|increased|grew|grown|low|high|down|up|missing|absent|poor|strong)\b',
    re.I,
)
QUALIFIER_RE=re.compile(r'\b(may|might|could|can potentially|likely|appears?|suggests?|risk|potential|hypothesis|inference|unmeasured|unknown|not measured|not observed|not verified|requires? measurement)\b',re.I)


def _walk_text(value):
    if isinstance(value,str):
        yield value
    elif isinstance(value,dict):
        for v in value.values(): yield from _walk_text(v)
    elif isinstance(value,list):
        for v in value: yield from _walk_text(v)


def _sentences(op):
    fields={k:op.get(k) for k in ('title','statement','diagnosis','expected_value','priority_assessment','constraints','domain_data') if k in op}
    text='\n'.join(_walk_text(fields))
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+',text) if s.strip()]


def _economic_support(refs,idx):
    for rid in refs:
        pair=idx.get(rid)
        if not pair: continue
        obj=pair[0]; typ=obj.get('object_type')
        if typ=='EconomicContext' and obj.get('metrics'):
            if ECONOMIC_METRIC_RE.search(json.dumps(obj.get('metrics'))): return True
        if typ=='BusinessClaim' and obj.get('authority') in {'explicit_user','verified_first_party'}:
            if ECONOMIC_METRIC_RE.search(obj.get('statement','')) or any(p.search(obj.get('statement','')) for p in ECONOMIC_CLAIM_PATTERNS): return True
        if typ=='MetricObservation':
            mref=obj.get('metric_ref'); mpair=idx.get(mref)
            if mpair and ECONOMIC_METRIC_RE.search(json.dumps(mpair[0])): return True
    return False


def _is_local_direct_observation(obj):
    if obj.get('object_type')!='Observation': return False
    ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
    le=ext.get('businessos_local_evidence') if isinstance(ext.get('businessos_local_evidence'),dict) else {}
    return bool(le)


def _has_measured_outcome_support(refs,idx):
    for rid in refs:
        pair=idx.get(rid)
        if not pair: continue
        obj=pair[0]; typ=obj.get('object_type')
        if typ not in MEASURED_TYPES: continue
        if typ=='Observation' and _is_local_direct_observation(obj):
            # deterministic website configuration is not measurement of search/AI/business performance
            continue
        return True
    return False


def opportunity_grounding_errors(business_id,objects=None):
    idx=object_index(business_id); errors=[]; warnings=[]
    opportunities=[]
    if objects is None:
        opportunities=[(obj,path) for obj,path in idx.values() if obj.get('object_type')=='Opportunity']
    else:
        opportunities=[(obj,path) for obj,path in objects if obj.get('object_type')=='Opportunity']
    for op,path in opportunities:
        oid=op.get('id','<opportunity>'); basis=op.get('reasoning_basis') if isinstance(op.get('reasoning_basis'),dict) else None
        if op.get('status') in STATUS_REQUIRES_BASIS and not basis:
            errors.append(f'{oid} {op.get("status")} Opportunity requires reasoning_basis separating fact_refs, measured_refs, inferences, and unknowns')
            continue
        if not basis: continue
        fact_refs=basis.get('fact_refs') if isinstance(basis.get('fact_refs'),list) else []
        measured_refs=basis.get('measured_refs') if isinstance(basis.get('measured_refs'),list) else []
        all_basis=set(fact_refs)|set(measured_refs)
        for rid in sorted(all_basis):
            if rid not in idx: errors.append(f'{oid} reasoning_basis references missing canonical object {rid}')
        for inf in basis.get('inferences') or []:
            for rid in inf.get('basis_refs') or []:
                if rid not in idx:
                    errors.append(f'{oid} inference references missing canonical object {rid}')
                elif rid not in all_basis:
                    errors.append(f'{oid} inference basis_ref {rid} must also appear in reasoning_basis.fact_refs or measured_refs')
        for rid in measured_refs:
            if rid not in idx: continue
            obj=idx[rid][0]
            if obj.get('object_type') not in MEASURED_TYPES:
                errors.append(f'{oid} measured_ref {rid} is {obj.get("object_type")}, not outcome/performance evidence')
            elif _is_local_direct_observation(obj):
                errors.append(f'{oid} measured_ref {rid} is deterministic local-site configuration evidence, not measured search/AI/business performance')
        refs=set(refs_in_object(op))|all_basis
        economic_supported=_economic_support(refs,idx)
        measured_supported=_has_measured_outcome_support(measured_refs,idx)
        for sent in _sentences(op):
            for pat in ECONOMIC_CLAIM_PATTERNS:
                if pat.search(sent) and not economic_supported:
                    errors.append(f'{oid} unsupported active-business economic/value assertion: {sent!r}; use business-specific economic evidence or remove the relative value claim')
                    break
            for pat in ABSOLUTE_OUTCOME_PATTERNS:
                if pat.search(sent):
                    errors.append(f'{oid} overstates an inferred search/AI outcome as certain: {sent!r}; rewrite as calibrated inference and preserve the unmeasured outcome as unknown')
                    break
            if PERFORMANCE_RE.search(sent) and not QUALIFIER_RE.search(sent) and not measured_supported:
                errors.append(f'{oid} states search/AI/business performance without measured outcome evidence: {sent!r}; add appropriate measured_refs or scope the claim as inference/unknown')
    return errors,warnings


def main():
    ap=argparse.ArgumentParser(description='Validate canonical Opportunity grounding and evidence/inference/unknown boundaries.')
    ap.add_argument('business_id'); a=ap.parse_args()
    errors,warnings=opportunity_grounding_errors(a.business_id)
    print(f'business={a.business_id} opportunity_grounding_errors={len(errors)} warnings={len(warnings)}')
    for w in warnings: print('WARNING',w)
    for e in errors: print('ERROR',e)
    if errors: raise SystemExit(1)
    print('opportunity grounding validation passed')

if __name__=='__main__': main()
