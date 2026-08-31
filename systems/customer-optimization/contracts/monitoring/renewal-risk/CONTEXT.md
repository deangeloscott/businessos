---
id: customer-optimization.monitoring.renewal-risk
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
# Renewal Risk Monitoring

## Purpose
Identify customer conditions that could prevent a healthy renewal before the decision deadline.

## Business Outcome
Create enough time to resolve real value, service, contract, or decision-process issues without coercive renewal tactics.

## Run When
Run during the business-specific pre-renewal window for renewable customers.

## Process
1. [DETERMINISTIC] Resolve renewal date/terms, value/adoption outcomes, open issues, support/service state, stakeholder/account changes, billing/contract conditions, and prior renewal history.
2. [AI] Identify observable risks: unrealized value, unresolved issue, stakeholder loss, low adoption, fit change, budget/term friction, competitor consideration, or process delay.
3. [AI] Separate issues Customer Optimization can address from Sales/Customer Success/Finance/Product/human-owned work.
4. [HYBRID] Avoid assuming lower usage alone means churn or using cancellation friction/dark patterns.
5. [AI] Build an intervention/readiness plan with responsible owners and latest-useful dates.
6. [DETERMINISTIC] Track risk state/actions/outcomes and avoid duplicate/conflicting outreach.
7. [AI] Feed renewal outcomes back into retention/risk Learning.
