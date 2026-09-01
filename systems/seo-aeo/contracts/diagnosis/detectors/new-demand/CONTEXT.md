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
Detect and explain material new demand early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **new demand**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Compare refreshed OrganicDemandUnits against prior universe and business/offer changes.
2. [HYBRID] Require relevance to an audience/offer or explicitly strategic awareness pathway.
3. [HYBRID] Check whether an existing asset already satisfies the need and whether current visibility/capture is sufficient.
4. [HYBRID] Estimate demand/value/confidence from observed first-party, search, answer, trend, or market evidence.
5. [DETERMINISTIC] Create one deduplicated Opportunity with target/missing asset and evidence.
6. [HYBRID] Schedule reevaluation for speculative/seasonal units rather than permanently promoting weak signals.


