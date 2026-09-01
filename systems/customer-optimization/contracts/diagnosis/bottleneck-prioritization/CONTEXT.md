---
id: customer-optimization.diagnosis.bottleneck-prioritization
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
# Journey Bottleneck Prioritization

## Purpose
Identify which customer journey transition is most worth improving now.

## Business Outcome
Focus optimization on the bottleneck with the largest realistic customer and business effect rather than the most visible metric.

## Run When
Run when several journey stages show friction, drop-off, delay, or risk and one must be prioritized.

## Process
1. [DETERMINISTIC] Calculate transition volume, conversion, delay/time-in-state, downstream value, support burden, and trend by relevant cohort.
2. [AI] Identify where observed loss/delay is both material and potentially addressable, distinguishing expected qualification/filtering from harmful friction.
3. [AI] Evaluate downstream consequence: activation, time-to-value, retention, revenue, cost-to-serve, customer success, and experience.
4. [AI] Consider confidence, intervention leverage, dependencies, reversibility, and whether another domain actually owns the root cause.
5. [HYBRID] Avoid prioritizing solely by largest percentage drop where volume/value/customer intent differs.
6. [DETERMINISTIC] Rank candidate bottlenecks with transparent components/ranges and attach baseline evidence.
7. [AI] Create/refresh Optimization Opportunities only for qualified bottlenecks.
