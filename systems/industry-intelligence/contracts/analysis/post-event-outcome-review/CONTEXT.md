---
id: industry.analysis.post-event-outcome-review
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
# Industry Event Outcome Review

## Purpose
Compare predicted impact pathways and scenarios with what actually occurred after an Event matured.

## Business Outcome
Improve future industry judgment by learning which signals, mechanisms, and assumptions were reliable.

## Run When
Run when an important Event reaches a meaningful outcome or evaluation window.

## Process
1. [DETERMINISTIC] Retrieve the original Event, factual summary, impact pathways, scenarios, predicted indicators, and downstream actions.
2. [INTEGRATION] Collect post-event evidence for the indicators/outcomes that were expected to change.
3. [AI] Compare predicted versus observed direction, timing, magnitude, affected populations, and unexpected consequences.
4. [AI] Identify which assumptions/pathways were supported, contradicted, untestable, or confounded.
5. [HYBRID] Separate poor prediction from a good decision under uncertainty; do not rewrite history based on hindsight.
6. [AI] Produce Industry Learning candidates about source quality, event classes, impact mechanisms, and response timing.
7. [DETERMINISTIC] Update Event/Insight status and future monitoring rules where warranted.
