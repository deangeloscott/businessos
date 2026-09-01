---
id: seo.diagnosis.detectors.low-ctr
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
Identify controllable search-presentation gaps without mistaking rank/result-layout movement or low-quality traffic for a copy problem.

## Run When
Use when fresh relevant CTR/search-result observations exist and the user/model needs to diagnose **low CTR / search presentation**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Relate query-page impressions, clicks, CTR, position, device, market, brand/nonbrand, result features, and business value. Exact joins are mechanical; comparability/value are model judgments.
2. [HYBRID] Apply useful initial rules and user-supplied thresholds where appropriate, then prefer learned expected CTR curves once sufficient comparable business evidence exists.
3. [HYBRID] Identify statistically/materially meaningful underperformance rather than every below-average row.
4. [AI] Diagnose title/snippet relevance, result features/zero-click behavior, intent mismatch, brand familiarity, ratings/reviews, structured appearance, query-page mismatch, and competitor presentation.
5. [AI] Create/update a presentation/content Opportunity only if the likely root cause is materially valuable and plausibly controllable.
6. [HYBRID] Define later evaluation against comparable position/query conditions so ranking movement is not mistaken for CTR-copy impact.

## Verification
- Compare CTR only against a relevant position/query/device/market expectation.
- Create an Opportunity only when the gap is material and plausibly controllable.
