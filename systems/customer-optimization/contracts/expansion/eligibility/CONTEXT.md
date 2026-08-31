---
id: customer-optimization.expansion.eligibility
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
# Customer Expansion Eligibility

## Purpose
Identify when an existing customer has achieved enough value and has a genuine additional need for expanded scope/capability.

## Business Outcome
Create expansion from customer success and fit instead of premature upselling.

## Run When
Run when expansion/upsell/cross-sell is a valid business motion.

## Process
1. [DETERMINISTIC] Resolve customer goals, current Offer/product/service, realized outcomes, usage/adoption, limits, support/issues, additional needs, account/stakeholder context, and eligible expansion options.
2. [AI] Identify a specific unmet/next-stage job that the additional Offer can credibly solve.
3. [AI] Confirm current value realization and absence of unresolved problems that make expansion inappropriate.
4. [HYBRID] Avoid inferring needs from sensitive data or treating high spend/value alone as eligibility.
5. [AI] Explain expected incremental outcome, required effort/change, fit, and evidence needed for a responsible expansion conversation.
6. [DETERMINISTIC] Create a scoped expansion signal/WorkRequest to Marketing/Sales/human owner with reason and expiry.
7. [AI] Track outcome and whether expansion improved customer value/retention, not only revenue.
