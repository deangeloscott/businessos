---
id: industry.monitoring.market
type: playbook
owner_system: industry-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- IndustryEvent
- Insight
capabilities:
  required:
  - market_data.read
  optional:
  - research.web.read
  - news.read
  - alert.read
  - market_data.read
context:
- Business
- Market
- Objective
- ProductService
---
# Market & Category Review

## Purpose
Review structural category/economic shifts relevant to demand, supply, pricing, customer behavior, competitive conditions, or business economics.

## Business Outcome
Give the organization current, evidence-backed market understanding without turning AURA into a market-data monitoring runtime.

## Run When
Use when a current decision or saved monitoring intent needs current market/category evidence and existing organizational knowledge may be stale, incomplete, or unresolved. Any recurring execution is owned by the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve only the market/category indicators and authoritative contextual sources material to the current question using the host's available capabilities.
2. [DETERMINISTIC] Validate definitions, units, revisions, geography, comparable periods, and any required mechanical transformations before calculating change.
3. [AI] Interpret what the observed movement may mean for customer/business mechanisms without treating correlation as established causality.
4. [HYBRID] Compare quantitative movement with relevant customer, competitor, industry, and active-business evidence where that comparison materially improves interpretation.
5. [AI] Identify which audiences, products/services, markets, economics, constraints, threats, or opportunities may actually be affected and preserve uncertainty when applicability is unclear.
6. [HYBRID] Persist SourceRecords/Observations and an Insight or IndustryEvent only when the evidence creates durable organizational value. Do not manufacture an Opportunity or downstream route merely because an indicator moved.
7. [AI] When future review matters, preserve the semantic reason/date/condition worth revisiting. The active harness/runtime owns any actual recurring check or notification.

## Verification
- Indicator definitions, units, geography, and revisions are explicit enough to support comparison.
- Market movement and causal/business interpretation remain distinguishable.
- External market evidence is not treated as proof of active-business impact without business-specific evidence.
- Saved review intent does not claim an active schedule exists.

## Completion Criteria
- The organization has the smallest useful current market/category understanding needed for the decision, with material evidence and uncertainty preserved for future reuse.
