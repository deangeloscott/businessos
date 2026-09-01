---
id: seo.intelligence.organic-competition.domain-analysis
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
# Competitor Domain Analysis

## Purpose
Build an interpretable domain-level model of how a competitor wins discovery and business attention.

## Business Outcome
Improve valuable organic discovery through competitor domain analysis, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring competitor intelligence when **competitor domain analysis** is needed to explain competitive visibility or identify gaps.

## Process
1. [HYBRID] Select a competitor because of actual overlap in business/search/answer opportunities.
2. [INTEGRATION] Inventory visible site sections, major page types, topic clusters, architecture, publishing patterns, local/market structure, and conversion/offers.
3. [DETERMINISTIC] Join search visibility, backlinks/mentions, answer citations, reputation/local state, freshness, and content patterns from available providers.
4. [AI] Identify concentrated strengths rather than reducing the domain to a synthetic authority score.
5. [AI] Separate observations from inferred strategy; cite representative pages/data.
6. [HYBRID] Write domain strengths, weaknesses, distinctive assets, and testable gaps relevant to owned opportunities.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


