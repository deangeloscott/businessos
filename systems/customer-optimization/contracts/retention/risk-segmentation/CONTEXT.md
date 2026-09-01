---
id: customer-optimization.retention.risk-segmentation
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
# Retention Risk Segmentation

## Purpose
Group retention risk by interpretable mechanism so interventions can address the actual reason for risk.

## Business Outcome
Avoid treating all at-risk customers as one segment or relying on opaque churn scores.

## Run When
Run when retention monitoring identifies meaningful recurring risk patterns.

## Process
1. [AI] Define candidate risk mechanisms from Journey/Customer Insights: unrealized value, low adoption, service failure, fit change, price/terms, unresolved support, stakeholder change, product dependency, renewal process, or competitor switching.
2. [DETERMINISTIC] Assign customers/accounts only using observable approved indicators and retain contributing factors.
3. [AI] Distinguish transient/expected behavior from persistent risk and identify customers fitting multiple mechanisms.
4. [HYBRID] Avoid sensitive/protected-trait inference and do not create pseudo-psychographic risk labels from weak data.
5. [DETERMINISTIC] Compare historical churn/retention and intervention response by mechanism with confidence/volume.
6. [AI] Define the appropriate intervention owner/path for each mechanism.
7. [DETERMINISTIC] Maintain risk state with expiry/review and duplicate-action suppression.
