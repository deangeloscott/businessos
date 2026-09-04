---
id: competitor.analysis.pricing
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- type: Insight
  domain: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
context:
- AudienceSegment
- Business
- EconomicContext
- Market
- Objective
- Offer
- ProductService
---
# Pricing Intelligence

## Purpose
Track competitor price, pricing model, discount/commitment terms, and material pricing changes accurately.

## Business Outcome
Improve competitive decisions through evidence-backed pricing intelligence, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current pricing intelligence and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Retrieve authoritative pricing/plan/order pages and capture timestamp, market/currency, billing period, taxes/fees qualifiers, and access limitations.
2. [AI] Extract price points, units, tiers, minimums, usage dimensions, setup fees, discounts, enterprise/contact-sales ambiguity, and disclosed terms.
3. [DETERMINISTIC] Normalize comparable units without erasing structurally different pricing models. Draw on the dedicated price-normalization Workflow when its additional method detail materially helps.
4. [HYBRID] Compare with prior snapshots and distinguish true change from localization, experiment/personalization, logged-in state, or temporary promotion.
5. [AI] Interpret likely strategic implications only after factual change is established. Use offer-comparison knowledge when packaging, terms, or included value are necessary to interpret the price difference.
6. [HYBRID] Cross-check customer/win-loss evidence before asserting price competitiveness or effectiveness.
7. [HYBRID] Update current Competitor/Observation state and preserve a material pricing-change Insight only when that interpretation has durable organizational value. Do not create runtime event traffic merely because competitor pricing changed.
