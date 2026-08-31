---
id: seo.intelligence.organic-demand.seed-generation
type: playbook
version: 1.1.0
owner_system: seo-aeo
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
# Demand Seed Generation

## Purpose
Generate an initial comprehensive but business-filtered set of topics, needs, questions, entities, and queries.

## Business Outcome
Improve valuable organic discovery through demand seed generation, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring demand research when the system must discover, classify, or update **demand seed generation** evidence.

## Process
1. [HYBRID] Traverse Brand Context: offers, audiences, awareness stages, problems, outcomes, objections, categories, use cases, locations, and competitors.
2. [HYBRID] Extract language from owned pages, reviews, testimonials, sales/support material, product/service catalogs, and internal site search where available.
3. [AI] Generate semantic expansions for category terms, problem terms, desired outcomes, alternatives, comparisons, constraints, local modifiers, jobs-to-be-done, and post-purchase questions.
4. [HYBRID] Separate customer language from internal jargon and preserve source/evidence for observed terms.
5. [AI] Map each seed to audience, offer/business goal, tentative intent, market/language, and expected answer/page type.
6. [HYBRID] Reject clearly low-fit topics early but retain a reason so rediscovery does not repeatedly recreate them.

## Decisions / Routing
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


