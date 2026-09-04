---
id: seo.intelligence.organic-demand.serp-expansion
type: workflow
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
Use observed search-result ecosystems to discover adjacent needs, intents, entities, formats, and competitors that seed research alone may miss.

## Business Outcome
Expand the organization's view of valuable search demand from what search surfaces actually expose while avoiding the assumption that every visible query, feature, or competitor pattern deserves pursuit.

## Run When
Use when observed search results can materially improve understanding of a demand cluster, reveal adjacent needs, or show how users and search surfaces frame the task.

## Process
1. [HYBRID] Select representative seed queries based on the business question and observe the markets, devices, and search surfaces that materially matter.
2. [HYBRID] Capture useful result context such as result types, visible domains/pages, related questions/searches where observable, local/product/video/image features, reformulations, and other patterns that may reveal user needs or discovery expectations.
3. [AI] Extract recurring entities, subtopics, comparison dimensions, constraints, and intent shifts that could materially change the demand model.
4. [AI] Distinguish evidence of customer/search demand from publisher SEO patterns, broad-match noise, and search-interface suggestions whose real demand or value remains uncertain.
5. [AI] Map materially distinct discoveries into existing demand clusters or preserve them as candidate OrganicDemandUnits when future work benefits. Do not create durable demand objects for every surfaced phrase.
6. [HYBRID] Preserve timestamp, market, device, and result context when those dimensions are needed to interpret or reproduce the observation.
7. [AI] Use competitor analysis, Opportunity creation, or another specialist method only when it improves the actual decision rather than as a required route.

## Verification
- Search-result features and related queries are treated as useful evidence, not unquestionable ground truth about volume or business value.
- Ranking and repeated result presence may be meaningful signals of exposure and market/discovery patterns while remaining distinct from proven downstream business outcomes.
- Newly discovered demand remains tied to a real user or business mechanism before it is prioritized.
