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
Mine actual search, site, sales, support, and customer language for valuable needs and opportunities that generic keyword tools or model-generated ideas may miss.

## Business Outcome
Ground organic-demand decisions in what real users are already asking, searching, clicking, converting on, or struggling with so discovery work reflects the organization’s actual market rather than generic keyword assumptions.

## Run When
Use when consented first-party language or search-performance evidence is available and could reveal materially useful demand, intent, or customer wording.

## Process
1. [INTEGRATION] Retrieve relevant search-performance queries, site-search terms, support/sales questions, chat/contact reasons, conversion query paths, and other consented first-party language available to the active host.
2. [HYBRID] Preserve raw wording, timing, source, and important context. Normalize case, punctuation, or variants only where meaning is not lost.
3. [AI] Interpret brand/nonbrand context, topic, intent, audience, awareness stage, market/language, current destination, and available visibility/conversion/value signals at the depth useful for the decision.
4. [HYBRID] Look for patterns such as rising or newly appearing needs, long-tail clusters, high-impression low-click demand, converting low-volume terms, recurring customer questions, and demand without a good owned destination.
5. [AI] Distinguish observed demand from inference. A query appearing in first-party data is strong evidence that someone expressed the need, but volume, intent, and business value still require context.
6. [HYBRID] Reuse or update existing OrganicDemandUnits when that durable organization-level representation is useful; create new ones only for materially distinct needs rather than every phrase variation.
7. [AI] Prioritize observed business-relevant demand over speculative volume estimates while still allowing external research or model judgment to add context when it improves the decision.

## Verification
- Raw first-party evidence remains traceable when material.
- Query wording, inferred intent, visibility, conversion, and business value remain distinct.
- Low-volume observed demand may still be highly valuable; high-volume demand is not automatically important.
- Competitor research, Opportunity creation, or another Workflow is optional and used only when it helps the current work.
