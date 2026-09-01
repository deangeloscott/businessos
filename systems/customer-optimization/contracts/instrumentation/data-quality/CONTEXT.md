---
id: customer-optimization.instrumentation.data-quality
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
# Journey Instrumentation Data Quality

## Purpose
Verify that journey events, identities, states, and metrics are trustworthy enough for optimization decisions.

## Business Outcome
Prevent false bottlenecks and intervention conclusions caused by broken tracking or inconsistent state definitions.

## Run When
Run when onboarding a journey, after instrumentation changes, or when metrics conflict with operational/customer evidence.

## Process
1. [DETERMINISTIC] Inventory required journey states/events, source systems, IDs, timestamps/timezones, properties, joins, eligibility, and MetricDefinitions.
2. [DETERMINISTIC] Test event presence, duplicates, ordering, late arrival, identity resolution, missing values, schema/version drift, and source totals.
3. [AI] Compare instrumented path with how the process actually works, including offline/human steps and exceptions.
4. [DETERMINISTIC] Reconcile key counts with independent sources where possible and quantify untracked/ambiguous population.
5. [HYBRID] Block high-confidence diagnosis when missing/broken tracking could plausibly explain the signal.
6. [DETERMINISTIC] Create instrumentation repair Actions/WorkRequests and verification checks.
7. [DETERMINISTIC] Document valid measurement windows/limitations and re-baseline after material fixes.
