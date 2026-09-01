---
id: seo.diagnosis.detectors.new-demand
type: detector
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
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.serp.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- records topic intent evidence
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# New Demand Detector

## Purpose
Detect newly observable or newly relevant demand with a credible business pathway.

## Business Outcome
Distinguish meaningful emerging demand from noisy/seasonal/speculative signals and identify a business-relevant response only when justified.

## Run When
Use when fresh demand observations exist and the user/model needs to diagnose **new demand**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Compare refreshed OrganicDemandUnits with prior evidence and relevant business/Offer changes.
2. [AI] Determine whether the demand is relevant to an audience/Offer or an explicitly valuable awareness pathway.
3. [AI] Check whether an existing Asset already satisfies the need and whether current visibility/capture is sufficient.
4. [HYBRID] Assess demand/value/confidence from observed first-party, search, answer, trend, or market evidence without inventing volume or business impact.
5. [AI] Create/update one deduplicated Opportunity only when a concrete missing/underperforming Asset or intervention has a credible value pathway and sufficient evidence.
6. [AI] For speculative/seasonal signals, preserve uncertainty and a future review intent only when useful. Any actual scheduled reevaluation belongs to the external runtime.

## Verification
- Novelty, demand magnitude, audience/Offer relevance, and business value remain distinct.
- Weak signals are not permanently promoted merely because they appeared once.
