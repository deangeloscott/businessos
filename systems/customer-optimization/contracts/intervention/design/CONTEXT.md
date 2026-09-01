---
id: customer-optimization.intervention.design
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- Observation
- Insight
- Opportunity
- MetricObservation
- Experiment
writes:
- Observation
- Insight
- Opportunity
capabilities:
  required:
  - analytics.read
  optional:
  - product_analytics.read
  - crm.contact.read
  - crm.opportunity.read
  - checkout.read
  - billing.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - experiment.run
  - workflow.update
  - email.send
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Customer Journey Intervention Design

## Purpose
Design the smallest intervention likely to remove the diagnosed cause while protecting customer quality and downstream outcomes.

## Business Outcome
Improve the journey mechanism rather than adding unnecessary complexity.

## Run When
Use after root-cause diagnosis identifies an addressable Customer Optimization Opportunity.

## Process
1. [AI] Restate the diagnosed cause, affected customer state, desired next state, mechanism, and real constraints.
2. [AI] Generate intervention options beginning with removing unnecessary steps, delay, ambiguity, handoff, or failure before adding reminders/content/automation.
3. [AI] Evaluate each option for customer effort, accessibility, operational burden, fit/qualification, risk, reversibility, dependencies, and expected downstream effect without fabricating impact estimates.
4. [HYBRID] Identify work that naturally belongs to another owner: Marketing for persuasion, Content for communication, Customer Intelligence for unknown motive, or the appropriate human/domain for product, sales, legal, finance, or operational causes. Create a durable `WorkRequest` only when a real handoff should survive the current session.
5. [AI] Select the smallest viable change or controlled test capable of validating the mechanism, when the user actually wants a recommendation/design decision.
6. [HYBRID] Define the implementation needed to test the mechanism: target, change, baseline/comparison, success criteria, guardrails, measurement window, rollback/recovery considerations, dependencies, and verification appropriate to the consequence. These are method design choices, not deterministic permission rules.
7. [AI] Preserve the intervention design in the smallest useful durable form when future work benefits from it: update the relevant Opportunity/Experiment/Asset or create a real handoff. Do not create an execution packet, approval object, or ordered runtime plan merely to make the design actionable.

## Verification
- The intervention addresses the diagnosed mechanism rather than a superficial symptom.
- Success criteria and guardrails are decision rules or evidence-backed expectations, not fabricated forecasts.
- Any delegated work maps to a real owner/output rather than mirroring model subagents or tool calls.
- The design does not require AURA to authorize, schedule, or orchestrate execution.
