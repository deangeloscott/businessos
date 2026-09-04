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
Identify the domains, pages, and entity types that materially compete for important search demand without maintaining a duplicate broad business-competitor profile.

## Business Outcome
Understand who or what is actually winning relevant search visibility so the organization can make better organic-discovery decisions.

## Run When
Use when search competitor discovery is needed to explain visibility, establish the competitive set for important demand, or identify material gaps.

## Process
1. [HYBRID] Select representative priority query clusters across the markets, devices, and search surfaces that materially matter. Scope the sample to the decision rather than collecting everything available.
2. [HYBRID] Record visible domains/pages and result types over enough representative queries to avoid one-query conclusions.
3. [HYBRID] Aggregate visibility across business-relevant demand and segment by topic, intent, market, or other dimensions only when they change the interpretation.
4. [AI] Distinguish vendors, publishers, marketplaces, communities, government sources, directories, aggregators, and other result roles. Not every visible domain is a business competitor.
5. [AI] Map search competitors to known canonical Competitor records when the same real entity appears, while preserving the specific organic-competition role and evidence.
6. [HYBRID] Preserve the queries/topics/assets that make each competitor materially relevant and identify only the patterns or gaps that could change a useful decision.

## Verification
- Competitive conclusions are based on representative demand rather than isolated queries.
- Search-result role and business-competitor identity remain distinct.
- Visibility is not treated as proof of revenue, authority, customer preference, or causal superiority.
- Create an Opportunity or other durable state only when that meaning is genuinely useful later; it is not required to complete discovery.
