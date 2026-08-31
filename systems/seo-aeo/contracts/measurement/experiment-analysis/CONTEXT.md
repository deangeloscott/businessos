---
id: seo.measurement.experiment-analysis
type: playbook
version: 1.1.0
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
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# SEO/AEO Experiment Analysis

## Purpose
Analyze controlled or quasi-controlled experiments without overstating causality.

## Business Outcome
Improve valuable organic discovery through seo/aeo experiment analysis, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run when the configured measurement window closes, a report is due, or **seo/aeo experiment analysis** evidence becomes decision-relevant.

## Process
1. [HYBRID] Verify experiment hypothesis, treatment/control definition, assignment, start/end, guardrails, contamination, and pre-period comparability.
2. [DETERMINISTIC] Validate data completeness and whether external changes affected treatment/control differently.
3. [DETERMINISTIC] Compute predefined primary/secondary outcomes and uncertainty using an analysis appropriate to the design/data volume.
4. [HYBRID] Inspect heterogeneity by page type/market/query only when sample size/design supports it.
5. [AI] Classify support, contradiction, or inconclusive evidence and distinguish statistical from business significance.
6. [HYBRID] Update Experiment and Strategy/Brand evidence; do not promote a tactic from one weak test.

## Decisions / Routing
- Route → SEO Domain Learning / Core Business Learning as justified by outcome evidence.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


