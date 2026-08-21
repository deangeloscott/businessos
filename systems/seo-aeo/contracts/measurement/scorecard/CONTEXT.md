---
id: seo.measurement.scorecard
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
# Unified SEO/AEO Scorecard

## Purpose
Maintain a layered scorecard where intermediate metrics remain visible but never replace business value.

## Business Outcome
Improve valuable organic discovery through unified seo/aeo scorecard, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run when the configured measurement window closes, a report is due, or **unified seo/aeo scorecard** evidence becomes decision-relevant.

## Process
1. [HYBRID] Populate Business layer: profit/revenue/qualified opportunities/leads/conversions/assists or declared proxy.
2. [HYBRID] Populate Discovery layer: qualified organic traffic and value-weighted search/AI/local coverage.
3. [AI] Populate Search layer: impressions/clicks/CTR/position/query coverage/features; AI layer: mentions/recommendations/citations/cited assets/referrals.
4. [AI] Populate Authority/Reputation and Technical/Index layers with directly interpretable metrics rather than a single opaque score.
5. [HYBRID] Segment by strategic dimensions and compare with baseline/target/trend.
6. [AI] Display data quality, attribution confidence, and whether each metric is a goal, diagnostic, guardrail, or proxy.
7. [AI] Use scorecard changes to open diagnosis, not to automatically prescribe a tactic.

## Decisions / Routing
- Route → SEO Domain Learning / Core Business Learning as justified by outcome evidence.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


