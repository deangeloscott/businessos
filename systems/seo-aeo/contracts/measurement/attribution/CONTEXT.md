---
id: seo.measurement.attribution
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- MetricObservation
- Opportunity
- ChangeEvent
- Experiment
writes:
- MetricObservation
- Experiment
- Learning
- OutcomeEvaluation
- Opportunity
- ChangeEvent
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - revenue.read
  - ai_answer.observe
context:
- EconomicContext
- Market
- Objective
- Offer
---
# Organic Attribution

## Purpose
Connect observed organic discovery to business outcomes using the strongest available evidence while labeling uncertainty.

## Business Outcome
Improve valuable organic discovery through organic attribution, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run when the configured measurement window closes, a report is due, or **organic attribution** evidence becomes decision-relevant.

## Process
1. [HYBRID] Define the reporting attribution model(s) and canonical business outcomes from Brand Context.
2. [DETERMINISTIC] Join search/answer/local referral observations to analytics sessions/landing pages/events using available identifiers and time windows.
3. [DETERMINISTIC] Join downstream CRM/order/opportunity/revenue/profit where available, minimizing personal data in artifacts.
4. [HYBRID] Separate direct/last-touch, assisted, first-touch, modeled, survey/self-reported, and proxy attribution rather than combining them invisibly.
5. [HYBRID] Quantify unmatched/unknown outcomes and known biases such as dark/direct traffic, offline sales, long cycles, cross-device, and AI answers with no referral.
6. [HYBRID] Report business value with an attribution-confidence field and use proxy hierarchy only when stronger evidence is unavailable.

## Decisions / Routing
- Route → SEO Domain Learning / Core Business Learning as justified by outcome evidence.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


