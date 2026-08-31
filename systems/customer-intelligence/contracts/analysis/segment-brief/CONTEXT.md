---
id: customer.analysis.segment-brief
type: playbook
version: 1.3.0
owner_system: customer-intelligence
reads:
- Insight
- Observation
- Asset
writes:
- Asset
- ContextUpdateProposal
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
Assemble the current evidence-backed understanding of a canonical AudienceSegment without creating a duplicate segment definition.

## Business Outcome
Give downstream systems a concise, current view of how a segment thinks, decides, succeeds, and differs from others.

## Run When
Run when a downstream decision needs a current segment view or when materially new evidence changes segment understanding.

## Process
1. [DETERMINISTIC] Resolve the canonical AudienceSegment and active Customer Insights/Observations that apply to it.
2. [AI] Summarize context, jobs/outcomes, pains, objections, decision criteria, triggers, alternatives, language, proof needs, and success/churn patterns.
3. [AI] Distinguish stable evidence from emerging/provisional themes and note freshness.
4. [DETERMINISTIC] Compare with neighboring segments to surface differences that are actually decision-relevant.
5. [AI] Identify contradictions, missing coverage, and assumptions that downstream systems should not treat as fact.
6. [AI] Produce a reusable brief/Asset referencing canonical objects rather than copying them into a new source of truth.
7. [HYBRID] If evidence suggests the canonical segment definition itself should change, create a ContextUpdateProposal rather than editing it.
