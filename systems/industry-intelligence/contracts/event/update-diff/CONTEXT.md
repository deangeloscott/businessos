---
id: industry.event.update-diff
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
# Industry Event Update Diff

## Purpose
Identify exactly what changed since the last verified Event state.

## Business Outcome
Prevent repeated headlines from being treated as new intelligence and focus attention on new facts.

## Run When
Run whenever an existing IndustryEvent receives new source material.

## Process
1. [DETERMINISTIC] Load the prior factual summary/timeline and new observations.
2. [AI] Classify each new item as duplicate, clarification, correction, new fact, status change, scope change, effective-date change, consequence, or commentary.
3. [AI] Identify which prior facts are now outdated, contradicted, or superseded.
4. [DETERMINISTIC] Preserve prior versions and source refs; do not overwrite historical fact state.
5. [AI] State the material delta in the smallest precise form.
6. [HYBRID] Re-run materiality/impact only if the delta can change a decision or prior Insight.
7. [DETERMINISTIC] Update Event status, timeline, follow-up date, and emit an update event only for meaningful deltas.
