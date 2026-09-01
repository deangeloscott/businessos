---
id: seo.diagnosis.detectors.cannibalization
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
# Cannibalization / Intent Ownership Detector

## Purpose
Find multiple owned assets competing/confusing intent ownership where consolidation or differentiation may improve outcomes.

## Business Outcome
Detect and explain material cannibalization / intent ownership early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **cannibalization / intent ownership**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [AI] Group queries/prompts/topics by multiple ranking/cited/target owned URLs and analyze switching over time.
2. [HYBRID] Compare actual intent, audience, page type, offer, canonical/internal links, and conversion purpose of the candidate assets.
3. [HYBRID] Distinguish legitimate multiple results or distinct sub-intents from harmful duplication.
4. [AI] Assess whether merge, redirect, canonical alignment, internal-link clarification, retargeting, or content differentiation is appropriate.
5. [HYBRID] Create one Opportunity spanning all affected assets and preserve redirect/content history.
6. [HYBRID] Define downstream measurement at the combined topic/cluster level rather than judging only the surviving URL.


