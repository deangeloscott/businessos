---
id: seo.monitoring.ecosystem-updates
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- MetricObservation
- Opportunity
- Incident
- SEOAssetState
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
  - local_profile.read
schedule:
  class: recurring
  default: daily
  configurable: true
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
updates:
  SEOAssetState:
  - organic_performance
---
# Search / Answer Ecosystem Update Monitoring

## Purpose
Detect official platform changes and credible industry developments that may require strategy review.

## Business Outcome
Improve valuable organic discovery through search / answer ecosystem update monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **search/answer ecosystem update monitoring**.

## Process
1. [HUMAN] Monitor approved official documentation, changelogs, webmaster announcements, policies, structured-data features, major search updates, and answer-surface measurement capabilities.
2. [AI] Monitor configured research/industry sources as lower evidence tiers.
3. [HYBRID] Extract distinct claims/changes with publication date, affected surface, source, and applicability.
4. [HYBRID] Check whether the development changes current system assumptions, policy, measurement, or active experiments.
5. [HYBRID] Route material items to SEO ecosystem evidence grading and urgent policy changes to Incident/policy review.
6. [HYBRID] Do not modify standard playbooks solely because a tip is popular.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


