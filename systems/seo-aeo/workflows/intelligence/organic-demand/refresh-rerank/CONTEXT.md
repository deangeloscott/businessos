---
id: seo.intelligence.organic-demand.refresh-rerank
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- OrganicDemandUnit
writes:
- OrganicDemandUnit
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
evidence_inputs:
- Market search answer evidence
- records topic intent evidence
updates:
  OrganicDemandUnit:
  - business_value
  - demand_evidence
---
# Demand Refresh and Rerank

## Purpose
Continuously update demand observations and priorities as markets, search behavior, products, and outcomes change.

## Business Outcome
Improve valuable organic discovery through demand refresh and rerank, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring demand research when the system must discover, classify, or update **demand refresh and rerank** evidence.

## Process
1. [HYBRID] Ingest new first-party queries, search/AI observations, trend/volume estimates, competitor movements, offers, and conversion/value data.
2. [HYBRID] Update existing OrganicDemandUnits instead of creating duplicates and preserve historical snapshots.
3. [HYBRID] Detect new, rising, declining, seasonal, saturated, and obsolete demand.
4. [DETERMINISTIC] Recompute intent/value/confidence when evidence changes and flag material classification shifts.
5. [HYBRID] Trigger new/updated Opportunities while preventing churn from insignificant short-term noise.
6. [DETERMINISTIC] Record what changed and why the priority moved.

## Decisions / Routing
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


