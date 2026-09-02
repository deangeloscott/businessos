---
id: seo.monitoring.ctr
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
- query-page impressions clicks CTR position SERP
updates:
  SEOAssetState:
  - organic_performance
---
# CTR Monitoring

## Purpose
Review click-through behavior relative to query/page position and result context without treating CTR movement as a self-explanatory optimization signal.

## Business Outcome
Keep search-result presentation evidence current enough to identify meaningful under/overperformance while protecting qualified traffic and downstream business value.

## Run When
Use for a bounded CTR review when the user requests it, saved monitoring intent indicates another check would be useful, or material search/result changes warrant comparison. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve impressions, clicks, CTR, position, query/page, market/device, and relevant result-context evidence from the strongest available first-party/search sources.
2. [HYBRID] Build or refresh relevant CTR expectations from sufficient business evidence while keeping cold-start assumptions visibly provisional.
3. [HYBRID] Assess material under/overperformance in the context of brand/nonbrand, intent, position, device, market, and observable result features.
4. [AI] Interpret sudden CTR changes without position movement as hypotheses about snippet/SERP/brand/reputation change until evidence distinguishes them.
5. [AI] Decide whether a material gap warrants deeper low-CTR diagnosis, an Opportunity, or a Learning review. Useful gains can inform Learning only when evidence supports a reusable mechanism; monitoring does not route those outcomes automatically.
6. [HYBRID] Preserve the useful MetricObservation/SEOAssetState evidence and keep downstream quality/conversion visible so raw CTR optimization cannot override business outcomes.

## Verification
- Compare CTR only against a relevant position/query/device/market expectation.
- Rank/demand/SERP movement and presentation effect remain distinct.
- A durable Opportunity is created only when a material plausibly controllable gap is actually supported, not because the monitor ran.
