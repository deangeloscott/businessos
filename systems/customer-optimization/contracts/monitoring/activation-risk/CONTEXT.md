---
id: customer-optimization.monitoring.activation-risk
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
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Activation Risk Review

## Purpose
Review observable evidence that new customers/users may miss an important activation or value milestone while there is still time for the business to help.

## Business Outcome
Identify specific, interpretable activation barriers early enough to support useful intervention without turning AURA into an outreach/risk-scoring runtime.

## Run When
Use for a bounded activation-risk review when the user/current work needs it, when saved monitoring intent indicates another review would be useful, or when current journey evidence suggests activation is deteriorating. Any recurring execution or outreach workflow is owned by the active harness/operational systems.

## Process
1. [HYBRID] Resolve the relevant activation/value milestones, expected timing, customer/cohort scope, prior Learning, and evidence available from product, CRM, support, implementation, or other authorized systems. Prefer cohort/process analysis when individual-level review is unnecessary.
2. [HYBRID] Compare observed customer/cohort state with milestone timing, failures, dependencies, and support/implementation evidence using mechanical calculations only after the semantic milestone/scope is defined.
3. [AI] Judge plausible barriers only from observable evidence; distinguish not-yet-due states, deliberate pacing, missing/instrumentation data, expected variation, and credible activation risk.
4. [AI] Identify the least intrusive useful response class when action appears warranted—for example information gathering, human help, service/process repair, product guidance, or no action—without sending messages or changing workflows merely because this review ran.
5. [AI] Separate activation likelihood/evidence from customer value or commercial priority. Do not infer sensitive traits, use opaque individual scores, or let account value inflate inferred risk.
6. [HYBRID] Persist a material Observation/Insight and, only when a durable improvement/intervention is genuinely worth coordinating later, an Opportunity. Otherwise return the finding/recommendation directly without lifecycle state.
7. [AI] When future review matters, preserve semantic review intent/checkpoint context only when useful. The active harness/runtime or operational system owns actual recurrence, alerts, outreach, and workflow state.

## Verification
- Risk interpretation traces to observable activation/value evidence.
- Missing or delayed data is not silently treated as customer failure.
- Review output does not itself trigger outreach or workflow mutation.
- Any persisted Opportunity represents durable improvement work rather than an individual alert.

## Completion Criteria
- The organization understands whether meaningful activation risk exists, the likely evidence-backed barrier, and the smallest useful response class without requiring an AURA-owned automation loop.
