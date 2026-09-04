---
id: customer-optimization.intervention.renewal
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  domain: customer-intelligence
- MetricObservation
writes: []
context:
- EconomicContext
- Offer
---
# Renewal Optimization

## Purpose
Make renewal decisions timely, informed, low-friction, and connected to demonstrated customer value.

## Business Outcome
Improve healthy renewal progression and value retention without masking unresolved value problems with process pressure or indiscriminate discounting.

## Run When
Use when renewal readiness, friction, risk, or process quality is a material customer/business issue. An existing Opportunity may provide context but is not required.

## Process
1. [HYBRID] Map the real renewal timeline, notice requirements, value review, decision stakeholders, procurement, pricing/terms, reminders, and failure states relevant to the business/customer segment. Draw on `customer-optimization.renewal.readiness` when its specialized method would improve the decision.
2. [AI] Combine usage/success/proof, customer expectations, objections, support/relationship evidence, and contract context to identify supported renewal barriers/opportunities without inventing motive. Use `customer-optimization.monitoring.renewal-risk` when a bounded pre-renewal risk evidence review would help; neither specialist method is a required execution step.
3. [AI] Separate process delay, unresolved value, pricing/Offer, relationship, competitive, procurement, and operational causes because they require different responses.
4. [AI] Design the smallest useful renewal approach with value evidence, decision preparation, appropriate Offer/terms handling, and escalation/recovery where genuinely needed.
5. [AI] Use Marketing, Content, Customer Intelligence, sales/customer-success, finance/legal, or other relevant operating knowledge/expertise directly when it improves the work. Create a WorkRequest only for a real durable handoff across actors/sessions/time.
6. [HYBRID] If execution is requested and the host has the real capability/permission, implement the relevant workflow/communication changes through the external systems. Otherwise return the actionable plan/assets without implying execution.
7. [HYBRID] Observe on-time renewal, revenue retention, discounting, churn, value realization, and customer-experience evidence when available. Preserve a ChangeEvent, Experiment, MetricObservation, OutcomeEvaluation, or Learning only when that meaning actually occurred and matters later.

## Completion Criteria
- The renewal mechanism and response are evidence-backed and usable, with execution/outcome state truthful and no mandatory AURA lifecycle objects.
