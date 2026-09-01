---
id: seo.diagnosis.detectors.backlink-gap
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
Find relevant authority relationships/assets competitors or the topic ecosystem have that the brand could legitimately earn.

## Business Outcome
Identify evidence-backed authority gaps that may justify useful work without optimizing for raw link volume or turning every competitor reference into an outreach task.

## Run When
Use when fresh relevant authority/link evidence exists and the user/model needs to diagnose an **authority / backlink gap**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Compare owned and relevant competitor/topic-ecosystem referring sources at the topic/page level.
2. [AI] Exclude spam, irrelevant, manipulative, or non-comparable sources and determine what value/context appears to explain each legitimate reference.
3. [AI] Decide whether the missing relationship points to an existing owned Asset/value proposition, a genuine prerequisite linkable-asset need, another acquisition method, or no worthwhile action.
4. [AI] Assess audience/business relevance, realistic attainability, reputational/compliance risk, and material resource cost without fabricating success probability.
5. [AI] Create/update an Authority Opportunity only when the evidence supports a legitimate, valuable, plausibly attainable intervention. Acquisition method remains a later model/user choice.
6. [HYBRID] Reject opportunities whose only mechanism is payment/manipulation contrary to actual platform/legal/organizational constraints.

## Verification
- Target relevance and legitimacy over raw link volume.
- Preserve outreach/source provenance and applicable opt-out/compliance constraints when relevant.
