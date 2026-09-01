---
id: customer.analysis.objections
type: playbook
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
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Objection Analysis

## Purpose
Understand what prevents qualified buyers from acting and what evidence would resolve or reduce uncertainty.

## Business Outcome
Reduce uncertainty about customers through objection analysis, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current objection analysis and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [AI] Retrieve direct customer/prospect objections from calls, lost deals, emails, interviews, surveys, and relevant support/pre-purchase sources.
2. [AI] Separate true objection, request for information, negotiation tactic, lack of urgency, poor fit, and operational constraint.
3. [AI] Classify objection object: price, trust, risk, timing, implementation, authority, effort, alternatives, proof, features, procurement, or other evidence-backed class.
4. [HYBRID] Map objection by segment, offer, awareness/buyer stage, and outcome rather than producing a universal list.
5. [HYBRID] Compare stated objection with actual outcome and behavioral evidence to avoid accepting post-hoc rationalizations as certain causes.
6. [AI] Identify missing proof/information implied by objections without prescribing marketing copy yet.
7. [HYBRID] Publish Customer Insights and route persuasion implications to Marketing Synthesis.
