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
Use when new evidence, saved review timing, downstream outcomes, or the current decision makes an existing Customer Insight worth re-evaluating. AURA may remember review intent; the active harness/runtime owns any actual reminder or recurring check.

## Process
1. [DETERMINISTIC] Load the existing Insight, its referenced evidence, new relevant Observations, scope, confidence, and resolvable canonical relationships.
2. [AI] Compare supporting, contradicting, contextualizing, and extending evidence while weighting directness and freshness appropriately.
3. [AI] Test whether the apparent contradiction is caused by segment, time, market, journey stage, or methodology differences.
4. [AI] Decide whether to strengthen, weaken, narrow, broaden, supersede, contradict, or leave the Insight unchanged.
5. [DETERMINISTIC] Preserve prior evidence/lineage and explicit references to any replacement or superseding Insight.
6. [AI] State what changed, why, confidence, applicability, and what remains uncertain.
7. [HYBRID] Persist the updated durable Insight state. When the changed understanding materially affects another active decision or Opportunity, surface that implication in the current work or future retrieval rather than emitting an internal dependency-change event.

## Verification
- Evidence supporting and contradicting the Insight remains inspectable.
- Semantic confidence/applicability changes are model judgments, not deterministic lifecycle transitions.
- Refresh timing is organizational intent, not an AURA-owned schedule.

## Completion Criteria
- Current Customer Insight state reflects the strongest available evidence and preserves enough lineage for future work to understand what changed without an internal event bus.
