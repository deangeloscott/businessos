---
id: customer.monitoring.research-gaps
type: playbook
owner_system: customer-intelligence
reads:
- Insight
- Opportunity
- Observation
writes:
- Opportunity
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
# Customer Research Gap Review

## Purpose
Identify important customer decisions that currently depend on missing, stale, narrow, contradictory, or weak evidence.

## Business Outcome
Direct research attention toward the customer knowledge most likely to change a valuable business decision, while avoiding curiosity-driven research and unnecessary recurring scans.

## Run When
Use when a current decision, planning question, changed objective/offer/audience, or evidence-quality concern makes it useful to reassess whether customer knowledge is sufficient. A saved review/check intent may inform when the model chooses to revisit this later; the active harness/runtime owns any recurrence.

## Process
1. [AI] Identify the actual decisions/objectives in scope and the Customer Insights, Observations, prior research, and material assumptions those decisions rely on.
2. [AI] Identify gaps caused by low confidence, stale evidence, narrow segment/market coverage, contradiction, missing first-party evidence, or repeated uncertainty in real work.
3. [AI] Distinguish decision-critical gaps from interesting but non-decisive questions. Do not create research work merely because more information could exist.
4. [HYBRID] Check whether current or recently completed research already addresses the gap before proposing additional collection.
5. [AI] Judge whether better evidence could plausibly change the decision, materially change confidence/downside, or satisfy a real verification need. If not, stop.
6. [AI] Define the smallest useful evidence action: reuse existing records, inspect a connected source, ask a bounded question, conduct a focused study, or do nothing yet. Let the capable model/harness choose the appropriate research method and tools.
7. [HYBRID] Preserve an Opportunity only when the research gap itself represents material durable work worth finding and coordinating later. Otherwise return the concise gap/evidence recommendation directly without creating lifecycle state.
8. [AI] When future re-evaluation matters because the underlying customer condition is volatile or evidence will mature, preserve semantic review intent/date/context only when useful. AURA does not create or claim an active scheduled job.

## Verification
- Each identified gap traces to a real decision or material uncertainty.
- Proposed research is narrow enough to plausibly change that decision.
- Existing evidence/research is reused before new collection is proposed.
- Any saved Opportunity has durable organizational value rather than representing an internal routing step.

## Completion Criteria
- The organization knows which customer knowledge gap, if any, is worth resolving next and the smallest useful evidence action, without requiring a recurring AURA research scanner.
