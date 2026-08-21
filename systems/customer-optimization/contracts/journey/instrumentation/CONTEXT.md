---
id: customer-optimization.journey.instrumentation
type: playbook
version: 1.1.0
owner_system: customer-optimization
risk: low
autonomy_ceiling: 4
reads:
- CustomerJourney
- type: Insight
  owner_system: customer-intelligence
- Observation
- MetricObservation
writes:
- CustomerJourney
- Observation
- Insight
- Opportunity
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - crm.opportunity.read
  - support.ticket.read
  - checkout.read
  - billing.read
  - customer_success.read
context:
- AudienceSegment
- Objective
- Offer
---
# Journey Instrumentation

## Purpose
Ensure customer transitions can be observed reliably enough to diagnose progression.

## Business Outcome
Improve customer progression and value realization through journey instrumentation, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires journey instrumentation to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Enumerate CustomerJourney stages/transitions and the exact event/state evidence needed to determine entry, progress, completion, failure, and time-to-next-stage.
2. [DETERMINISTIC] Inventory existing CRM/product/analytics/billing/support/scheduling events and data definitions.
3. [HYBRID] Identify missing, ambiguous, duplicated, delayed, or inconsistent signals and cross-system identity gaps.
4. [DETERMINISTIC] Define canonical event/metric definitions, identifiers, required dimensions, and data-quality checks.
5. [HYBRID] Prioritize instrumentation by decision value rather than tracking everything possible.
6. [INTEGRATION] Implement when authorized/capable or create Manual Action Packet.
7. [DETERMINISTIC] Verify event firing/state transitions and update journey instrumentation confidence.
