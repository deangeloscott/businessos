#!/usr/bin/env python3
"""Deterministic precheck for broad profitable-growth/next-best-work requests.

This does not choose a tactic. It tells the agent whether enough first-party
business evidence exists to responsibly rank intervention classes.
"""
from _common import *
import argparse,json,collections

FIRST_PARTY_DECISION_TYPES={'EconomicContext','MetricObservation','OutcomeEvaluation'}
BASIC_CONTEXT_TYPES={'Business','Market','ProductService','Objective','SourceRecord'}


def assess(business_id):
    base=ROOT/'instances'/business_id
    if not base.exists(): raise ValueError(f'Unknown business: {business_id}')
    counts=collections.Counter()
    for obj,_ in iter_instance_objects(business_id): counts[obj.get('object_type')]+=1
    first_party={t:counts[t] for t in sorted(FIRST_PARTY_DECISION_TYPES)}
    signal_count=sum(first_party.values())
    if signal_count==0:
        return {
          'business_id':business_id,
          'status':'baseline_required',
          'reason':'No first-party economic/performance/outcome observations are present, so BusinessOS cannot yet distinguish the main profitable-growth constraint classes responsibly.',
          'next_best_work':'Establish the smallest first-party profitable-growth baseline needed to distinguish acquisition, conversion, retention/repeat behavior, service economics/mix, capacity, or another material constraint.',
          'first_party_signal_counts':first_party,
          'baseline_guidance':[
            'Reuse connected/available first-party business data before asking the user.',
            'Collect only the smallest subset of lead/source volume and paid-source cost, funnel conversion, revenue/gross-profit/service economics, repeat/retention, or capacity data that can change which constraint class is most likely.',
            'Do not require every category if fewer facts are enough to distinguish the likely constraint.',
            'Do not substitute competitor, SEO, content, persona, or broad industry research for missing first-party business state.',
            'Translate the universal constraint classes into business-contextual questions, but include a domain-specific question only when its answer could materially change diagnosis/prioritization.',
            'Do not invent a user-time estimate for collecting the baseline; actual effort depends on connected systems, data availability, and user resources.'
          ],
          'research_gate':'External research may support a later selected opportunity, but should not be the default first move when missing first-party state is what prevents prioritization.',
          'implementation_gate':'If the user asked only what to do next, recommend/define this baseline work and stop; do not implement an unrelated tactic.'
        }
    return {
      'business_id':business_id,
      'status':'first_party_evidence_present',
      'reason':'At least one first-party economic/performance/outcome object exists. Use next-best-work reasoning to determine whether it is sufficient and current before gathering more.',
      'first_party_signal_counts':first_party,
      'next_best_work':None
    }


def main():
    ap=argparse.ArgumentParser(description='Precheck whether a business has enough first-party evidence to rank broad profitable-growth interventions. This is a gate, not a tactic recommender.')
    ap.add_argument('business_id')
    a=ap.parse_args()
    try: out=assess(a.business_id)
    except ValueError as e: raise SystemExit(str(e))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
