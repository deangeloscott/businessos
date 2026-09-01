---
id: seo.intelligence.organic-competition.page-analysis
type: playbook
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- Observation
- OrganicCompetitorState
- Competitor
writes:
- OrganicCompetitorState
- MetricObservation
- Observation
- Competitor
capabilities:
  required:
  - search.serp.read
  optional:
  - ai_answer.observe
  - backlink.read
  - research.web.read
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Competitor Page Analysis

## Purpose
Compare a specific competing page/asset against the owned or missing asset for a defined intent.

## Business Outcome
Improve valuable organic discovery through competitor page analysis, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring competitor intelligence when **competitor page analysis** is needed to explain competitive visibility or identify gaps.

## Process
1. [INTEGRATION] Retrieve the competing asset and record type, intent, audience, freshness, structure, entities, evidence, media, UX/CTA, internal/external references, and visible structured information.
2. [HYBRID] Observe which query/prompt/result context makes the page competitive.
3. [HYBRID] Compare against the owned target on usefulness, unique information, evidence, format, accessibility, conversion alignment, authority/context, and freshness.
4. [AI] Identify differentiators that explain user/search/answer usefulness without copying text or superficial word counts.
5. [AI] Classify gaps as content, evidence, format, technical, internal linking, authority, reputation, local, or offer/brand.
6. [HYBRID] Write page-level gap evidence into the relevant Opportunity.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


