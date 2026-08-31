---
id: industry.research.source-validation
type: playbook
version: 1.3.0
owner_system: industry-intelligence
reads:
- IndustryEvent
- SourceRecord
- Observation
- Insight
writes:
- IndustryEvent
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - news.read
  - rss.read
  - regulatory.read
  - research.paper.read
  - market_data.read
  - social.listen
  - webpage.snapshot
  - webpage.compare
  - alert.read
context:
- Business
- Market
- Objective
---
# Industry Source Validation

## Purpose
Evaluate whether an industry source is suitable for discovering or supporting a specific fact.

## Business Outcome
Prevent low-quality, copied, stale, or circular reporting from becoming authoritative business intelligence.

## Run When
Run when adding a recurring source or when a material Event depends on uncertain source quality.

## Process
1. [AI] Identify source origin, publisher/author, publication/revision date, primary-vs-secondary status, expertise, incentives, and evidence cited.
2. [DETERMINISTIC] Trace important claims toward primary documents/data where available and detect syndicated/copied reporting.
3. [AI] Evaluate directness, methodology, scope, freshness, correction history, and whether the source can support the specific fact claimed.
4. [HYBRID] Note conflicts of interest, anonymous/unclear sourcing, sensational framing, or missing methodology without automatically discarding useful signals.
5. [AI] Distinguish discovery value from evidentiary authority; a weak source may surface an event but not validate it.
6. [DETERMINISTIC] Record the source assessment and which claim types it can/cannot support.
7. [AI] Require corroboration or primary-source verification where material conclusions exceed source authority.
