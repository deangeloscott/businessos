---
id: industry.analysis.business-impact
type: playbook
version: 1.1.0
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
---
# Business Impact Analysis

## Purpose
Translate a verified external event into evidence-backed implications for this specific business.

## Business Outcome
Improve the business response to external change through timely, evidence-backed business impact analysis.

## Run When
Run when a decision or monitoring signal requires current business impact analysis and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Load the IndustryEvent plus relevant Business Context, Objectives, markets, audiences, offers, constraints, and existing Intelligence.
2. [AI] Enumerate plausible mechanisms affecting demand, customer concerns, competitors, operations, compliance, economics, channels, or positioning.
3. [HYBRID] Separate confirmed direct effects from scenario-dependent second-order effects.
4. [AI] Identify which systems have semantic authority to investigate each implication.
5. [HYBRID] Estimate urgency/value/risk ranges and evidence gaps without creating domain Opportunities on their behalf.
6. [DETERMINISTIC] Publish Industry Insight and relevance events; create refresh/research requests where owner-domain evidence is missing.
