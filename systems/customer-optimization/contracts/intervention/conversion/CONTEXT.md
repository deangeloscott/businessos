---
id: customer-optimization.intervention.conversion
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
  - id: customer-optimization.conversion.form-friction
    when: form effort or errors are a material mechanism
---
# Conversion Optimization

## Purpose
Reduce non-persuasive process/UX friction between qualified intent and the intended conversion action.

## Business Outcome
Improve customer progression and value realization through conversion optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires conversion optimization to improve a defined customer transition or outcome.

## Process
1. [HYBRID] Confirm diagnosis is primarily progression/process friction rather than message/offer persuasion; route persuasion to Marketing.
2. [DETERMINISTIC] Map the exact conversion path, fields, steps, errors, delays, device states, eligibility, and abandonment points.
3. [AI] Identify unnecessary effort, ambiguity, choice overload, trust/process uncertainty, accessibility, technical failures, or handoff gaps.
4. [HYBRID] Select interventions that reduce friction without lowering lead/customer quality or violating required qualification/compliance.
5. [DETERMINISTIC] Define success/guardrail metrics and test/rollout plan.
6. [INTEGRATION] Implement authorized journey changes or delegate content/messaging components.
7. [HYBRID] Verify flow and evaluate qualified business outcomes, not raw conversion alone.
