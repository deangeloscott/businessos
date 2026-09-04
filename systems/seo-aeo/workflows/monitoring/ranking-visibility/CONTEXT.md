---
id: seo.monitoring.ranking-visibility
type: workflow
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
evidence_inputs:
- rank/visibility time series query-page mappings
updates:
  SEOAssetState:
  - organic_performance
---
# Ranking and Search Visibility Monitoring

## Purpose
Review material query/page/cluster visibility changes across relevant search surfaces without making AURA the rank-tracking runtime.

## Business Outcome
Keep search-visibility evidence current enough to recognize meaningful gains and losses in exposure for valuable demand and the resulting opportunity for qualified clicks, traffic, leads, and other business outcomes.

## Run When
Use for a bounded ranking/visibility check when the user requests it, saved monitoring intent indicates another review would be useful, or a material search/site change warrants comparison. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve current first-party search and available rank/visibility observations for the decision-relevant query/asset/market scope.
2. [HYBRID] Aggregate where useful by value-weighted query cluster, Asset, topic, market, device, branded/nonbrand, and result type.
3. [HYBRID] Compare appropriate rolling/prior/YoY windows while accounting for seasonality, sample limitations, and observable search-surface changes.
4. [HYBRID] Add demand and SERP/result context so position/visibility shifts are not interpreted in isolation.
5. [AI] Treat sustained stronger visibility for valuable demand as a meaningful upstream gain because higher or more frequent presence can increase exposure and the opportunity for qualified clicks and downstream value. Keep that pathway distinct from observed clicks, conversions, leads, or revenue when those later stages have not been measured.
6. [AI] Decide whether a sustained change warrants deeper ranking-decay/upside/root-cause diagnosis, an Opportunity, or Learning review. Monitoring does not route those methods automatically.
7. [HYBRID] Preserve current and historical measurement/state needed for later comparison rather than overwriting prior evidence.

## Verification
- Separate demand, ranking, indexing, SERP-layout, seasonality, and tracking effects before assigning a cause.
- Visibility is neither dismissed as a vanity metric nor mislabeled as downstream business outcome; its value depends on the demand and business pathway.
- Semantic cause/materiality remains model judgment.
- AURA stores useful monitoring intent/evidence; the host owns any recurring rank collection.
