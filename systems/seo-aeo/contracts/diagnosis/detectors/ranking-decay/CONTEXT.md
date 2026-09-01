---
id: seo.diagnosis.detectors.ranking-decay
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
Detect sustained loss of position/visibility for valuable demand and identify the likely scope/mechanism.

## Business Outcome
Explain material ranking decay without assuming every fluctuation is actionable or automatically rewriting content.

## Run When
Use when fresh relevant visibility observations exist and the user/model needs to diagnose **ranking decay**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Compare appropriate recent/prior/YoY/rolling windows while retaining query-page-market-device context.
2. [HYBRID] Require material value-weighted decline beyond normal volatility and observable measurement noise.
3. [AI] Determine whether the decline is page-specific, cluster-wide, template/sitewide, market-specific, competitor displacement, or still unresolved.
4. [HYBRID] Evaluate demand/intent/SERP changes, technical/index state, page changes, competitor movement, authority, freshness, cannibalization, and relevant platform/industry evidence.
5. [AI] Create/update an Opportunity or Incident only when severity, business value, and a plausible intervention/root cause are sufficiently supported; otherwise preserve hypotheses/uncertainty.
6. [AI] Do not automatically rewrite content until diagnosis identifies a plausible content cause.

## Verification
- Separate demand, ranking, indexing, SERP-layout, seasonality, tracking effects, and causal hypotheses before assigning a cause.
