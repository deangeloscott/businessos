---
id: customer-optimization.intervention.upsell-cross-sell
type: playbook
version: 1.1.0
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes:
- WorkRequest
- ChangeEvent
- Experiment
- MetricObservation
- OutcomeEvaluation
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - crm.contact.update
  - crm.opportunity.read
  - checkout.read
  - checkout.update
  - billing.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - email.send
  - workflow.update
  - experiment.run
context:
- EconomicContext
- Offer
---
# Upsell / Cross-Sell Optimization

## Purpose
Identify when an additional offer genuinely improves customer outcomes and present it at the right lifecycle moment.

## Business Outcome
Improve customer progression and value realization through upsell / cross-sell optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires upsell / cross-sell optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Map customer achieved/current outcomes to adjacent unmet needs and canonical Offers/products that can credibly help.
2. [DETERMINISTIC] Identify eligibility, usage/success prerequisites, timing signals, historical uptake, margin, and downstream success.
3. [HYBRID] Exclude customers with unresolved core value/support problems or poor fit; expansion should not mask failure.
4. [AI] Define trigger, value rationale, proof, friction, and appropriate channel/handoff.
5. [HYBRID] Delegate persuasion to Marketing and education to Content; Customer Optimization owns timing/progression logic.
6. [DETERMINISTIC] Measure incremental expansion value, adoption/success, churn/refund/support, and cannibalization guardrails.
