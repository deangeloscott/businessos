---
id: customer-optimization.intervention.repeat-purchase
type: playbook
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
# Repeat Purchase Optimization

## Purpose
Increase appropriate repeat purchases by making replenishment/reuse timing and value clear without over-contacting.

## Business Outcome
Improve customer progression and value realization through repeat purchase optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires repeat purchase optimization to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Analyze purchase intervals, product/category replenishment cycles, customer cohorts, usage/consumption proxies, and repeat rates.
2. [AI] Identify why customers do/do not return: timing, satisfaction, awareness, convenience, price, alternatives, changed need, or product fit.
3. [HYBRID] Define eligible moments and suppression rules; avoid prompting repurchase when likely unnecessary/inappropriate.
4. [AI] Design reminders, reorder convenience, bundles, education, loyalty/value communication, or service interventions as appropriate.
5. [DETERMINISTIC] Measure incremental profitable repeat purchases, unsubscribes/complaints, discount cost, and long-term value.
