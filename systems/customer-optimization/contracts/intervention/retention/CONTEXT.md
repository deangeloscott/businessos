---
id: customer-optimization.intervention.retention
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes: []
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - customer_success.read
  - support.ticket.read
  - workflow.update
  - email.send
  - experiment.run
context:
- EconomicContext
- Offer
subcontracts:
  required:
  - customer-optimization.retention.risk-segmentation
  - customer-optimization.retention.intervention-plan
---
# Retention Optimization

## Purpose
Increase sustained customer value/continuation by improving the experience and outcomes that drive durable retention.

## Business Outcome
Improve durable retention through better value realization rather than temporary lock-in, indiscriminate discounting, or vanity retention metrics.

## Run When
Use when evidence suggests retention is a material constraint or opportunity. An existing Opportunity may provide context but is not required.

## Process
1. [HYBRID] Define the retention period/state appropriate to the business model and segment, including what constitutes healthy retained value.
2. [HYBRID] Compare retention across relevant cohorts and customer/value states while accounting for tenure, acquisition mix, seasonality, pricing/product changes, and censoring where they matter.
3. [AI] Identify plausible retention drivers and failure mechanisms using Customer Insights, behavioral/service evidence, outcomes, and economics without treating correlation as motive or cause.
4. [AI] Prioritize interventions that improve underlying value realization and relationship quality over temporary lock-in or blanket discounting.
5. [AI] Use whatever additional operating knowledge is relevant—customer success, communication, product/process, persuasion, service recovery, or other expertise—directly through the active model/harness. A WorkRequest is only for a real durable handoff.
6. [HYBRID] Define and, when evidence is available, evaluate retention, customer value, margin/LTV, satisfaction/support, and future expansion/referral guardrails proportionate to the intervention.
7. [AI] Persist only durable meanings that actually occurred and matter later, such as a real intervention/change, experiment, measured outcome, updated Insight, or Learning. Do not manufacture a lifecycle bundle.

## Completion Criteria
- The organization has an evidence-backed retention mechanism and useful intervention/decision, with execution and outcome state reported truthfully and no mandatory AURA lifecycle objects.
