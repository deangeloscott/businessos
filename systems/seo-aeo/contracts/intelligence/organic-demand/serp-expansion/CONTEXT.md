---
id: seo.intelligence.organic-demand.serp-expansion
type: playbook
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- OrganicDemandUnit
- Observation
- OrganicCompetitorState
- Competitor
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
# Search Result Expansion

## Purpose
Use observed search-result ecosystems to discover adjacent queries, intents, entities, result formats, and competitors.

## Business Outcome
Improve valuable organic discovery through search result expansion, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring demand research when the system must discover, classify, or update **search result expansion** evidence.

## Process
1. [HYBRID] Select representative seed queries by business value/cluster and observe configured search surfaces/markets.
2. [HYBRID] Capture result types, ranking/cited domains, page types, related questions/searches where observable, local/product/video/image features, and query reformulations.
3. [HYBRID] Extract recurring entities, subtopics, comparison dimensions, and intent shifts from the result set.
4. [INTEGRATION] Distinguish true customer-demand evidence from publisher SEO patterns or unrelated broad matches.
5. [AI] Map newly discovered demand into existing clusters or create candidate OrganicDemandUnits.
6. [DETERMINISTIC] Record timestamp/market/device because result ecosystems can change.

## Decisions / Routing
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


