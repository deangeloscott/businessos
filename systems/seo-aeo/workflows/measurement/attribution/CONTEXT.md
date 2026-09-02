---
id: seo.measurement.attribution
type: workflow
owner_system: seo-aeo
reads:
- MetricObservation
- Opportunity
- ChangeEvent
- Experiment
writes:
- MetricObservation
context:
- EconomicContext
- Market
- Objective
- Offer
---
# Organic Attribution

## Purpose
Connect observed organic discovery to business outcomes using the strongest available evidence while making attribution uncertainty explicit.

## Business Outcome
Help the organization understand how organic/search/answer discovery contributes to real business value without pretending ambiguous attribution is causal proof.

## Run When
Use when a decision needs an attribution view of organic discovery and the relevant business/measurement evidence is available enough to support one.

## Process
1. [AI] Define the business outcome and attribution question actually needed for the decision; do not force one attribution model onto every use case.
2. [DETERMINISTIC] Join search/answer/local referral observations to analytics sessions/landing pages/events when reliable identifiers and time windows make the linkage mechanical.
3. [DETERMINISTIC] Join downstream CRM/order/opportunity/revenue/profit only where stable identifiers permit it, minimizing personal data in AURA artifacts.
4. [HYBRID] Keep direct/last-touch, assisted, first-touch, modeled, survey/self-reported, and proxy attribution distinct instead of combining them invisibly.
5. [HYBRID] Quantify unmatched/unknown outcomes and material biases such as dark/direct traffic, offline sales, long cycles, cross-device behavior, and AI answers with no referral.
6. [AI] State what the evidence supports about contribution, what remains uncertain, and which conclusions are only directional. Never promote association into causality without a design that supports it.
7. [DETERMINISTIC] Persist new durable MetricObservations only when the normalized attribution result will materially help future work; otherwise return the analysis without manufacturing canonical state.

## Verification
- Attribution method and uncertainty are visible near the conclusion.
- Stronger first-party/business evidence is preferred over weaker proxies when available.
- Attribution results do not automatically create Learning, Opportunities, or downstream work.

## Completion Criteria
- The organization can understand the strongest defensible relationship between organic discovery and business outcomes, including material unknowns and bias, without a routing layer.
