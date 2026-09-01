---
id: seo.diagnosis.detectors.ranking-upside
type: detector
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
writes:
- Opportunity
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.serp.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- rank/visibility time series query-page mappings
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Ranking Upside Detector

## Purpose
Find Assets already visible for valuable demand where a realistic relevance/quality/authority improvement could materially increase business value.

## Business Outcome
Identify plausible ranking upside with a real business pathway while avoiding raw-volume prioritization and false precision about potential lift.

## Run When
Use when fresh relevant visibility/demand observations exist and the user/model needs to diagnose **ranking upside**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Select business-relevant query/page clusters with meaningful visibility and room for improvement, using thresholds appropriate to the evidence rather than one universal position band.
2. [AI] Prioritize by value-weighted demand and current conversion/Offer fit, not raw volume.
3. [HYBRID] Inspect trend, result composition, intent match, competitors, page quality, internal links, authority, technical state, and possible cannibalization.
4. [AI] Judge whether the current Asset is plausibly capable of improving or whether a different Asset/intent strategy is needed.
5. [AI] Create/update an Opportunity with evidence-backed root-cause hypotheses and only the range/confidence that current evidence can support; do not fabricate incremental value.
6. [HYBRID] Exclude misleading visibility caused by location/personalization or demand where improved rank would not materially help the business.

## Verification
- Demand, visibility, business value, intervention feasibility, and expected effect remain separately calibrated.
