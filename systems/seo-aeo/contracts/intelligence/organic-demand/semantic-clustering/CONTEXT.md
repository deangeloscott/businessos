---
id: seo.intelligence.organic-demand.semantic-clustering
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
# Semantic Demand Clustering

## Purpose
Group demand by shared underlying need while preserving distinct intents that deserve separate assets.

## Business Outcome
Improve valuable organic discovery through semantic demand clustering, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring demand research when the system must discover, classify, or update **semantic demand clustering** evidence.

## Process
1. [HYBRID] Represent each OrganicDemandUnit with query/prompt text, entities, intent, audience, stage, market, result/answer overlap, and current target pages.
2. [HYBRID] Create candidate clusters using semantic similarity and observed result overlap where available.
3. [HYBRID] Split clusters when the same words imply distinct tasks, audiences, locations, comparison contexts, or conversion destinations.
4. [HYBRID] Merge superficial wording variants when one strong asset can satisfy them without awkward keyword-specific sections.
5. [HYBRID] Name cluster/topic/entity hierarchy in customer-understandable language and retain member units.
6. [AI] Map clusters to owned assets, missing assets, and competitor coverage for Opportunity generation.

## Decisions / Routing
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


