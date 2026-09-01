---
id: seo.monitoring.technical
type: playbook
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
  - crawler.run
  optional:
  - webpage.fetch
  - cms.page.read
  - cms.page.update
  - search.index.inspect
updates:
  SEOAssetState:
  - organic_performance
---
# Technical Health Monitoring

## Purpose
Continuously detect changes in technical conditions likely to affect discovery, user experience, or measurement.

## Business Outcome
Improve valuable organic discovery through technical health monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **technical health monitoring**.

## Process
1. [HYBRID] Run incremental/full crawls and direct checks according to site scale/risk.
2. [HYBRID] Monitor uptime/status, redirects, robots/noindex, canonicals, sitemaps, rendering, internal links, structured data, performance, security indicators, and template changes.
3. [HYBRID] Group recurring URL symptoms into shared root causes.
4. [INTEGRATION] Compare with Change Events/deployments to identify likely causal timing.
5. [HYBRID] Route normal issues to Technical detector and critical sitewide changes to Incidents.
6. [HYBRID] Suppress accepted/intentional states with expiry/review dates rather than permanently ignoring them.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.


