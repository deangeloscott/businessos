---
id: competitor.analysis.price-normalization
type: playbook
version: 1.3.0
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - social.observe
  - review.read
  - search.observe
  - document.read
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Price Normalization

## Purpose
Convert observed competitor prices into comparable economic units without erasing meaningful packaging differences.

## Business Outcome
Enable valid price comparisons and change detection across non-identical offers.

## Run When
Run whenever competitor pricing must be compared across plans, time, currency, billing periods, usage, or bundled services.

## Process
1. [DETERMINISTIC] Capture listed price, currency, billing period, minimum commitment, unit/usage basis, quantity thresholds, promotion, and included entitlements.
2. [AI] Identify dimensions that make offers non-comparable, including implementation, service, support, limits, seats, quality, guarantees, and hidden/unknown fees.
3. [DETERMINISTIC] Convert currency/period/unit only when the conversion is legitimate and preserve original values.
4. [AI] Separate standard price from temporary promotion, negotiated/estimated price, free tier, and contact-sales unknowns.
5. [HYBRID] Refuse a single normalized number when materially different value/terms would make it misleading.
6. [DETERMINISTIC] Produce comparable ranges/units with assumptions and confidence.
7. [AI] Link normalized comparisons to source evidence and affected Competitor/Offer intelligence.
