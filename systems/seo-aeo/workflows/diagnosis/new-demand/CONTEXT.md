---
id: seo.diagnosis.new-demand
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
writes:
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- records topic intent evidence
---
# Emerging Demand

## Purpose
Determine whether newly observable or newly relevant demand represents a meaningful opportunity for the organization rather than noise, seasonality, or speculative interest.

## Business Outcome
Recognize useful changes in customer/search/answer demand early enough to respond when warranted without turning every new signal into content or a permanent priority.

## Run When
Use when current first-party, search, answer, trend, market, or business evidence suggests demand may be new, changing, or newly relevant to an audience, Offer, or valuable awareness pathway.

## Process
1. [HYBRID] Compare current OrganicDemandUnits and supporting evidence with prior observations, seasonality, known market changes, and relevant changes to the organization's audiences, Offers, products/services, geography, or Objectives.
2. [AI] Establish what is actually novel: new demand, increased/decreased demand, changed language or intent, a newly relevant business pathway, or merely newly observed data. Novelty and magnitude are separate questions.
3. [AI] Determine whether the demand is relevant to a real audience/Offer or a clearly useful awareness/decision pathway. Do not treat broad topic popularity as business relevance.
4. [AI] Check whether an existing Asset already satisfies the need and whether current visibility/capture is sufficient before proposing new production.
5. [HYBRID] Assess magnitude, persistence, confidence, business value, and available evidence without inventing search volume, revenue potential, or certainty. Use investigation depth proportionate to the potential decision and uncertainty.
6. [AI] Preserve an Opportunity only when a concrete missing/underperforming Asset or other intervention has a credible value pathway and enough evidence to justify attention.
7. [AI] For weak, speculative, or seasonal signals, preserve uncertainty and a future review intent only when forgetting the signal would reduce future quality. Any scheduled reevaluation belongs to the external runtime.

## Verification
- Novelty, magnitude, persistence, audience/Offer relevance, and business value remain distinct.
- A signal is not permanently promoted merely because it appeared once.
- New content or work is not required when existing assets already serve the demand sufficiently.
