---
id: customer-optimization.renewal.readiness
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
# Renewal Readiness Assessment

## Purpose
Determine whether a customer is ready to renew and what legitimate issues must be resolved before the decision.

## Business Outcome
Improve healthy renewal by making value, fit, terms, and unresolved risks visible early.

## Run When
Run during the pre-renewal window before renewal outreach/decision.

## Process
1. [DETERMINISTIC] Compile value/adoption outcomes, success goals, usage/service delivery, open issues, support, stakeholder/account state, current terms/price, billing, and renewal date/process.
2. [AI] Assess evidence of realized value, unresolved blockers, changed needs, fit, stakeholder alignment, and decision process.
3. [AI] Identify missing proof/value recap the customer may need and distinguish actual product/service issues from communication gaps.
4. [HYBRID] Route commercial negotiation/sales-owned renewal discussion to the appropriate future/human owner while Customer Optimization handles process/value friction.
5. [AI] Define required pre-renewal actions and latest-useful dates.
6. [DETERMINISTIC] Track completion/readiness and suppress conflicting automated outreach.
7. [AI] Use renewal outcome to refine risk/readiness Learning.
