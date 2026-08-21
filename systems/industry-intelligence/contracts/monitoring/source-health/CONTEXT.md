---
id: industry.monitoring.source-health
type: playbook
version: 1.3.0
owner_system: industry-intelligence
risk: low
autonomy_ceiling: 2
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
# Industry Source Health Monitoring

## Purpose
Detect when priority industry sources stop updating, move, degrade, or become unreliable.

## Business Outcome
Prevent silent monitoring blind spots caused by broken feeds, changed URLs, or stale source assumptions.

## Run When
Run on a periodic source-health cadence for priority monitoring sources.

## Process
1. [DETERMINISTIC] Check retrieval status, last publication/update, expected cadence, redirects/location, format/parser changes, and authentication/access status.
2. [DETERMINISTIC] Compare observed source behavior with its expected update pattern.
3. [AI] Determine whether inactivity is normal, event-driven, retired/moved, or a likely collection failure.
4. [INTEGRATION] Locate official replacement feeds/pages/endpoints when a source moves.
5. [HYBRID] Revalidate authority when ownership/publisher/methodology materially changes.
6. [DETERMINISTIC] Update source map and monitoring bindings without losing historical SourceRecords.
7. [AI] Create a monitoring-gap Opportunity only when source loss creates material decision risk.
