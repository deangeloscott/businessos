---
id: customer-optimization.intervention.checkout
type: playbook
version: 1.3.0
owner_system: customer-optimization
risk: medium
autonomy_ceiling: 3
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes:
- ActionPacket
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
subcontracts:
  required:
  - customer-optimization.diagnosis.root-cause
  - customer-optimization.intervention.design
  conditional:
  - id: customer-optimization.checkout.payment-failure
    when: payment failure is a material mechanism
---
# Checkout Optimization

## Purpose
Reduce preventable purchase friction while preserving trust, economics, compliance, and order quality.

## Business Outcome
Improve customer progression and value realization through checkout optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires checkout optimization to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Map checkout steps, fields, payment methods, validation/errors, fees/taxes/shipping timing, coupons, authentication, mobile/device behavior, and failure reasons.
2. [DETERMINISTIC] Quantify abandonment and technical/payment errors by stage/segment/device/source without assuming all abandonment is a defect.
3. [AI] Identify surprise cost, uncertainty, effort, forced account, payment limitation, trust, performance, and technical friction hypotheses.
4. [HYBRID] Separate Offer/price persuasion problems (Marketing/business) from checkout mechanics.
5. [HYBRID] Design intervention/test with revenue, fraud, support, margin, refund, and customer-experience guardrails.
6. [INTEGRATION] Implement authorized changes and payment options; verify transactions in controlled test.
7. [HYBRID] Evaluate completed profitable purchases and downstream quality, not checkout conversion alone.
