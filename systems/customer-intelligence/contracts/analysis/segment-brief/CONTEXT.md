---
id: customer.analysis.segment-brief
type: playbook
owner_system: customer-intelligence
reads:
- Insight
- Observation
- Asset
writes:
- Asset
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
# Customer Segment Intelligence Brief

## Purpose
Assemble the current evidence-backed understanding of a canonical AudienceSegment without creating a duplicate segment definition or a parallel context-change lifecycle.

## Business Outcome
Give future work a concise, current view of how a segment thinks, decides, succeeds, and differs from others while keeping customer evidence distinct from organization-owned segment definition.

## Run When
Run when a decision needs a current segment view or when materially new customer evidence changes segment understanding.

## Process
1. [DETERMINISTIC] Resolve the canonical AudienceSegment and current Customer Insights/Observations that reference or materially concern it.
2. [AI] Summarize context, jobs/outcomes, pains, objections, decision criteria, triggers, alternatives, language, proof needs, and success/churn patterns at the level the evidence supports.
3. [AI] Distinguish established evidence from emerging/provisional themes, inference, contradictions, and unknowns; note freshness where it can affect interpretation.
4. [AI] Compare with neighboring segments only when that comparison is useful to the decision, and do not infer meaningful difference merely from labels or sparse data.
5. [AI] Identify contradictions, missing coverage, and assumptions that downstream work should not treat as fact.
6. [AI] Produce a reusable brief/Asset referencing canonical objects rather than copying them into a new source of truth.
7. [AI] If the evidence suggests the canonical AudienceSegment itself may be wrong or outdated, state the supported correction or unresolved question explicitly. Customer Intelligence does not manufacture a change-control record merely because a possible correction exists. A current authoritative organization decision/correction can update canonical context through the normal Core memory path; preserve an unresolved context proposal only when remembering that unresolved possibility would materially help future work.

## Verification
- The brief is traceable to the segment-specific evidence it summarizes.
- Customer observation, inference, and canonical organization context remain distinct.
- No ContextUpdateProposal or other change-control object is required merely to produce or revise the brief.

## Completion Criteria
- The user or future model can understand the segment evidence, differences, uncertainty, and any material possible context correction without treating the brief itself as canonical segment truth.
