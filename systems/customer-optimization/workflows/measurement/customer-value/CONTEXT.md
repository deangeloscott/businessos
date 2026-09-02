---
id: customer-optimization.measurement.customer-value
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Observation
- Insight
- MetricObservation
- OutcomeEvaluation
- Opportunity
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
# Customer Value and Relationship Economics

## Purpose
Understand which customer relationships, segments, or cohorts create durable customer-realized value and sustainable business value, and where value is being created, lost, or put at risk.

## Business Outcome
Improve retention, service, acquisition quality, and responsible expansion using mutually valuable relationship economics rather than raw revenue, account size, or activity alone.

## Run When
Run when the business needs to understand customer ROI/value realization, LTV, profitability/cost-to-serve, high-value customer patterns, value-at-risk, cohort economics, expansion quality, or another lifecycle economic question.

## Process
1. [DETERMINISTIC] Define the unit of analysis (customer/account/contract/segment/cohort), eligibility, observation window, start/end events, censoring rules, currency/economic definitions, and the specific business/customer decision before calculating value.
2. [HYBRID] Resolve available evidence for customer outcomes/value milestones, adoption/usage, tenure/retention/renewal, revenue/expansion, gross margin or contribution when actually known, direct/allocated cost-to-serve where defensible, support burden, acquisition cost when attributable, referrals, and other relevant relationship signals. Preserve missing/estimated fields explicitly.
3. [DETERMINISTIC] Calculate only metrics supported by consistent definitions/data. LTV, CAC/payback, NRR, gross/contribution margin, customer ROI, value-at-risk, or profitability must not be fabricated from incomplete components; use ranges/partial views where justified and otherwise keep them unknown.
4. [AI] Compare customers/cohorts/segments across both customer-realized value and business economics. Identify patterns associated with durable mutual value, poor fit, service burden, successful expansion, or preventable leakage without treating high spend alone as “best customer.”
5. [AI] Test cohort composition, acquisition-source differences, tenure, seasonality, pricing/product changes, survivorship, service model, and other plausible confounders before interpreting differences.
6. [HYBRID] Separate **risk likelihood** from **value/consequence at risk**. A valuable account may deserve faster attention when an evidence-backed risk exists, but its value does not itself establish churn probability or justify manipulative retention.
7. [AI] Link relevant Customer Insights (why customers value/leave/expand) to observed behavioral/economic patterns while preserving correlation-versus-causation limits.
8. [AI] Produce evidence-backed Journey/Customer Optimization Insights and, when warranted, a prioritized Opportunity for onboarding, success, service recovery, retention, acquisition-quality feedback, expansion, or another correctly owned intervention.
9. [HYBRID] Protect privacy and fairness: avoid sensitive-trait inference, opaque customer scoring, or punitive treatment based on predicted value. Prefer interpretable contributing factors and aggregate/cohort analysis where individual-level action is unnecessary.

## Verification
- Every reported metric has an explicit definition, denominator/window, source, and known limitations.
- Customer outcome/value realization is not replaced by revenue alone.
- Estimated economics are labeled and not silently promoted to first-party fact.
- Association is not presented as causal effect without appropriate design/evidence.

## Completion Criteria
- The organization has a decision-useful, evidence-bounded view of customer and business value, with unknowns explicit and any intervention routed to the correct semantic owner.
