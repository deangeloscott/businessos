---
id: industry.event.factual-summary
type: playbook
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
# Industry Event Factual Summary

## Purpose
Produce a source-grounded account of what happened before adding business or audience interpretation.

## Business Outcome
Give all downstream systems a stable factual layer that can be updated without mixing facts with recommendations.

## Run When
Run after an Event is verified or materially updated.

## Process
1. [DETERMINISTIC] Resolve the Event timeline and highest-authority supporting/contradicting SourceRecords.
2. [AI] State who/what/where/when and the specific change, decision, finding, release, rule, or occurrence.
3. [AI] Separate confirmed facts, reported claims, estimates, disputed points, and unknowns.
4. [AI] Include material dates such as announcement, effective, enforcement, release, study period, or next milestone where applicable.
5. [HYBRID] Remove audience advice, business recommendations, speculation, and “so what” interpretation from the factual layer.
6. [DETERMINISTIC] Link each material factual statement to evidence and preserve version/update history.
7. [AI] Produce a concise updated summary that downstream Insights can reference.
