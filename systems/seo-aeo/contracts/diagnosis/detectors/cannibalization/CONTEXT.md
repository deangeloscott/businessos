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
Find multiple owned assets competing or confusing intent ownership where consolidation or differentiation may improve outcomes.

## Business Outcome
Distinguish harmful ownership ambiguity from legitimate multiple-result coverage and identify a focused intervention only when the evidence supports it.

## Run When
Use when fresh relevant query/asset observations exist and the user/model needs to diagnose **cannibalization / intent ownership**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [AI] Group queries/prompts/topics with multiple ranking/cited/target owned URLs and inspect switching/overlap over time.
2. [HYBRID] Compare actual intent, audience, page type, Offer, canonical/internal links, and conversion purpose of candidate Assets.
3. [AI] Distinguish legitimate multiple results or distinct sub-intents from harmful duplication/ownership ambiguity.
4. [AI] Decide whether merge, redirect, canonical alignment, internal-link clarification, retargeting, content differentiation, or no change is most plausible.
5. [AI] Create/update one Opportunity spanning the materially affected Assets only when the evidence supports a controllable problem; preserve relevant redirect/content history.
6. [HYBRID] Define later evaluation at the combined topic/cluster level so success is not judged only by one surviving URL.

## Verification
- Query/topic similarity alone does not establish harmful cannibalization.
- A future change remains model/harness execution; this detector only preserves the diagnosis/Opportunity when useful.
