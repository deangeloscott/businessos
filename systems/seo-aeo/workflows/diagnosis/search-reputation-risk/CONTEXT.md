---
id: seo.diagnosis.search-reputation-risk
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
- Observation
writes:
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- review mention reputation response history
---
# Search Reputation Risk

## Purpose
Diagnose reputation or review conditions that materially affect organic, local, or answer-surface discovery without treating broad reputation management as an SEO responsibility.

## Business Outcome
Identify the search-relevant reputation mechanism, its actual business importance, and the smallest useful response without turning operational complaints into SEO problems.

## Run When
Use when reputation evidence appears relevant to a search, local, or AI-discovery decision and current evidence is sufficient to distinguish the visible reputation signal from its underlying cause.

## Process
1. Compare rating, review volume/recency/themes, response coverage, profile accuracy, and other reputation evidence only across the locations, products, sources, and decision paths that materially matter.
2. Relate that evidence to where it is actually visible in search, local, AI-answer, or customer decision surfaces rather than assuming all reputation data affects discovery equally.
3. Determine whether the likely mechanism is insufficient authentic review coverage, an unanswered-review backlog, inaccurate profile information, misinformation, a recurring operational complaint, or another cause.
4. Separate SEO-visible symptoms from operational, product, service, customer-experience, or other root causes. Use the relevant operating knowledge directly when SEO is not the real owner.
5. When a legitimate search/discovery intervention exists, define the smallest useful response and preserve an Opportunity only when the durable coordination value justifies it.
6. Evaluate later change using relevant trust, choice, discovery, and business evidence rather than review count alone.

## Proportionate Scope
Prioritize reputation evidence that meaningfully appears in the actual customer/search decision. Broaden the review when stakes, uncertainty, contradictory evidence, or multiple locations/surfaces make additional investigation likely to change the conclusion.

## Verification
- Search visibility, reputation evidence, operational root cause, and business impact remain distinct.
- Never recommend synthetic reviews, review gating, manipulation, or unsupported reputation claims merely to improve a metric.
- Do not manufacture cross-domain routing objects when the active model/user can simply continue with the appropriate method.
