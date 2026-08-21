---
id: seo.intelligence.organic-demand.intent-classification
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- SEOAssetState
- Asset
- MetricObservation
- OrganicDemandUnit
writes:
- OrganicDemandUnit
capabilities:
  required:
  - search.performance.read
  optional:
  - search.serp.read
  - ai_answer.observe
  - analytics.read
  - research.web.read
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
evidence_inputs:
- Market search answer evidence
- records topic intent evidence
updates:
  OrganicDemandUnit:
  - business_value
  - demand_evidence
---
# Intent and Journey Classification

## Purpose
Classify demand by what the user is trying to accomplish, not only by keyword syntax.

## Business Outcome
Improve valuable organic discovery through intent and journey classification, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring demand research when the system must discover, classify, or update **intent and journey classification** evidence.

## Process
1. [HYBRID] Review the query/prompt, observed results/answers, modifiers, related queries, and audience/business context.
2. [AI] Classify primary and secondary intent such as informational, commercial investigation, transactional, navigational, local, comparison, troubleshooting, or post-purchase.
3. [AI] Map awareness stage: unaware/problem-aware/solution-aware/product-aware/most-aware or the configured equivalent.
4. [AI] Map buyer journey role and desired next action; distinguish research that can legitimately lead to the brand from irrelevant informational traffic.
5. [HYBRID] Assign confidence and evidence; mark mixed/ambiguous intent rather than forcing one label.
6. [AI] Reclassify when observed SERPs/answers/conversion behavior materially contradict the prior label.

## Decisions / Routing
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


