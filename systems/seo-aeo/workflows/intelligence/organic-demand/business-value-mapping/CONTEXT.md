---
id: seo.intelligence.organic-demand.business-value-mapping
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- Observation
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
# Demand Business-Value Mapping

## Purpose
Connect pursued organic/search/answer demand to a credible business-value pathway so attention is prioritized by usefulness and opportunity rather than volume alone.

## Business Outcome
Focus organic-discovery effort on demand where stronger visibility can plausibly create valuable exposure, traffic, consideration, leads, sales, retention, or another business outcome while keeping those stages and their evidence distinct.

## Run When
Use when deciding whether a demand unit is worth pursuing, comparing priorities, or revisiting value after Offers, markets, customer behavior, or outcome evidence change.

## Process
1. [AI] Map the demand unit to audience, problem/goal, awareness or buying stage, relevant Offer or organizational value, and the plausible next action or assisted role.
2. [HYBRID] Use observed first-party traffic, conversion, lead-quality, revenue, customer, or other outcome evidence when available. Preserve the difference between direct outcomes and upstream signals such as rankings, impressions, citations, mentions, clicks, or engagement.
3. [AI] Describe the credible value pathway. For example, stronger visibility for valuable demand may increase qualified exposure, which may increase visits or consideration, which may create more lead or revenue opportunities. Treat that pathway as plausible unless downstream steps are actually measured.
4. [AI] Estimate relative business relevance using customer fit, market priority, Offer economics where actually known, conversion proximity, strategic importance, assisted value, and evidence quality. Keep assumptions visible rather than fabricating precise economics.
5. [AI] Recognize supporting demand whose value is indirect but real: education, trust, comparison, objection resolution, brand discovery, or post-purchase help may contribute to later outcomes even when the asset is not expected to convert directly.
6. [AI] Downweight or reject high-volume demand when the audience fit or business pathway is weak, while preserving strategically important low-volume demand when its value is high.
7. [AI] Produce an interpretable value rationale at the resolution needed for the decision. A numeric score is optional and should never replace the reasoning.
8. [HYBRID] Update or persist OrganicDemandUnit value evidence only when doing so improves future prioritization or continuity; no Opportunity Engine or qualification lifecycle is required.

## Verification
- Rankings, visibility, citations, mentions, traffic, conversions, leads, and revenue remain distinct evidence stages.
- Strong upstream signals may be treated as meaningful business opportunity indicators when the pathway is credible, without being mislabeled as observed downstream outcomes.
- Unknown economics remain unknown rather than being filled with invented values.
- Demand prioritization stays tied to the actual organization, market, audience, and objectives rather than generic search volume.
