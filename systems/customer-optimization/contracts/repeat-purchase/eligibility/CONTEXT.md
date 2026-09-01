---
id: customer-optimization.repeat-purchase.eligibility
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
# Repeat Purchase Eligibility

## Purpose
Determine when an existing customer has a legitimate need and readiness for another purchase of the same/replenishable offering.

## Business Outcome
Prompt repeat purchase when it benefits the customer rather than simply because time has passed.

## Run When
Run for business models with repeat purchase and sufficient consumption/need/timing evidence.

## Process
1. [DETERMINISTIC] Define the expected consumption/replenishment/use cycle, prior purchase, usage/consumption evidence where available, eligibility, satisfaction/issues, and product availability.
2. [AI] Identify signals that the customer is likely approaching renewed need versus still holding/using the prior purchase.
3. [AI] Exclude customers with unresolved service/product issues, ineligible status, excess recent purchase, or evidence the offering is not appropriate.
4. [HYBRID] Avoid exploiting health/sensitive inference or repeated pressure where need is uncertain.
5. [AI] Select appropriate reminder/reorder convenience versus promotional persuasion based on evidence.
6. [DETERMINISTIC] Trigger the correct journey/Marketing WorkRequest with suppression and measurement.
7. [AI] Evaluate repeat rate, returns/complaints, and customer value rather than sends/clicks alone.
