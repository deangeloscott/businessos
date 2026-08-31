---
id: customer.monitoring.research-gaps
type: playbook
version: 1.3.0
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
# Customer Research Gap Monitoring

## Purpose
Continuously identify important customer decisions that rely on missing, stale, narrow, or weak evidence.

## Business Outcome
Prioritize research where improved customer knowledge is most likely to change a valuable business decision.

## Run When
Run on a recurring intelligence review or when business objectives, offers, audiences, or major customer conditions change.

## Process
1. [DETERMINISTIC] Inventory active high-priority Objectives, Opportunities, Customer Insights, review dates, and unresolved selectors.
2. [AI] Identify important assumptions with low confidence, stale evidence, narrow segment coverage, or repeated downstream uncertainty.
3. [AI] Distinguish curiosity gaps from decision-critical knowledge gaps.
4. [DETERMINISTIC] Detect duplicated open research and existing collection work before creating anything new.
5. [AI] Estimate decision impact, urgency, researchability, and evidence already available.
6. [AI] Create Customer Intelligence Opportunities only for material knowledge gaps and link the decisions they affect.
7. [DETERMINISTIC] Schedule review/refresh according to volatility rather than one universal cadence.
