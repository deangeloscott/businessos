---
id: customer.evidence-collection.reviews
type: playbook
version: 1.1.0
owner_system: customer-intelligence
risk: low
autonomy_ceiling: 4
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - review.read
  optional:
  - crm.contact.read
  - analytics.read
context:
- AudienceSegment
- Market
- Offer
- ProductService
---
# Review Intelligence

## Purpose
Extract what customers praise, dislike, compare, and expect from first- and third-party reviews.

## Business Outcome
Reduce uncertainty about customers through review intelligence, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current review intelligence and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [INTEGRATION] Retrieve reviews with rating, date, product/location/source, and review text where permitted.
2. [DETERMINISTIC] Deduplicate syndicated/cross-posted reviews and separate business-owned from competitor review sources.
3. [AI] Extract aspect-level praise, complaint, desired outcome, expectation, comparison, exact language, and severity rather than relying on whole-review sentiment only.
4. [HYBRID] Weight evidence by freshness, verified-customer confidence when available, source incentives, and segment/product relevance.
5. [DETERMINISTIC] Trend aspects over time and compare ratings/themes by product, location, segment proxy, and lifecycle stage where valid.
6. [AI] Identify persistent themes, emerging issues, and contradictions with support/interview evidence.
7. [HYBRID] Publish Customer Insights; route competitor-specific review observations to Competitor Intelligence and journey friction to Customer Optimization.
