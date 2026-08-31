---
id: customer-optimization.intervention.referral
type: playbook
version: 1.3.0
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
subcontracts:
  required:
  - customer-optimization.referral.eligibility-timing
---
# Referral Optimization

## Purpose
Make it easy and appropriate for successful customers to recommend the business when genuine value exists.

## Business Outcome
Improve customer progression and value realization through referral optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires referral optimization to improve a defined customer transition or outcome.

## Process
1. [HYBRID] Define customer success/eligibility thresholds so requests target customers with demonstrated positive outcomes rather than arbitrary dates.
2. [DETERMINISTIC] Analyze current referral sources, timing, friction, incentives where allowed, and referred-customer quality.
3. [AI] Identify natural advocacy moments: outcome achieved, praise, renewal, milestone, support success, event/community interaction.
4. [AI] Design low-friction ask/mechanism, shareable context, recognition/incentive where appropriate, and opt-out behavior.
5. [HYBRID] Ensure compliance/industry rules and avoid pressuring customers during unresolved issues.
6. [DETERMINISTIC] Measure referral rate, referred customer quality/value, incentive cost, and customer sentiment.
