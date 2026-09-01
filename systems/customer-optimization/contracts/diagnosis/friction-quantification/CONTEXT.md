---
id: customer-optimization.diagnosis.friction-quantification
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
# Journey Friction Quantification

## Purpose
Measure the size, location, and customer/business cost of a known friction condition.

## Business Outcome
Give prioritization a defensible estimate of how much the friction matters.

## Run When
Run after friction is observed and before major intervention effort when impact is not already clear.

## Process
1. [DETERMINISTIC] Define the friction event/state and affected transition, population, period, and success comparison.
2. [DETERMINISTIC] Measure incidence, drop-off, added time/steps, errors, retries, support contacts, abandonment, and downstream outcome differences where available.
3. [AI] Separate customers for whom the step is intentionally qualifying/required from customers harmed by avoidable friction.
4. [DETERMINISTIC] Estimate affected volume and customer/business impact using ranges where causal attribution is uncertain.
5. [AI] Identify data gaps and whether the friction is concentrated by segment/device/channel/plan/process owner.
6. [HYBRID] Avoid assigning all outcome difference to the friction when customers self-select into it.
7. [AI] Attach quantified impact/confidence to the Opportunity/Insight.
