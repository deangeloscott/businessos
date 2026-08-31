---
id: seo.diagnosis.detectors.backlink-gap
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
- backlink/referring-domain/mention evidence and prospect records
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Authority / Backlink Gap Detector

## Purpose
Find relevant authority relationships/assets competitors or the topic ecosystem have that the brand can legitimately earn.

## Business Outcome
Detect and explain material authority / backlink gap early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **authority / backlink gap**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Compare owned and relevant competitor referring sources at topic/page level.
2. [DETERMINISTIC] Filter low-quality/spam/irrelevant sources and identify why each reference exists.
3. [HYBRID] Match source need to an owned value proposition/asset or create a prerequisite linkable-asset Opportunity.
4. [HYBRID] Estimate audience/business relevance, likelihood, reputational risk, and material cost.
5. [HYBRID] Create qualified Authority Opportunity routed by acquisition strategy.
6. [HYBRID] Do not create opportunities whose only plan is payment/manipulation contrary to system policy.

## Verification
- Target relevance and legitimacy over raw link volume; preserve outreach provenance and opt-out/compliance requirements.


