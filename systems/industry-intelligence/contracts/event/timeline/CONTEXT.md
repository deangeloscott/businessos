---
id: industry.event.timeline
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
# Industry Event Timeline

## Purpose
Maintain the sequence of meaningful developments in an evolving IndustryEvent.

## Business Outcome
Make updates, causality, deadlines, and status changes understandable without rereading every article.

## Run When
Run for developing events with multiple announcements, actions, effective dates, revisions, or consequences.

## Process
1. [DETERMINISTIC] Collect dated Event Observations and normalize announcement, occurrence, effective, publication, and expected future dates.
2. [AI] Group duplicate coverage and select the event-changing facts for the timeline.
3. [AI] Distinguish planned/announced, enacted/released, effective, enforced/observed, reversed, delayed, and superseded milestones.
4. [DETERMINISTIC] Preserve source refs and confidence for each milestone.
5. [AI] Mark dependencies and future checkpoints that could change business implications.
6. [HYBRID] Avoid inferring causal order solely because one item occurred earlier.
7. [DETERMINISTIC] Update the canonical Event and next follow-up schedule.
