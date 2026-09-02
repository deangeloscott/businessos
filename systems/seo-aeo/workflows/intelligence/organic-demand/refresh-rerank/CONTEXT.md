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
# Demand Refresh and Reprioritization

## Purpose
Update organic-demand understanding and priorities as customer behavior, markets, search/answer surfaces, Offers, and observed outcomes change.

## Business Outcome
Keep effort focused on the demand that matters now without allowing stale assumptions or short-term noise to drive work.

## Run When
Use when material new evidence could change demand relevance, intent, value, confidence, seasonality, or priority, or when the user/runtime invokes a periodic demand review. AURA may remember refresh intent; the harness/runtime owns recurrence.

## Process
1. [HYBRID] Gather only the fresh evidence likely to change the decision: first-party queries, search/AI observations, trend/volume estimates, competitor movement, Offer changes, customer evidence, and conversion/value outcomes.
2. [AI] Compare new evidence with existing OrganicDemandUnits and prior context; update existing meaning rather than creating duplicates for routine wording or measurement variation.
3. [AI] Identify genuinely new, rising, declining, seasonal, saturated, obsolete, or newly valuable demand and distinguish durable change from short-term volatility.
4. [AI] Reconsider intent, value, confidence, market/audience relevance, and business pathway when the evidence warrants it. Do not mechanically recompute labels merely because a refresh occurred.
5. [AI] Reprioritize at the resolution useful for current planning. Preserve the reasoning for material changes when future work would otherwise rediscover why the priority moved.
6. [HYBRID] Create or update an Opportunity only when an unresolved possibility is itself useful durable organizational memory; do not generate task churn for every priority change.

## Verification
- Priority changes trace to material evidence or changed business context.
- Short-term search/answer volatility is not automatically treated as changed demand.
- Visibility and traffic signals may legitimately change priority because they affect exposure opportunity, while downstream business outcomes remain separately evidenced.
- The model/user remains free to override or reinterpret stale classifications when better evidence or judgment supports it.
