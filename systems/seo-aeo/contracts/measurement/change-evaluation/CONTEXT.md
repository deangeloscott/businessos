---
id: seo.measurement.change-evaluation
type: playbook
owner_system: seo-aeo
reads:
- MetricObservation
- Opportunity
- ChangeEvent
- Experiment
writes:
- MetricObservation
- OutcomeEvaluation
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
# Change Evaluation

## Purpose
Evaluate whether a specific SEO/AEO change likely helped, harmed, had little effect, or remains inconclusive without overstating causality.

## Business Outcome
Improve future organic-discovery decisions by turning executed changes into evidence rather than anecdotes.

## Run When
Use when a material change has enough post-change evidence to evaluate, or when a severe negative signal justifies an earlier bounded review. If the evidence window is not mature enough, say so; AURA does not wait or schedule the future check itself.

## Process
1. [HYBRID] Resolve the ChangeEvent/change evidence, hypothesis, affected scope, before state, intended outcome, guardrails, and any measurement design actually used.
2. [AI] Judge whether enough evidence exists for the intended evaluation. Preserve the remaining measurement condition/checkpoint when useful instead of manufacturing a conclusion.
3. [INTEGRATION] Retrieve relevant post-change business/search/AI/local/technical observations and verify that measurement inputs are usable.
4. [HYBRID] Account for demand, seasonality, concurrent changes, market/device mix, position/SERP shifts, and other plausible confounders using only adjustments the evidence/design can support.
5. [AI] Classify the result as supported improvement, supported harm, neutral/no material effect, or inconclusive; state effect size/range and causal confidence separately.
6. [HYBRID] Persist an OutcomeEvaluation and material supporting MetricObservations when future work benefits. Recommend rollback/replanning or another next method when warranted, but the active user/harness owns any actual change.
7. [AI] Promote reusable Learning only through the appropriate evidence-based Learning path when the result is sufficiently strong and scoped; one change does not automatically become a rule.

## Verification
- Before/after association is not presented as causality without supporting design/evidence.
- Confounders and measurement limitations remain visible.
- Recommended reversal/replanning is distinct from action actually executed.

## Completion Criteria
- The organization has a calibrated reusable evaluation of the change and knows what, if anything, the evidence warrants next without automatic routing.
