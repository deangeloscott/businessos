---
id: customer.bootstrap.knowledge-map
type: playbook
version: 1.1.0
owner_system: customer-intelligence
risk: low
autonomy_ceiling: 4
reads:
- Insight
- SourceRecord
writes:
- Observation
- Insight
- WorkRequest
capabilities:
  required:
  - crm.opportunity.read
  optional:
  - customer_feedback.read
  - support.ticket.read
  - sales_call.read
  - survey.read
  - review.read
context:
- AudienceSegment
- Objective
- Offer
---
# Customer Knowledge Map

## Purpose
Establish what customer questions matter, what evidence already exists, and which unknowns materially affect decisions.

## Business Outcome
Reduce uncertainty about customers through customer knowledge map, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current customer knowledge map and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [AI] Translate active Business Objectives, Audience Segments, Offers, and known decision points into a prioritized list of customer-knowledge questions.
2. [DETERMINISTIC] Inventory available customer evidence sources and coverage by segment, journey stage, market, and recency.
3. [AI] Map existing active Customer Insights to the knowledge questions and mark direct, partial, contradictory, or missing coverage.
4. [HYBRID] Classify gaps as blocking, high-value, monitor-only, or optional based on expected decision impact.
5. [AI] Choose the least costly credible evidence source for each material gap; prefer first-party direct customer evidence for customer claims when available.
6. [DETERMINISTIC] Record refresh needs and avoid duplicate research already active elsewhere.
7. [HYBRID] Produce a bounded research plan with priority, evidence target, and confidence goal rather than a generic research backlog.
