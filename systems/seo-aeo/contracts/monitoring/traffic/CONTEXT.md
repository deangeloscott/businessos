---
id: seo.monitoring.traffic
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
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
  - local_profile.read
evidence_inputs:
- traffic time series landing page dimensions conversion
updates:
  SEOAssetState:
  - organic_performance
---
# Organic Traffic Monitoring

## Purpose
Detect material changes in qualified organic site/app traffic and landing behavior.

## Business Outcome
Improve valuable organic discovery through organic traffic monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **organic traffic monitoring**.

## Process
1. [HYBRID] Refresh organic sessions/users/landing pages and quality/business-action metrics.
2. [HYBRID] Segment by asset, topic, market, device, new/returning, brand/nonbrand, and source surface where observable.
3. [HYBRID] Compare rolling/prior/YoY baselines with seasonality and known campaign/site changes.
4. [DETERMINISTIC] Validate analytics health before alerting on decline.
5. [AI] Route material unexplained losses to traffic-decay diagnosis and gains to Change Event attribution/learning.
6. [HYBRID] Track quality and conversion so raw visitor growth cannot hide worse business outcomes.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.

## Verification
- Reconcile search visibility, analytics and conversion evidence before concluding the site lost demand or rank.


