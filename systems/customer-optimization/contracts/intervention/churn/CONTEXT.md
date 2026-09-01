---
id: customer-optimization.intervention.churn
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
subcontracts:
  required:
  - customer-optimization.diagnosis.root-cause
  - customer-optimization.retention.risk-segmentation
  - customer-optimization.retention.intervention-plan
---
# Churn Diagnosis & Prevention

## Purpose
Identify actionable churn risk mechanisms and intervene before avoidable customer loss while respecting non-fit churn.

## Business Outcome
Improve customer progression and value realization through churn diagnosis & prevention, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires churn diagnosis & prevention to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Define churn/renewal event, at-risk horizon, cohort, involuntary vs voluntary where relevant, and baseline rates.
2. [DETERMINISTIC] Analyze preceding product/service behavior, support, billing, success milestones, engagement, contract/timing, and segment patterns.
3. [AI] Combine Customer Intelligence stated churn reasons with behavioral predictors without treating predictors as motivations.
4. [HYBRID] Identify preventable mechanisms, non-fit/healthy churn, and cases requiring service recovery or product/business escalation.
5. [AI] Design targeted interventions tied to the mechanism rather than blanket discounts/reminders.
6. [DETERMINISTIC] Define incremental retention, margin, complaint, discount, and long-term value guardrails.
7. [INTEGRATION] Execute eligible risk workflows and evaluate causal lift where possible.
