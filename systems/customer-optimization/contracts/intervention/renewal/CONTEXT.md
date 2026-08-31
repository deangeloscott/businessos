---
id: customer-optimization.intervention.renewal
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
  - customer-optimization.renewal.readiness
  conditional:
  - id: customer-optimization.monitoring.renewal-risk
    when: pre-renewal risk monitoring is needed
---
# Renewal Optimization

## Purpose
Make renewal decisions timely, informed, low-friction, and connected to demonstrated value.

## Business Outcome
Improve customer progression and value realization through renewal optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires renewal optimization to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Map renewal timeline, notice requirements, value review, decision stakeholders, procurement, pricing/terms, reminders, and failure states.
2. [AI] Combine usage/success/proof, customer expectations, objections, and contract context to identify renewal risk/opportunity.
3. [HYBRID] Separate process delay, unresolved value, pricing/offer, relationship, competitive, and procurement causes.
4. [AI] Design renewal sequence with value evidence, decision preparation, appropriate offer/terms handling, and escalation.
5. [HYBRID] Delegate persuasion assets to Marketing and content proof to Content where necessary.
6. [DETERMINISTIC] Measure on-time renewal, revenue retention, discounting, churn, and customer-experience guardrails.
