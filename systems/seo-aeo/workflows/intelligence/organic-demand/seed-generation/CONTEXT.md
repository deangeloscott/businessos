---
id: seo.intelligence.organic-demand.seed-generation
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- OrganicDemandUnit
writes:
- OrganicDemandUnit
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
Generate a broad but business-grounded starting set of topics, needs, questions, entities, and queries without mistaking model-generated possibilities for observed demand.

## Business Outcome
Give organic/search/answer research enough breadth to find valuable opportunities while filtering out obviously irrelevant demand before it creates research or content waste.

## Run When
Use when the organization needs an initial or expanded demand map and existing first-party, customer, market, or search evidence does not provide enough coverage by itself.

## Process
1. [HYBRID] Start from current Brand, Offers, audiences, problems, desired outcomes, objections, use cases, locations/markets, customer journey, and known competitors or alternatives where relevant.
2. [HYBRID] Reuse observed language from owned pages, reviews, testimonials, sales/support material, catalogs, site search, search-performance data, and other available first-party evidence before inventing new terminology.
3. [AI] Expand into plausible category terms, problems, desired outcomes, alternatives, comparisons, constraints, jobs-to-be-done, local modifiers, implementation questions, and post-purchase needs that could materially matter.
4. [AI] Keep observed customer language distinct from generated hypotheses and internal jargon. Preserve source/evidence when a term or need came from real users or market observations.
5. [AI] Associate useful seeds with audience, Offer or business pathway, tentative intent, market/language, and likely answer/asset type only where that context improves later decisions.
6. [AI] Remove or downweight clearly low-fit ideas early, but do not overfilter uncertain demand merely because it does not match an existing category. The model may preserve promising unknowns for further research.
7. [HYBRID] Persist materially useful OrganicDemandUnits when future work benefits; do not create one durable record for every generated keyword or wording variant.

## Verification
- Generated ideas and observed demand remain distinguishable.
- Breadth does not become exhaustive keyword enumeration for its own sake.
- Existing business categories do not artificially limit discovery of legitimate adjacent or emerging customer needs.
- Competitor research or Opportunity creation is optional, not a required next stage.
