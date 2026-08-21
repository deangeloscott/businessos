---
id: industry.event.detect
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
# Industry Event Detection

## Purpose
Determine whether new external observations represent a new material Event, an update to an existing Event, or noise.

## Business Outcome
Create one coherent evolving Event record rather than separate “news” objects for repeated coverage.

## Run When
Run whenever monitoring retrieves a potentially relevant external development.

## Process
1. [DETERMINISTIC] Normalize entity/topic/date/geography and compare the observation with active/recent IndustryEvents.
2. [AI] Determine whether it describes the same underlying development, a distinct event, a follow-on consequence, or merely commentary/repetition.
3. [AI] Separate factual new information from headline/framing changes.
4. [HYBRID] Require adequate source support before creating a material Event; keep unverified early signals scoped.
5. [DETERMINISTIC] Link the Observation to the matching Event or create a new Event with first-observed timestamp and source refs.
6. [AI] Classify event type, affected markets/entities, current status, and what remains unknown.
7. [DETERMINISTIC] Trigger verification/materiality only when the event contains genuinely new information.
