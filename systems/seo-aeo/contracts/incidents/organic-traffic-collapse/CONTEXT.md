---
id: seo.incidents.organic-traffic-collapse
type: incident
version: 1.1.0
owner_system: seo-aeo
risk: high
autonomy_ceiling: 2
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- ActionPacket
- Incident
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.index.inspect
  - crawler.run
  - cms.page.read
events:
  consumes:
  - none
  emits:
  - seo.incident.updated
evidence_inputs:
- traffic time series landing page dimensions conversion
---
# Organic Traffic Collapse Incident

## Purpose
Diagnose severe qualified organic traffic loss while protecting measurement and revenue pathways.

## Business Outcome
Improve valuable organic discovery through organic traffic collapse incident, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run immediately when monitoring or an operator identifies a plausible **organic traffic collapse incident**. Incident routing overrides normal optimization until containment is complete.

## Process
1. [DETERMINISTIC] Validate analytics/tagging/data source and compare with search-performance evidence.
2. [HYBRID] Quantify affected landing pages, topics, markets, devices, conversion actions, and time of onset.
3. [HYBRID] Decompose into demand, ranking/visibility, CTR/SERP, indexing/technical, site availability, migration, tracking, or conversion-path causes.
4. [HYBRID] Freeze/revert likely harmful recent changes where evidence and rollback safety support it.
5. [HYBRID] Route technical/index/ranking recovery work in priority order by business value.
6. [HYBRID] Maintain stakeholder updates and postmortem with preventive controls.

## Verification
- Reconcile search visibility, analytics and conversion evidence before concluding the site lost demand or rank.


