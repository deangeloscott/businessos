---
id: seo.monitoring.data-health
type: playbook
version: 1.1.0
owner_system: seo-aeo
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
updates:
  SEOAssetState:
  - organic_performance
---
# Data Health Monitoring

## Purpose
Detect broken, stale, partial, duplicated, or materially changed inputs before the system makes decisions from them.

## Business Outcome
Improve valuable organic discovery through data health monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **data health monitoring**.

## Process
1. [HYBRID] Check each required provider/feed for last-success timestamp, expected row/event volume, schema, authorization, rate-limit, and error state.
2. [HYBRID] Compare key totals/distributions with recent baselines to detect silent truncation, duplication, timezone/property/scope changes, or tracking loss.
3. [DETERMINISTIC] Validate joins/identity coverage for assets, queries, locations, conversions, and competitors.
4. [AI] Classify degradation as warning, decision-blocking, or Incident based on which workflows depend on the data.
5. [HYBRID] Disable or downweight affected detectors/scores rather than treating missing values as zero.
6. [HYBRID] Alert/escalate and verify recovery before normal autonomous decisions resume.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.


