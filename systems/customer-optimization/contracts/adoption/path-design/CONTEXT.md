---
id: customer-optimization.adoption.path-design
type: playbook
version: 1.3.0
owner_system: customer-optimization
risk: medium
autonomy_ceiling: 2
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
- ActionPacket
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
# Adoption Path Design

## Purpose
Define how customers progress from first value to sustained use of the capabilities/actions required for their desired outcomes.

## Business Outcome
Increase durable value realization without optimizing feature usage for its own sake.

## Run When
Run when customers activate but fail to adopt behaviors/capabilities necessary for ongoing success.

## Process
1. [AI] Define target customer outcome and the minimum recurring/advanced capabilities or behaviors causally/reliably associated with it.
2. [DETERMINISTIC] Map current adoption states, prerequisite skills/configuration/data, usage patterns, barriers, and successful-customer paths.
3. [AI] Sequence adoption milestones by customer value/dependency rather than product menu order.
4. [AI] Identify where simplification, defaults, in-product guidance, Content, Customer Success, or product/process change is needed.
5. [HYBRID] Avoid forcing usage that does not improve customer outcomes or inflating “adoption” by meaningless clicks.
6. [DETERMINISTIC] Define milestone instrumentation, success/guardrail metrics, timing, and segment variations.
7. [AI] Create intervention plan and evaluate downstream value/retention, not feature usage alone.
