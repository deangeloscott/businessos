---
id: seo.measurement.quarterly-strategy
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
- review mention reputation response history
---
# Quarterly Organic Discovery Strategy Review

## Purpose
Reassess markets, demand, competitors, asset portfolio, strategy evidence, and resource direction.

## Business Outcome
Improve valuable organic discovery through quarterly organic discovery strategy review, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run when the configured measurement window closes, a report is due, or **quarterly organic discovery strategy review** evidence becomes decision-relevant.

## Process
1. [HYBRID] Refresh Brand Context for product/offer/audience/market/positioning changes.
2. [HYBRID] Review quarter business value and longer-term organic contribution against objectives and proxy dependence.
3. [AI] Reassess Demand Universe, competitor types, answer/search/local surfaces, topic coverage, authority/reputation, and technical architecture.
4. [HYBRID] Review what intervention classes worked for this brand and what SEO ecosystem evidence or eligible System Learning changed.
5. [AI] Identify structural investments such as new asset types, original research/data, architecture, localization, reputation programs, or integrations.
6. [AI] Reprioritize objectives/opportunity scoring weights only with an interpretable business reason and preserve version history.

## Decisions / Routing
- Route → SEO Domain Learning / Core Business Learning as justified by outcome evidence.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


