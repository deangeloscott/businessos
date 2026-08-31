---
id: customer.analysis.churn
type: playbook
version: 1.3.0
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - none
  optional:
  - customer_feedback.read
  - crm.opportunity.read
  - support.ticket.read
  - sales_call.read
  - survey.read
  - review.read
  - analytics.read
events:
  consumes:
  - none
  emits:
  - customer.insight.updated
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - customer.research.evidence-coverage
  - customer.analysis.theme-coding
  - customer.analysis.decision-drivers
---
# Churn Reason Analysis

## Purpose
Understand customer-stated and evidenced reasons for leaving without conflating correlation with customer motivation.

## Business Outcome
Reduce uncertainty about customers through churn reason analysis, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current churn reason analysis and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [DETERMINISTIC] Define churn event/cohort, voluntary vs involuntary where relevant, segment, tenure, product/offer, and analysis window.
2. [INTEGRATION] Gather cancellation reasons, exit interviews, support history, success notes, usage summaries, billing events, and renewal communications.
3. [AI] Extract customer-stated reasons, unmet outcomes, expectation gaps, alternatives, triggers, and language.
4. [HYBRID] Separate stated reason from behavioral predictors owned by Customer Optimization.
5. [DETERMINISTIC] Compare churn reasons across tenure/segment/cohort while reporting missing exit-feedback coverage.
6. [AI] Identify multi-cause patterns and contradictions between stated reasons and preceding experience.
7. [HYBRID] Publish Customer Insights and send lifecycle-friction evidence to Customer Optimization.
