---
id: seo.diagnosis.detectors.ranking-decay
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
# Ranking Decay Detector

## Purpose
Detect sustained loss of position/visibility for valuable demand and identify the likely scope.

## Business Outcome
Detect and explain material ranking decay early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **ranking decay**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Compare configurable recent/prior/YoY/rolling windows and retain query-page-market-device granularity.
2. [HYBRID] Require material value-weighted decline beyond normal volatility/provider noise.
3. [AI] Determine whether the drop is page-specific, cluster-wide, template/sitewide, market-specific, or competitor displacement.
4. [HYBRID] Check demand/intent/SERP changes, technical/index state, page changes, competitor changes, authority, freshness, cannibalization, and ecosystem updates.
5. [HYBRID] Create Opportunity or Incident based on severity/scope, with hypotheses ranked by evidence.
6. [AI] Do not automatically rewrite content until diagnosis identifies a plausible content cause.

## Verification
- Separate demand, ranking, indexing, SERP-layout, seasonality and tracking effects before assigning a cause.


