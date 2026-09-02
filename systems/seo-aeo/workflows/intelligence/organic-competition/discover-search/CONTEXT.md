---
id: seo.intelligence.organic-competition.discover-search
type: workflow
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
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Search Competitor Discovery

## Purpose
Identify/search-analyze organic competitors and answer sources without maintaining a duplicate broad business competitor profile.

## Business Outcome
Improve valuable organic discovery through search competitor discovery, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring competitor intelligence when **search competitor discovery** is needed to explain competitive visibility or identify gaps.

## Process
1. [HYBRID] Sample weighted priority query clusters across configured markets/devices/surfaces.
2. [DETERMINISTIC] Record ranking/result domains/pages and result types over enough queries to avoid one-query bias.
3. [HYBRID] Aggregate visibility/share across business-value-weighted demand and segment by topic/intent/market.
4. [INTEGRATION] Classify result entities such as vendors, publishers, marketplaces, communities, government, directories, or aggregators.
5. [AI] Map search competitors to known business competitors when applicable but retain separate type labels.
6. [HYBRID] Write competitor observations with the queries/topics/assets that make each domain relevant.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


