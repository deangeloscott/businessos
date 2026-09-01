---
id: industry.source-mapping.priority-sources
type: playbook
owner_system: industry-intelligence
reads: []
writes:
- SourceRecord
- Observation
capabilities:
  required:
  - research.web.read
  optional:
  - news.read
  - regulatory.read
  - research.paper.read
  - market_data.read
  - rss.read
context:
- Business
- Market
- Objective
- ProductService
---
# Industry Source Map

## Purpose
Define authoritative and useful sources by event type so monitoring coverage is deliberate rather than news-volume driven.

## Business Outcome
Improve the business response to external change through timely, evidence-backed industry source map.

## Run When
Run when a decision or monitoring signal requires current industry source map and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Translate Business Context, markets, products, compliance, and Objectives into external development categories that could materially change decisions.
2. [AI] For each category identify primary/authoritative, specialist, research, company, trade, data, and reputable news source classes.
3. [HYBRID] Rank sources by authority for the fact type, directness, timeliness, historical reliability, access stability, and duplication.
4. [DETERMINISTIC] Map sources to event types/markets and expected cadence; identify single-source failure points.
5. [HYBRID] Define corroboration requirements for high-impact claims such as regulation, scientific findings, or market shocks.
6. [DETERMINISTIC] Persist source monitoring configuration without copying provider credentials.
