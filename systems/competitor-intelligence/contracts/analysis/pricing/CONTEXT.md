---
id: competitor.analysis.pricing
type: playbook
owner_system: competitor-intelligence
reads:
- Competitor
- type: Insight
  owner_system: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - review.read
  - crm.opportunity.read
  - social.observe
context:
- AudienceSegment
- Business
- EconomicContext
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - competitor.analysis.price-normalization
  conditional:
  - id: competitor.analysis.offer-comparison
    when: price differences cannot be interpreted without packaging, terms, or included value
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
3. [DETERMINISTIC] Normalize comparable units without erasing structurally different pricing models.
4. [HYBRID] Compare with prior snapshots and distinguish true change from localization, experiment/personalization, logged-in state, or temporary promotion.
5. [AI] Interpret likely strategic implications only after factual change is established.
6. [HYBRID] Cross-check customer/win-loss evidence before asserting price competitiveness or effectiveness.
7. [DETERMINISTIC] Update Competitor state/Observations and emit pricing change when material.
