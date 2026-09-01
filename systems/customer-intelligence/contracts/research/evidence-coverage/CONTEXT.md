---
id: customer.research.evidence-coverage
type: playbook
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- Observation
- WorkRequest
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
# Customer Evidence Coverage Audit

## Purpose
Determine whether available customer evidence is sufficiently representative, current, and direct for the decision being made.

## Business Outcome
Prevent confident customer conclusions from being built on stale, narrow, or systematically biased evidence.

## Run When
Run before activating a high-impact Customer Insight, after major market/customer change, or when evidence quality is disputed.

## Process
1. [DETERMINISTIC] Inventory evidence by source type, segment, journey stage, recency, outcome class, and directness.
2. [AI] Identify populations or perspectives absent from the evidence, including non-buyers, losses, churned customers, and unsuccessful users where relevant.
3. [HYBRID] Evaluate selection, survivorship, nonresponse, channel, interviewer, and self-report bias.
4. [DETERMINISTIC] Compare coverage against the research plan or decision-specific minimums; do not convert arbitrary sample counts into certainty.
5. [AI] Determine which gaps could materially change the conclusion versus gaps that are unlikely to affect the decision.
6. [AI] Mark conclusions as sufficiently supported, scoped/narrowed, provisional, or blocked and state why.
7. [AI] Create targeted collection WorkRequests only for material gaps.
