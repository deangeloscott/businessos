---
id: seo.diagnosis.detectors.traffic-decay
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
- traffic time series landing page dimensions conversion
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Organic Traffic Decay Detector

## Purpose
Separate traffic decline into demand, visibility, CTR, analytics, conversion-path, and technical causes.

## Business Outcome
Detect and explain material organic traffic decay early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **organic traffic decay**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Detect material decline in qualified organic sessions/users/landing-page visits using configurable windows and seasonality controls.
2. [DETERMINISTIC] Validate analytics/data health first.
3. [HYBRID] Decompose traffic = available demand × visibility/position × click behavior × index/access factors at query/page/market level where possible.
4. [HYBRID] Check new/returning, device, geography, landing pages, branded/nonbrand, and conversion quality.
5. [AI] Classify primary contributors: demand decline, rank decline, CTR/SERP change, deindex/technical, tracking change, site migration, or unknown.
6. [HYBRID] Create targeted Opportunities/Incident rather than a generic traffic-recovery task.

## Verification
- Reconcile search visibility, analytics and conversion evidence before concluding the site lost demand or rank.


