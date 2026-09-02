---
id: seo.diagnosis.ranking-upside
type: workflow
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
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- rank/visibility time series query-page mappings
---
# Ranking Upside

## Purpose
Identify owned assets already visible for valuable demand where a realistic relevance, quality, architecture, technical, or authority improvement could materially increase business value.

## Business Outcome
Find plausible ranking upside with a real business pathway while avoiding raw-volume prioritization, universal position bands, and false precision about incremental lift.

## Run When
Use when current demand and visibility evidence can help determine whether an already-visible asset has a worthwhile, realistically addressable organic-growth opportunity.

## Process
1. [HYBRID] Select business-relevant query/page/topic clusters with meaningful visibility and room for improvement using thresholds appropriate to the actual evidence, result environment, and objective rather than one universal ranking band.
2. [AI] Prioritize by value-weighted demand, audience/Offer fit, current downstream quality/value, and expected decision usefulness—not raw query volume or theoretical traffic alone.
3. [HYBRID] Inspect trend, intent/result composition, competitor/source quality, page usefulness, internal links/architecture, authority, technical/index state, SERP features, and possible cannibalization only to the depth that could change the opportunity judgment.
4. [AI] Determine whether the current Asset can plausibly improve for the intended demand or whether a different Asset/intent strategy—or no action—is more appropriate.
5. [AI] Identify evidence-backed root-cause hypotheses and the smallest plausible intervention class. Do not fabricate ranking probability, incremental traffic, revenue, or a precise effect range that the evidence cannot support.
6. [HYBRID] Exclude misleading visibility caused by personalization/location or demand where improved rank would not materially help the business.
7. [AI] Preserve an Opportunity only when demand, business value, intervention feasibility, and evidence are jointly strong enough to justify attention.

## Verification
- Demand, current visibility, business value, intervention feasibility, and expected effect remain separately calibrated.
- Opportunity priority reflects business value and realistic mechanism rather than raw search volume.
- No ranking or revenue lift is presented with more precision than the evidence supports.
