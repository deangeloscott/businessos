---
id: industry.monitoring.news
type: playbook
version: 1.2.0
owner_system: industry-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- IndustryEvent
- Insight
capabilities:
  required:
  - news.read
  optional:
  - research.web.read
  - news.read
  - alert.read
  - market_data.read
  - rss.read
events:
  consumes:
  - none
  emits:
  - industry.event.updated
schedule:
  class: recurring
  default: daily
  configurable: true
context:
- Business
- Market
- Objective
- ProductService
---
# News Monitoring

## Purpose
Detect materially relevant current industry developments while suppressing duplicate/low-value coverage.

## Business Outcome
Improve the business response to external change through timely, evidence-backed news monitoring.

## Run When
Run when a decision or monitoring signal requires current news monitoring and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [INTEGRATION] Retrieve new items from prioritized source set with publication/event dates and canonical source references.
2. [DETERMINISTIC] Deduplicate syndicated/rewrite coverage and cluster items describing the same underlying event.
3. [AI] Extract the actual event claims, entities, dates, affected market, and what is confirmed versus reported/speculative.
4. [HYBRID] Check materiality against active markets, audiences, products, Objectives, risks, and existing IndustryEvents.
5. [HYBRID] Verify high-impact claims with authoritative/independent sources before escalating.
6. [DETERMINISTIC] Create/update IndustryEvent and Observations; only create an Insight after business relevance is interpreted.
7. [DETERMINISTIC] Emit industry.event.updated when material.
