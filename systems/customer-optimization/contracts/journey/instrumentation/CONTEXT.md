---
id: customer-optimization.journey.instrumentation
type: playbook
owner_system: customer-optimization
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
Determine whether customer transitions can be observed reliably enough for the current progression decision, and improve the real measurement setup when the user has requested that work.

## Business Outcome
Make journey diagnosis and outcome measurement trustworthy without turning AURA into the canonical telemetry/event platform.

## Run When
When a customer-journey decision depends on transition evidence that may be missing, ambiguous, inconsistent, or unreliable.

## Process
1. [AI] Identify the journey stages/transitions and the smallest event/state evidence needed to answer the current question: entry, progress, completion, failure, time-to-next-stage, or another decision-relevant condition.
2. [HYBRID] Inspect the actual available CRM/product/analytics/billing/support/scheduling evidence and its definitions through the active harness. Reuse authoritative source semantics instead of copying entire event systems into AURA.
3. [HYBRID] Identify missing, ambiguous, duplicated, delayed, or inconsistent signals and cross-system identity/coverage gaps that could materially change the decision.
4. [AI] Define the measurement meaning AURA needs—metric/event concept, population, dimensions, units, timing, and quality requirements—without pretending AURA owns provider-specific event names, schemas, identifiers, joins, or implementation details.
5. [AI] Prioritize instrumentation by decision value rather than tracking everything possible.
6. [INTEGRATION] When implementation is inside the user's requested action scope and the active harness has the necessary capability/access, make the smallest useful change in the system that actually owns the instrumentation. Respect real organizational/platform/account constraints; do not require an AURA approval object. If implementation cannot be completed, preserve the concrete measurement gap and create a durable handoff only when another actor genuinely needs to continue it.
7. [HYBRID] Observe enough resulting data/state to determine whether the needed transition evidence is now trustworthy. Persist only the bounded organizational meaning—such as journey measurement confidence, a material Observation/Insight, or a genuine Opportunity—that future work benefits from.

## Verification
- AURA can state what evidence is required, what real source supplies it, what quality limitations remain, and how those limitations affect the business decision.
- Provider-specific telemetry remains owned by the external system rather than duplicated as an AURA control plane.
- No Manual Action Packet or internal authorization lifecycle is required.

## Completion Criteria
- The journey question has adequate trustworthy measurement evidence, or the exact unresolved instrumentation gap and its decision consequence are explicit.
