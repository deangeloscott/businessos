---
id: seo.incidents.ranking-collapse
type: incident
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- Incident
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.index.inspect
  - crawler.run
  - cms.page.read
evidence_inputs:
- rank/visibility time series query-page mappings
---
# Ranking Collapse Incident

## Purpose
Rapidly stabilize and diagnose a broad or high-value ranking/visibility collapse.

## Business Outcome
Improve valuable organic discovery through ranking collapse incident, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run immediately when monitoring or an operator identifies a plausible **ranking collapse incident**. Incident routing overrides normal optimization until containment is complete.

## Process
1. [HYBRID] Confirm data/provider health and quantify affected pages/topics/markets/devices and first observed time.
2. [INTEGRATION] Correlate with deployments/Change Events, index/technical state, migrations, manual actions/policy notices, security, competitors, SERP demand shifts, and known ecosystem updates.
3. [HYBRID] Freeze risky autonomous changes affecting the impacted scope until diagnosis stabilizes.
4. [AI] Identify reversible likely causes and prioritize restoring known-good access/index/canonical/tracking state before speculative content rewrites.
5. [HUMAN] Execute/approve recovery actions with frequent verification and preserve incident timeline/evidence.
6. [HYBRID] Monitor recovery and conduct postmortem/root-cause learning before re-enabling normal autonomy.

## Verification
- Separate demand, ranking, indexing, SERP-layout, seasonality and tracking effects before assigning a cause.


