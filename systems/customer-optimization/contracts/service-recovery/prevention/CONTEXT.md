---
id: customer-optimization.service-recovery.prevention
type: playbook
version: 1.3.0
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
# Service Failure Prevention Review

## Purpose
Turn recurring or material service recovery cases into systemic journey/process improvements.

## Business Outcome
Reduce recurrence rather than repeatedly handling the same customer failure case-by-case.

## Run When
Run after a material recovery is stabilized or when similar incidents/complaints recur.

## Process
1. [DETERMINISTIC] Aggregate linked recovery cases, incidents, process state, affected journey transition, recent changes, and recurrence pattern.
2. [AI] Identify primary/contributing system/process/ownership/product/communication causes and escape points where the issue should have been prevented/detected.
3. [AI] Distinguish one-off execution error from structural process/design weakness.
4. [AI] Design prevention/detection changes beginning upstream of the customer-facing failure.
5. [HYBRID] Route product/engineering/sales/finance/legal root causes to the correct owner while retaining journey impact evidence.
6. [DETERMINISTIC] Define corrective Action/Change, verification, monitoring, and recurrence metric.
7. [AI] Evaluate post-change recurrence and promote Learning when evidence supports it.
