---
id: industry.analysis.event-evolution
type: playbook
version: 1.3.0
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
subcontracts:
  required:
  - industry.event.timeline
  - industry.event.update-diff
  - industry.event.follow-up
---
# Event Evolution Tracking

## Purpose
Maintain one coherent evolving event state as new facts, dates, interpretations, and impacts emerge.

## Business Outcome
Improve the business response to external change through timely, evidence-backed event evolution tracking.

## Run When
Run when a decision or monitoring signal requires current event evolution tracking and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [DETERMINISTIC] Compare new observations with current IndustryEvent claims/status/timeline.
2. [AI] Classify new evidence as confirmation, clarification, contradiction, escalation, de-escalation, new phase, or unrelated event.
3. [HYBRID] Update current summary/status without erasing historical states or contradictory evidence.
4. [AI] Reassess materiality, urgency, affected domains, and active Insights when the event meaning changes.
5. [DETERMINISTIC] Emit dependency-changed events for materially affected Insights/Opportunities.
6. [HYBRID] Close/archive only when decision relevance has ended and residual monitoring needs are explicit.
