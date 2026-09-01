---
id: customer-optimization.intervention.activation
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
# Activation Optimization

## Purpose
Increase the share of acquired customers reaching an evidence-backed early value behavior predictive of durable success.

## Business Outcome
Improve customer progression and value realization through activation optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires activation optimization to improve a defined customer transition or outcome.

## Process
1. [HYBRID] Validate the activation definition against later value/retention rather than choosing a convenient event.
2. [DETERMINISTIC] Analyze path/time to activation, prerequisite behaviors, cohort differences, and dropoff.
3. [AI] Identify barriers: setup, knowledge, missing data/integration, unclear next step, poor fit, product/process issue, delayed external dependency.
4. [HYBRID] Prioritize interventions by impact on true activation and customer value, not event inflation.
5. [INTEGRATION] Implement guided actions/workflows/content as authorized.
6. [DETERMINISTIC] Verify event instrumentation and measure downstream retention/success guardrails.
