---
id: customer-optimization.intervention.onboarding
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
  - customer-optimization.onboarding.milestone-design
  - customer-optimization.onboarding.sequence-design
  - customer-optimization.onboarding.guidance
  - customer-optimization.onboarding.escalation
  - customer-optimization.onboarding.qa
---
# Onboarding Optimization

## Purpose
Help new customers reach the first meaningful value state with less confusion, delay, and avoidable effort.

## Business Outcome
Improve customer progression and value realization through onboarding optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires onboarding optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Define the customer-specific activation/time-to-value state and required onboarding milestones rather than counting task completion alone.
2. [DETERMINISTIC] Measure completion, time, dropoff, retries, support, handoffs, implementation delays, and segment differences by milestone.
3. [HYBRID] Combine behavioral evidence with Customer Insights/support/success feedback to diagnose why customers stall.
4. [AI] Redesign sequence, defaults, guidance, ownership, expectations, education, checklists, and escalation around the shortest safe path to value.
5. [HYBRID] Delegate educational Content and motivational Messaging while Customer Optimization retains the Opportunity.
6. [DETERMINISTIC] Define activation/time-to-value/customer-quality guardrails and experiment/rollout.
7. [INTEGRATION] Implement workflow/product/process changes as authorized; verify and evaluate retention/value effects.

## Decision Rules
- Define the activation/value milestone the onboarding process exists to achieve; task completion alone is not success.
- Distinguish missing instruction, missing motivation, product/service defect, operational delay, role ambiguity, and expectation mismatch because they require different interventions.
- Prefer removing unnecessary onboarding work before adding reminders, education, or automation around it.
- Measure time-to-value and downstream activation/retention guardrails, not just onboarding-step completion.
