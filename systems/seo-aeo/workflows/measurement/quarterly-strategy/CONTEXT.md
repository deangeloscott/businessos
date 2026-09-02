---
id: seo.measurement.quarterly-strategy
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
---
# Organic Discovery Strategy Review

## Purpose
Reassess organic-discovery markets, demand, competitors, asset portfolio, strategy evidence, and investment direction over a strategically meaningful horizon.

## Business Outcome
Keep SEO/AEO strategy aligned with current business value and evidence instead of preserving tactics because they were previously selected.

## Run When
Use when the organization needs a strategic organic-discovery review across a sufficiently meaningful period. Quarterly is a common horizon, not an AURA-owned schedule.

## Process
1. [HYBRID] Reuse current Business/Brand/Offer/Audience/Market/Objectives and identify changes that materially alter the strategy question.
2. [HYBRID] Review business value and longer-term organic contribution against Objectives, including where conclusions still rely on proxies.
3. [AI] Reassess the demand universe, competitor types, answer/search/local surfaces, topic/asset coverage, authority/reputation, and technical architecture at the depth that could change strategy.
4. [AI] Review which intervention mechanisms have evidence for this organization and what credible external/SEO ecosystem evidence materially changes prior assumptions.
5. [AI] Identify structural investments or removals worth considering, such as asset types, original research/data, architecture, localization, reputation work, or integrations; do not preserve a tactic merely because it exists in an older plan.
6. [AI] Recommend changes to strategic priorities/weights only with an interpretable business reason and evidence. Persist actual organizational decisions when they are made; do not deterministically rewrite strategy because a reporting period ended.
7. [DETERMINISTIC] Persist only new reusable MetricObservations that improve future measurement context.

## Verification
- Strategy recommendations trace to current business context and evidence.
- External tactic popularity does not substitute for local applicability/outcome evidence.
- The review does not automatically create Learning, Opportunities, or routed work.

## Completion Criteria
- The organization has a current evidence-backed view of where organic discovery should concentrate, stop, deepen, or change, with decisions left to the appropriate user/model.
