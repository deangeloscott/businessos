---
id: seo.measurement.monthly-business
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
- review mention reputation response history
---
# Monthly Organic Discovery Business Review

## Purpose
Connect SEO/AEO operations to business outcomes and strategic decisions.

## Business Outcome
Improve valuable organic discovery through monthly organic discovery business review, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run when the configured measurement window closes, a report is due, or **monthly organic discovery business review** evidence becomes decision-relevant.

## Process
1. [DETERMINISTIC] Validate full month data and document material attribution/data limitations.
2. [HYBRID] Report profit/revenue/qualified leads/conversions or strongest available proxies first, then qualified traffic and supporting visibility metrics.
3. [HYBRID] Break down contribution by market, offer, audience, topic/cluster, asset type, discovery surface, and major intervention where defensible.
4. [AI] Explain gains/losses through demand, visibility, CTR, conversion, technical, authority, local, AEO, and major ecosystem/competitor changes.
5. [HYBRID] Review Opportunity portfolio: value captured, pipeline, blockers, experiments, autonomy performance, and material costs.
6. [DETERMINISTIC] Set/adjust next-month priorities and record explicit strategic decisions rather than only presenting charts.

## Decisions / Routing
- Route → SEO Domain Learning / Core Business Learning as justified by outcome evidence.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


