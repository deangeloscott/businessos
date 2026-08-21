---
id: customer-optimization.measurement.transition
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
# Journey Transition Measurement

## Purpose
Measure progression from one defined customer state to the next with consistent eligibility, timing, and outcome rules.

## Business Outcome
Make journey bottlenecks and intervention effects observable.

## Run When
Run when a CustomerJourney transition is created, changed, monitored, or evaluated.

## Process
1. [DETERMINISTIC] Define source state, target state, eligible population, entry timestamp, success event, failure/timeout, and observation window.
2. [DETERMINISTIC] Validate event/source data for duplicates, missing events, ordering, identity, timezone, and late-arriving data.
3. [DETERMINISTIC] Calculate entered, completed, failed/expired, still-in-progress, rate, elapsed time distribution, and relevant dimensions.
4. [AI] Identify where metric definition could reward wrong behavior or exclude meaningful customer outcomes.
5. [HYBRID] Separate intended qualification/filtering from undesired abandonment.
6. [DETERMINISTIC] Persist MetricObservations with cohort/definition/version so comparisons remain valid.
7. [AI] Flag anomalies or structural changes for diagnosis rather than automatically creating interventions.
