---
id: customer-optimization.measurement.time-to-value
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
# Time-to-Value Analysis

## Purpose
Measure how long it takes customers to reach a genuinely meaningful value milestone and what delays it.

## Business Outcome
Reduce the time between commitment/start and customer-realized value without substituting vanity activation events.

## Run When
Run when onboarding, implementation, adoption, retention, or customer success depends on speed to meaningful value.

## Process
1. [AI] Define the first meaningful customer value milestone using Customer Insights, product/service reality, and retention/success evidence—not the easiest trackable event.
2. [DETERMINISTIC] Map start event, required milestones, timestamps, successful/failed/censored cases, and segment/context.
3. [DETERMINISTIC] Calculate median/distribution/percentiles and milestone-level elapsed/wait/active effort time.
4. [AI] Compare fast versus slow value cases and identify delays caused by customer effort, internal handoff, technical dependency, education, fit, capacity, or policy.
5. [AI] Test which milestone delays actually predict success/retention rather than assuming all speed is valuable.
6. [HYBRID] Avoid optimizing speed by skipping necessary qualification, setup quality, safety, or customer learning.
7. [AI] Publish Journey Insight/Opportunity and define TTV measurement for interventions.
