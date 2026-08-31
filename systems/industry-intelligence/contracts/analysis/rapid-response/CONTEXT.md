---
id: industry.analysis.rapid-response
type: playbook
version: 1.3.0
owner_system: industry-intelligence
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
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - industry.event.factual-summary
  - industry.analysis.impact-pathway
  - industry.handoff.decision-brief
---
# Rapid Response Intelligence

## Purpose
Produce a verified bounded intelligence packet quickly when a developing event demands business communication or action.

## Business Outcome
Improve the business response to external change through timely, evidence-backed rapid response intelligence.

## Run When
Run when a decision or monitoring signal requires current rapid response intelligence and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Define the exact urgent decision and maximum acceptable uncertainty/time horizon.
2. [INTEGRATION] Retrieve primary/most authoritative current sources first and timestamp every claim.
3. [AI] Separate confirmed facts, credible reports, unknowns, implications, and speculation.
4. [HYBRID] Perform rapid materiality/business-impact assessment and identify compliance/reputation sensitivity.
5. [AI] Produce a concise reusable Insight plus source/evidence references and affected-system notifications.
6. [HYBRID] Explicitly schedule/trigger follow-up verification because developing facts may change.
7. [DETERMINISTIC] Update/supersede the rapid Insight when authoritative facts evolve.
