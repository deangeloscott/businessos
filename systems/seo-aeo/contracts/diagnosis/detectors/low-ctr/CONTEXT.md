---
id: seo.diagnosis.detectors.low-ctr
type: detector
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
- Observation
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
- query-page impressions clicks CTR position SERP
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Low CTR / Search Presentation Detector

## Purpose
Find pages whose observed clicks are materially below an appropriate expectation for their visibility and intent.

## Business Outcome
Detect and explain material low ctr / search presentation early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **low ctr / search presentation**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [DETERMINISTIC] Join query-page impressions, clicks, CTR, position, device, market, brand/nonbrand, result features, and business value.
2. [HYBRID] Apply configurable initial rules (including user-supplied position/impression thresholds where configured), then prefer learned expected CTR curves once sufficient brand data exists.
3. [HYBRID] Flag statistically/materially meaningful underperformance rather than every below-average row.
4. [AI] Diagnose title/snippet relevance, result features/zero-click behavior, intent mismatch, brand familiarity, ratings/reviews, structured appearance, query-page mismatch, and competitor presentation.
5. [HYBRID] Create a presentation/content Opportunity only if the root cause is plausibly controllable.
6. [HYBRID] Define downstream measurement against matched position/query conditions so ranking movement is not mistaken for CTR-copy impact.

## Verification
- Compare CTR only against a relevant position/query/device/market expectation; do not mistake rank movement for presentation lift.
- Create an Opportunity only when the gap is material and plausibly controllable.


