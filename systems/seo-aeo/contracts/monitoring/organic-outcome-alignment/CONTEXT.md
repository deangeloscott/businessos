---
id: seo.monitoring.organic-outcome-alignment
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
- conversion CRM revenue best available proxy
updates:
  SEOAssetState:
  - organic_performance
---
# Organic Conversion and Value Monitoring

## Purpose
Track downstream business outcomes from organic discovery and detect quality/value changes.

## Business Outcome
Improve valuable organic discovery through organic conversion and value monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **organic conversion and value monitoring**.

## Process
1. [HYBRID] Refresh conversions/leads/opportunities/orders/revenue/profit or best available proxies.
2. [DETERMINISTIC] Join to organic landing/query/content/market paths using documented attribution limitations.
3. [HYBRID] Compare conversion rate, qualified rate, value per visit/lead, and total value over appropriate windows.
4. [HYBRID] Detect traffic growth with value decline, lead-quality deterioration, offer/market capacity issues, and tracking changes.
5. [HYBRID] Route actionable landing/acquisition mismatches to conversion-gap detector; route sales/product/operations causes externally.
6. [HYBRID] Update value model confidence and opportunity prioritization from observed outcomes.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.


