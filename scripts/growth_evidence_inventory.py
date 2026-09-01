#!/usr/bin/env python3
"""Inventory recorded evidence relevant to broad growth and next-best-work decisions.

This helper reports structured organizational state so a capable model/human can judge
whether the evidence is sufficient for a particular decision. It is not a semantic gate,
tactic recommender, permission check, or proof that unrepresented evidence is absent.
"""
from _common import *
import argparse,json,collections

STRUCTURED_BASELINE_TYPES={'EconomicContext','MetricObservation','OutcomeEvaluation'}
RELATED_EVIDENCE_TYPES={
    'SourceRecord','Observation','Insight','Experiment','Learning','Opportunity',
    'BusinessClaim','CustomerJourney','Asset'
}
BASIC_CONTEXT_TYPES={'Business','Brand','Market','ProductService','Offer','Objective','AudienceSegment'}


def assess(business_id):
    base=ROOT/'instances'/business_id
    if not base.exists(): raise ValueError(f'Unknown business: {business_id}')
    counts=collections.Counter()
    for obj,_ in iter_instance_objects(business_id):
        typ=obj.get('object_type')
        if typ: counts[typ]+=1

    structured={t:counts[t] for t in sorted(STRUCTURED_BASELINE_TYPES)}
    related={t:counts[t] for t in sorted(RELATED_EVIDENCE_TYPES) if counts[t]}
    context={t:counts[t] for t in sorted(BASIC_CONTEXT_TYPES) if counts[t]}
    structured_count=sum(structured.values())

    if structured_count:
        baseline_state='present'
        reason=(
            'Structured economic/performance/outcome state is recorded. Its freshness, '
            'coverage, causal relevance, and sufficiency for this particular decision remain '
            'semantic judgments for the capable model/human.'
        )
    else:
        baseline_state='not_recorded'
        reason=(
            'No EconomicContext, MetricObservation, or OutcomeEvaluation objects are recorded. '
            'That is a representation/state fact only: it does not establish that usable '
            'first-party evidence is absent, and it does not block bounded useful work by itself.'
        )

    return {
        'business_id':business_id,
        'status':'evidence_inventory_ready',
        'mode':'advisory_evidence_inventory',
        'hard_gate':False,
        'decision_authority':'model_or_human',
        'structured_baseline_state':baseline_state,
        'structured_baseline_counts':structured,
        'related_evidence_counts':related,
        'business_context_counts':context,
        'recorded_object_counts':dict(sorted(counts.items())),
        'reason':reason,
        'guidance':[
            'Inspect and reuse the actual first-party evidence already available in organizational context before requesting more information.',
            'Do not infer "no usable evidence" merely because particular canonical metric/economic object types are absent.',
            'Judge evidence sufficiency relative to the specific decision and level of commitment, not against a universal completeness threshold.',
            'If one missing fact could materially change the next move, gather the smallest decisive gap; otherwise continue with useful bounded work and preserve uncertainty.',
            'External research may strengthen a selected hypothesis, but it should not be used to fabricate missing active-business facts.',
            'Unknown remains unknown; a bounded draft, analysis, prototype, or reversible test may still be useful when the available evidence supports it.'
        ],
        'recommended_next_step':None,
    }


def main():
    ap=argparse.ArgumentParser(description='Inventory recorded growth-relevant organizational evidence for model/human judgment.')
    ap.add_argument('business_id')
    a=ap.parse_args()
    try: out=assess(a.business_id)
    except ValueError as e: raise SystemExit(str(e))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
