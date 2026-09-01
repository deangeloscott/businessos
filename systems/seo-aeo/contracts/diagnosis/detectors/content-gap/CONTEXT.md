---
id: seo.diagnosis.detectors.content-gap
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
# Content / Information Gap Detector

## Purpose
Find high-value buyer needs or answer components not adequately served by an owned asset.

## Business Outcome
Detect and explain material content / information gap early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **content / information gap**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [DETERMINISTIC] Join Demand clusters, journey stages, competitor/answer-source coverage, owned asset inventory, support/sales questions, and performance.
2. [AI] Identify absent destinations, incomplete sections/evidence, obsolete information, or formats that users actually need.
3. [HYBRID] Check whether enhancing an existing asset is better than creating a new one to avoid fragmentation/cannibalization.
4. [HYBRID] Define the missing user outcome/information, not a target word count.
5. [HYBRID] Create a content/on-page Opportunity with business pathway and evidence.
6. [HYBRID] Reject content whose only justification is keyword volume without audience/business value.


