---
id: customer-optimization.monitoring.renewal-risk
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
  - billing.read
  - support.ticket.read
  - customer_success.read
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Renewal Risk Review

## Purpose
Review observable customer/account conditions that could prevent a healthy renewal while there is still time to resolve real value, service, contract, or decision-process problems.

## Business Outcome
Improve renewal readiness through evidence-backed understanding and customer value rather than coercive retention tactics or an AURA-owned renewal workflow.

## Run When
Use for a bounded renewal-readiness/risk review when the user/current work needs it, when a material renewal decision approaches, or when saved monitoring intent indicates another review would be useful. Any recurring execution, reminders, outreach, or account workflow is owned by the active operational system/harness.

## Process
1. [HYBRID] Resolve the relevant renewal date/terms, value/adoption outcomes, open service/support issues, stakeholder/account changes, billing/contract conditions, prior renewal evidence, and customer/cohort scope from authorized sources. Use only the level of individual detail actually needed for the decision.
2. [AI] Identify observable renewal risks such as unrealized value, unresolved failure, stakeholder loss, low adoption tied to value, fit change, budget/term friction, competitor consideration, or decision-process delay. Preserve unknowns instead of filling them with generic churn assumptions.
3. [AI] Distinguish evidence of renewal risk from ordinary usage variation, seasonality, customer lifecycle differences, missing data, or deliberate lower use. Do not use cancellation friction, dark patterns, or account value as evidence that renewal is more or less likely.
4. [AI] Separate the likely problem mechanism from the team/tool that may eventually address it. Suggest useful response classes—such as customer-success help, service recovery, value clarification, commercial review, product/process repair, or no action—without creating AURA routing/ownership state.
5. [AI] Identify any genuine external date/dependency that matters to the decision. Preserve it as organizational context when future work benefits; do not turn it into an AURA scheduler or artificial deadline lifecycle.
6. [HYBRID] Persist a material Observation/Insight and, only when a durable improvement/intervention is genuinely worth coordinating later, an Opportunity. Otherwise return the finding/recommendation directly.
7. [AI] Later renewal outcomes may support domain Learning when enough comparable evidence exists. Do not automatically promote one account outcome into a reusable rule.

## Verification
- Renewal-risk conclusions trace to observable customer/account evidence.
- Customer value, account economics, and inferred renewal likelihood remain distinct concepts.
- Review output does not itself send outreach, alter workflows, or create scheduler state.
- Any persisted Opportunity represents durable improvement work rather than an individual alert/task.

## Completion Criteria
- The organization understands whether meaningful renewal risk exists, the likely evidence-backed mechanism, material dates/unknowns, and the smallest useful response class without relying on an AURA-owned renewal automation loop.
