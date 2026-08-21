---
id: industry.analysis.event-deduplication
type: playbook
version: 1.1.0
owner_system: industry-intelligence
risk: low
autonomy_ceiling: 4
reads:
- IndustryEvent
- Observation
- SourceRecord
- Insight
writes:
- IndustryEvent
- Observation
- Insight
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - research.web.read
  - news.read
  - regulatory.read
  - research.paper.read
  - market_data.read
events:
  consumes:
  - none
  emits:
  - industry.insight.updated
context:
- Business
- Market
- Objective
- ProductService
---
# Event Deduplication & Clustering

## Purpose
Resolve many articles/updates into one evolving underlying IndustryEvent.

## Business Outcome
Improve the business response to external change through timely, evidence-backed event deduplication & clustering.

## Run When
Run when a decision or monitoring signal requires current event deduplication & clustering and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [DETERMINISTIC] Normalize source URLs/titles/dates and group exact/syndicated duplicates.
2. [AI] Compare entities, event action, location, date, causal sequence, and source claims to determine whether items refer to the same underlying event.
3. [HYBRID] Keep separate events when materially different actions, jurisdictions, dates, or causal episodes would change downstream decisions.
4. [DETERMINISTIC] Merge references into one IndustryEvent without deleting contradictory observations.
5. [AI] Update event summary using only currently supported claims and preserve evolution chronology.
6. [DETERMINISTIC] Maintain source/observation lineage and emit one material event update rather than duplicate alerts.
