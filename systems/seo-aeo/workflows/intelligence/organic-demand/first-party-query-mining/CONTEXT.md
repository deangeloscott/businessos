---
id: seo.intelligence.organic-demand.first-party-query-mining
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
# First-Party Query Mining

## Purpose
Mine actual search/site/customer language for opportunities that generic keyword tools may miss.

## Business Outcome
Improve valuable organic discovery through first-party query mining, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring demand research when the system must discover, classify, or update **first-party query mining** evidence.

## Process
1. [INTEGRATION] Retrieve search-performance queries, site-search terms, support/sales questions, chat/contact reasons, conversion query paths, and other consented first-party language.
2. [DETERMINISTIC] Normalize case/punctuation only where meaning is preserved and retain raw text/timestamps.
3. [AI] Classify brand/nonbrand, topic, intent, audience, awareness stage, market/language, current asset, and conversion/value signals.
4. [HYBRID] Detect rising/new queries, long-tail clusters, high-impression low-click queries, converting low-volume terms, and queries without a good destination.
5. [DETERMINISTIC] Join to existing OrganicDemandUnits and create new units for materially distinct needs.
6. [HYBRID] Prioritize observed business-relevant demand over speculative volume estimates.

## Decisions / Routing
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


