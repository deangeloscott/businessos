---
id: customer-optimization.retention.risk-segmentation
type: workflow
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
2. [DETERMINISTIC] Assign customers/accounts only using observable approved indicators and retain contributing factors in the real operational analysis where individual-level state is appropriate.
3. [AI] Distinguish transient/expected behavior from persistent risk and identify customers fitting multiple mechanisms.
4. [HYBRID] Avoid sensitive/protected-trait inference and do not create pseudo-psychographic risk labels from weak data.
5. [DETERMINISTIC] Compare historical churn/retention and intervention response by mechanism with confidence/volume.
6. [AI] Identify the appropriate intervention and real responsible function/process for each mechanism; use relevant operating knowledge directly rather than assigning the work to an internal AURA domain.
7. [HYBRID] Preserve only the durable risk understanding, evidence, expiry/review intent, or Opportunity that future organizational work benefits from. Any active risk queue, recurring review, notification, or duplicate-action suppression belongs to the real CRM/runtime/harness.
