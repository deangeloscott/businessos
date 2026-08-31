---
id: seo.intelligence.organic-competition.gap-analysis
type: playbook
version: 1.1.0
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
# Competitive Gap Analysis

## Purpose
Convert competitor observations into specific, business-relevant opportunities rather than a list of things competitors have.

## Business Outcome
Improve valuable organic discovery through competitive gap analysis, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring competitor intelligence when **competitive gap analysis** is needed to explain competitive visibility or identify gaps.

## Process
1. [DETERMINISTIC] Join owned demand/assets/current performance with Business/Search/Answer competitor coverage.
2. [AI] Identify demand where competitors outperform, formats/assets the market repeatedly rewards, source/authority gaps, and underserved needs competitors also miss.
3. [HYBRID] Estimate whether the owned brand can credibly produce a better/different solution with business value.
4. [HYBRID] Reject imitation opportunities that lack audience/business fit or depend on prohibited tactics.
5. [HYBRID] Attach competitor evidence and expected pathway to each created Opportunity.
6. [HYBRID] Rank gaps by business relevance and leverage, not by competitor content volume alone.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


