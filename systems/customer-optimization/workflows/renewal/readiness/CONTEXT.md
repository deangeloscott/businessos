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
4. [HYBRID] When commercial negotiation or sales-owned renewal decisions are material, use the relevant sales/commercial expertise or real organizational owner directly while this method stays focused on process/value readiness; do not route work through an internal AURA domain.
5. [AI] Define the concrete pre-renewal work and latest-useful dates in the real process.
6. [DETERMINISTIC] Observe completion/readiness and suppress conflicting automated outreach in the real customer/renewal system when the active harness has that capability and authorization.
7. [AI] When renewal outcome evidence becomes available, preserve scoped risk/readiness Learning if it materially improves future work.
