---
id: customer-optimization.monitoring.churn-risk
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
# Customer Churn Risk Monitoring

## Purpose
Detect observable lifecycle conditions associated with elevated churn so the business can investigate and respond appropriately.

## Business Outcome
Surface actionable risk without opaque or sensitive profiling.

## Run When
Run on an appropriate cadence for active customers where early churn prevention is valuable.

## Process
1. [DETERMINISTIC] Use approved risk indicators grounded in prior Journey Insights/Learnings such as missed value milestones, unresolved failures, usage/adoption decline, support escalation, renewal issues, or explicit feedback.
2. [DETERMINISTIC] Calculate current indicator state and suppress duplicate alerts until material change/review condition occurs.
3. [AI] Classify the plausible actionable mechanism and distinguish data anomaly, expected seasonality, healthy lower usage, or customer lifecycle differences.
4. [HYBRID] Do not infer sensitive traits or use opaque scores without interpretable contributing factors.
5. [AI] Determine whether the next step is investigation, Customer Success/human outreach, service recovery, education, product/process fix, or no action.
6. [DETERMINISTIC] Create scoped risk Observation/Action only when threshold/evidence is met and record reason.
7. [DETERMINISTIC] Track whether risk resolved and use outcomes to recalibrate indicators.
