---
id: customer-optimization.monitoring.churn-risk
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
  - revenue.read
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
Detect observable lifecycle conditions associated with elevated churn so the business can investigate and respond appropriately, while distinguishing likelihood of loss from the value/consequence at risk.

## Business Outcome
Surface actionable, interpretable risk early and prioritize responsible response without opaque/sensitive profiling or treating account value as churn probability.

## Run When
Run on an appropriate cadence for active customers where early churn prevention is valuable.

## Process
1. [DETERMINISTIC] Use approved risk indicators grounded in prior Journey/Customer Insights/Learnings such as missed value milestones, unresolved failures, usage/adoption decline, support escalation, renewal issues, billing/process problems, or explicit feedback.
2. [DETERMINISTIC] Calculate current indicator state and suppress duplicate alerts until material change/review condition occurs.
3. [AI] Classify the plausible actionable mechanism and distinguish data anomaly, expected seasonality, healthy lower usage, customer lifecycle differences, deliberate reduced need, or actual deterioration.
4. [HYBRID] Keep risk likelihood/evidence separate from consequence/value-at-risk. Revenue, LTV, margin, strategic importance, or customer value may help prioritize attention only after a risk is supported; high account value must never increase the inferred probability of churn by itself.
5. [HYBRID] Do not infer sensitive traits or use opaque scores without interpretable contributing factors. Preserve uncertainty and avoid individual profiling where cohort/process monitoring is sufficient.
6. [AI] Determine whether the next step is investigation, Customer Success/human outreach, service recovery, education, product/process fix, commercial/renewal review, or no action. Prioritize restoration of customer value over manipulative retention.
7. [DETERMINISTIC] Create scoped risk Observation/Action only when threshold/evidence is met and record the contributing factors, confidence, and any separately calculated value-at-risk.
8. [DETERMINISTIC] Track whether risk resolved, whether customer value was restored, and use outcomes to recalibrate indicators without converting one rescue into a universal rule.
