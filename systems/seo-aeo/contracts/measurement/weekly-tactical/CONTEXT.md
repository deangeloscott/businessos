---
id: seo.measurement.weekly-tactical
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
# Weekly Tactical Report

## Purpose
Produce an action-oriented weekly view of changes, risks, opportunities, and work performed.

## Business Outcome
Improve valuable organic discovery through weekly tactical report, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run when the configured measurement window closes, a report is due, or **weekly tactical report** evidence becomes decision-relevant.

## Process
1. [DETERMINISTIC] Validate data-source health and reporting period completeness.
2. [AI] Summarize material business/search/AI/local/authority/technical changes only; suppress routine noise.
3. [HYBRID] List Opportunities created, reprioritized, executed, blocked, awaiting approval, or closed with reasons.
4. [HYBRID] List Change Events and early/confirmed outcomes, Incidents, failed actions, and upcoming measurement checkpoints.
5. [AI] Explain why top next actions are prioritized in business terms and which executor/autonomy tier applies.
6. [AI] Produce concise executive summary plus drill-down tables/links to underlying objects and evidence.

## Decisions / Routing
- Route → SEO Domain Learning / Core Business Learning as justified by outcome evidence.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


