---
id: customer-optimization.monitoring.journey-health
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- MetricObservation
- Observation
- ChangeEvent
- Learning
writes:
- Observation
- Insight
- Incident
- Opportunity
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - checkout.read
  - billing.read
  - customer_success.read
---
# Customer Journey Health Monitoring

## Purpose
Continuously detect material deterioration or improvement in customer progression, delays, failure states, or downstream value.

## Business Outcome
Improve customer progression and value realization through customer journey health monitoring, while protecting customer and business guardrails.

## Run When
Run on the configured lifecycle monitoring cadence and after material product/process/offer changes.

## Process
1. [DETERMINISTIC] Refresh transition metrics, time-to-stage, failure/error, retention/renewal/expansion, and configured guardrails for eligible journeys.
2. [DETERMINISTIC] Compare recent, prior, seasonal/cohort, and expected ranges at segment/offer/channel dimensions with minimum sample rules.
3. [HYBRID] Separate instrumentation/data-health changes from real customer behavior before escalation.
4. [AI] Identify affected transition scope and recent ChangeEvents/Industry/Marketing/Product context that may explain movement.
5. [HYBRID] Classify normal variation, watch, Optimization Opportunity candidate, or Incident based on magnitude/customer harm/business risk.
6. [DETERMINISTIC] Publish observations and emit material journey-health events; avoid automatically changing workflows without diagnosis.
