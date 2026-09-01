---
id: customer.analysis.insight-refresh
type: playbook
owner_system: customer-intelligence
reads:
- Insight
- Observation
writes:
- Insight
capabilities:
  required:
  - none
  optional:
  - crm.opportunity.read
  - crm.activity.read
  - sales_call.read
  - support.ticket.read
  - survey.read
  - review.read
  - community.read
  - social.listen
  - analytics.read
  - research.web.read
context:
- AudienceSegment
- Objective
---
# Customer Insight Refresh

## Purpose
Re-evaluate an existing Customer Insight against new, stale, or contradictory evidence.

## Business Outcome
Keep customer intelligence current without overwriting history or preserving disproven assumptions.

## Run When
Run when an Insight reaches its review date, receives material new evidence, or is contradicted by downstream outcomes.

## Process
1. [DETERMINISTIC] Load the existing Insight, original evidence, new relevant Observations, scope, confidence, and downstream dependents.
2. [AI] Compare supporting, contradicting, contextualizing, and extending evidence while weighting directness and freshness appropriately.
3. [AI] Test whether the apparent contradiction is caused by segment, time, market, journey stage, or methodology differences.
4. [HYBRID] Decide whether to strengthen, weaken, narrow, broaden, supersede, contradict, or leave the Insight unchanged.
5. [DETERMINISTIC] Preserve prior state/evidence lineage and create explicit relationships to any replacement Insight.
6. [AI] State what changed, why, confidence, applicability, and what remains uncertain.
7. [DETERMINISTIC] Emit dependency-change events so affected Opportunities can be re-evaluated rather than silently continuing.
