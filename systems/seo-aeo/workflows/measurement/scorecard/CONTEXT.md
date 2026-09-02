---
id: seo.measurement.scorecard
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
Create a layered view of organic-discovery performance where intermediate visibility metrics remain interpretable but never replace business value.

## Business Outcome
Help the organization understand whether organic/search/answer work is producing valuable outcomes, where change is occurring, and what deserves deeper diagnosis.

## Run When
Use when a current decision or review needs a consolidated SEO/AEO performance view and sufficiently current measurement evidence is available.

## Process
1. [HYBRID] Start with the strongest available business outcomes: profit/revenue/qualified opportunities/leads/conversions/assists or a clearly labeled proxy.
2. [HYBRID] Add qualified organic traffic and value-weighted search/AI/local discovery coverage only where they help explain the business result.
3. [HYBRID] Add interpretable search metrics (impressions, clicks, CTR, position, query coverage/features) and AI-answer observations (mentions, recommendations, citations, cited assets/referrals) at the relevant scope.
4. [HYBRID] Add authority/reputation and technical/index evidence only where it materially explains performance; do not collapse unlike dimensions into one opaque score.
5. [HYBRID] Segment by decision-relevant dimensions and compare with appropriate baseline/target/trend, keeping data quality and sample limitations visible.
6. [AI] Label each metric as business outcome, diagnostic, guardrail, or proxy and state attribution/measurement uncertainty.
7. [AI] Interpret material changes and identify the smallest useful next question. Relevant diagnosis, Learning, or Opportunity methods are optional next choices for the model/user, not automatic routes from the scorecard.
8. [DETERMINISTIC] Persist new normalized MetricObservations only when they add durable reusable measurement meaning rather than duplicating source data already represented elsewhere.

## Verification
- Business outcomes and proxies are clearly distinguished.
- Surface-specific measurements remain separate enough to interpret.
- Scorecard changes do not automatically create Opportunities, Learning, experiments, or runtime work.

## Completion Criteria
- A decision-maker can see what organic discovery contributed, what changed, how reliable the evidence is, and what deserves attention without a routing lifecycle or opaque composite score.
