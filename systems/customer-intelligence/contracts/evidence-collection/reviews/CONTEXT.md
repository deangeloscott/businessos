---
id: customer.evidence-collection.reviews
type: playbook
owner_system: customer-intelligence
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
1. [INTEGRATION] Discover relevant review sources, then inspect the underlying reviews used for material claims; search-result snippets are discovery leads, not sufficient preserved evidence.
2. [INTEGRATION] Record the acquisition method, then preserve a bounded evidence packet for each material review with source/permalink, rating/date/context when available, and exact review text or bounded exact excerpt when permitted. Capture a screenshot/snapshot when it adds preservation/proof value and the surface permits it.
3. [DETERMINISTIC] Persist evidence through `scripts/persist_research_bundle.py` with `acquisition_method` for each source or the equivalent supported provider path so SourceRecords, optional Assets, Observations, hashes, lineage, and support links validate without custom schema-writing code.
4. [DETERMINISTIC] Deduplicate syndicated/cross-posted reviews and separate business-owned from competitor review sources.
5. [AI] Extract aspect-level praise, complaint, desired outcome, expectation, comparison, exact language, and severity rather than relying on whole-review sentiment only. Keep direct statements separate from interpretation.
6. [HYBRID] Weight evidence by freshness, verified-customer confidence when available, source incentives, and segment/product relevance.
7. [DETERMINISTIC] Trend aspects over time and compare ratings/themes by product, location, segment proxy, and lifecycle stage where valid.
8. [AI] Identify persistent themes, emerging issues, and contradictions with support/interview evidence. Do not call an Insight `supported` when its evidence chain is only a URL/search snippet or other pointer-only public source.
9. [HYBRID] Publish Customer Insights; route competitor-specific review observations to Competitor Intelligence and journey friction to Customer Optimization. Run research-evidence/business validation before calling the job complete.
