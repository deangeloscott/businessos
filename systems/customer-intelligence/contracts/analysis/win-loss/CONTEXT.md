---
id: customer.analysis.win-loss
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
# Win/Loss Analysis

## Purpose
Explain why qualified opportunities are won or lost using direct and behavioral evidence, not CRM reason codes alone.

## Business Outcome
Reduce uncertainty about customers through win/loss analysis, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current win/loss analysis and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [DETERMINISTIC] Define comparable won/lost cohort, period, segment, offer, deal size, channel, and minimum evidence coverage.
2. [INTEGRATION] Retrieve CRM outcomes, customer communications/calls, competitor references, pricing/discount context, stage duration, and available post-decision interviews.
3. [AI] Extract direct customer decision reasons and separate them from seller inference.
4. [HYBRID] Build multi-cause decision records with primary/contributing factors and unknown where evidence is absent.
5. [DETERMINISTIC] Compare rates and factor prevalence across wins/losses while checking selection/sample bias.
6. [AI] Identify decision criteria, competitive alternatives, proof gaps, expectation mismatches, and segment-specific patterns.
7. [HYBRID] Test candidate explanations against contradictory cases and behavior rather than reporting correlation as cause.
8. [HYBRID] Publish scoped Customer Insights; contribute competitor observations; route journey/process findings appropriately.

## Decision Rules
- Treat CRM loss/win reason fields as evidence about seller/system coding unless the reason is traceable to the buyer.
- Use `unknown` when evidence does not support a reason; do not force complete attribution.
- Publish segment-specific Insights instead of one global conclusion when factor prevalence or mechanism differs materially by segment, Offer, or stage.
- Do not infer causal importance from factor frequency alone; compare wins/losses and contradictory cases, and state when sampling prevents a reliable comparison.
