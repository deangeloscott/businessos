---
id: seo.measurement.experiment-analysis
type: workflow
owner_system: seo-aeo
reads:
- MetricObservation
- Opportunity
- ChangeEvent
- Experiment
- Observation
writes:
- MetricObservation
- Experiment
- OutcomeEvaluation
context:
- EconomicContext
- Market
- Objective
- Offer
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# SEO/AEO Experiment Analysis

## Purpose
Analyze controlled or defensible quasi-controlled SEO/AEO experiments without overstating causality or generalizing beyond the tested context.

## Business Outcome
Turn experiments into reusable decision evidence about what helped, harmed, or remains uncertain for this organization.

## Run When
Use when an SEO/AEO experiment has enough outcome evidence for its planned analysis or a guardrail result requires a bounded early review.

## Process
1. [HYBRID] Verify the actual hypothesis, treatment/control definition, assignment, start/end, guardrails, contamination, and pre-period comparability.
2. [HYBRID] Check data completeness and whether external changes affected treatment/control or comparison groups differently.
3. [DETERMINISTIC] Compute the predefined primary/secondary outcomes and uncertainty using the analysis chosen for the actual design/data; do not switch methods merely to obtain significance.
4. [HYBRID] Inspect heterogeneous effects only when the sample/design supports them and when they matter to the decision.
5. [AI] Classify support, contradiction, neutral/no material effect, or inconclusive evidence; distinguish statistical uncertainty, practical/business significance, and causal confidence.
6. [HYBRID] Preserve the Experiment result, supporting MetricObservations, and an OutcomeEvaluation with assumptions/limitations. Do not automatically create an Opportunity or change operating guidance.
7. [AI] If the result supports reusable scoped guidance, use the evidence-based Learning path separately; if it suggests another experiment or intervention, that remains a model/user choice.

## Verification
- Analysis follows the actual design rather than retrofitting a preferred conclusion.
- Statistical and business significance remain distinct.
- One weak or context-specific experiment is not promoted into universal guidance.

## Completion Criteria
- The experiment result is inspectable, calibrated, and reusable, with any next method left to capable model/user judgment.
