---
id: seo.diagnosis.detectors.ranking-upside
type: detector
version: 1.1.0
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
- rank/visibility time series query-page mappings
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Ranking Upside Detector

## Purpose
Find pages already visible for valuable demand where a realistic relevance/quality/authority improvement could materially increase business value.

## Business Outcome
Detect and explain material ranking upside early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **ranking upside**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Select business-relevant query/page clusters with meaningful impressions/visibility and positions below likely high-click range.
2. [HYBRID] Prioritize by value-weighted demand and current conversion/offer fit, not raw volume.
3. [HYBRID] Inspect trend, SERP composition, intent match, ranking competitors, page quality, internal links, authority, technical state, and potential cannibalization.
4. [HYBRID] Estimate whether the page is structurally capable of improving or whether a different asset/intent strategy is needed.
5. [HYBRID] Create an Opportunity with root-cause hypotheses and expected incremental value range/confidence.
6. [HYBRID] Exclude queries where position is misleading due to location/personalization or where ranking higher would not help the business.

## Verification
- Separate demand, ranking, indexing, SERP-layout, seasonality and tracking effects before assigning a cause.


