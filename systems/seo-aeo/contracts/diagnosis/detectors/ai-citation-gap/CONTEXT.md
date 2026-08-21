---
id: seo.diagnosis.detectors.ai-citation-gap
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
- prompt/question observations, answer text, citations, mentions, and competing sources
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# AI Citation / Recommendation Gap Detector

## Purpose
Find high-value prompts where relevant competitors/sources appear but the brand is absent or poorly represented.

## Business Outcome
Detect and explain material ai citation / recommendation gap early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **ai citation / recommendation gap**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Select weighted prompt clusters and Answer Observations with stable-enough evidence.
2. [AI] Classify the gap separately: no mention, no recommendation, no citation, wrong cited URL, inaccurate facts, competitor dominance, or missing source type.
3. [DETERMINISTIC] Join underlying demand/business value, owned asset suitability, factual/evidence coverage, authority/reputation, and cited-source patterns.
4. [AI] Determine whether the legitimate intervention is content, evidence, technical/indexing, entity consistency, local/reputation, or earned third-party coverage.
5. [HYBRID] Create an AEO Opportunity with surface-specific evidence and no claim of guaranteed inclusion.
6. [HYBRID] Define the SEO re-observation sample, evaluation window, window, and success/guardrail metrics for any later intervention.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


