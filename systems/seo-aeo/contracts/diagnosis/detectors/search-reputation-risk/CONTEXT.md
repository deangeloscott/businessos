---
id: seo.diagnosis.detector.search-reputation-risk
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
- review mention reputation response history
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Search Reputation Risk Detector

## Purpose
Detect reputation/review conditions that materially affect organic/local discovery or search-result trust, without owning broad sentiment/reputation management.

## Business Outcome
Detect and explain material search reputation risk early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **reputation gap**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Compare rating/review volume/recency/themes/response coverage and third-party profile accuracy by location/product/source.
2. [DETERMINISTIC] Join search/local/AI observations to identify where reputation is visible in the decision path.
3. [AI] Identify whether the issue is insufficient authentic review generation, response backlog, operational complaint pattern, inaccurate profile, or misinformation.
4. [HYBRID] Route operational root causes outside SEO when marketing cannot fix them.
5. [HYBRID] Create ethical reputation Opportunities with business impact evidence.
6. [HYBRID] Define downstream measurement of reputation and conversion effects, not review count alone.


