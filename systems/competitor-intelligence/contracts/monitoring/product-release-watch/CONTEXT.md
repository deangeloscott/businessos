---
id: competitor.monitoring.product-release-watch
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
# Competitor Product Release Watch

## Purpose
Detect material competitor product, capability, release, or integration changes against the last verified state.

## Business Outcome
Keep competitive intelligence current and distinguish meaningful change from cosmetic edits.

## Run When
Run on the monitoring cadence for priority competitors or when an external signal suggests a product, capability, release, or integration change.

## Process
1. [DETERMINISTIC] Resolve the priority competitor, monitored sources, and last verified baseline.
2. [INTEGRATION] Retrieve current source state and compare it with the last stored version/snapshot.
3. [DETERMINISTIC] Filter exact/noise/cosmetic changes and preserve the raw diff for material candidates.
4. [AI] Determine what changed factually, affected product/offer/audience, effective date if known, and whether the change is material.
5. [AI] Create/update Observations and identify which existing Insights may require refresh.
6. [HYBRID] Avoid strategic interpretation until evidence exceeds the factual change itself; route material changes to analysis.
7. [DETERMINISTIC] Update monitoring checkpoint and emit change event only when new information exists.
