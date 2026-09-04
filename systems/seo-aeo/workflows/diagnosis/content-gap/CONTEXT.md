---
id: seo.diagnosis.content-gap
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
- records topic intent evidence
---
# Content & Information Gap

## Purpose
Identify valuable user needs, decision questions, or answer components that owned assets do not currently serve well enough.

## Business Outcome
Find information gaps with a credible audience and business pathway while avoiding keyword-volume-driven production, unnecessary asset fragmentation, and content created merely because competitors have it.

## Run When
Use when current demand, customer, competitor, answer-source, support/sales, or content-performance evidence can help determine whether an important information need is missing or inadequately served.

## Process
1. [HYBRID] Relate relevant demand clusters, journey/decision stages, customer questions, competitor/answer-source coverage, owned Asset inventory, support/sales evidence, and performance to the actual business question. Scope the investigation to needs whose resolution could materially help the audience or objective.
2. [AI] Identify the real gap: absent destination, incomplete explanation/evidence, obsolete information, missing comparison/decision support, unsuitable format, or another unmet user outcome. Do not define the gap as a target word count or keyword list.
3. [AI] Check what existing owned assets already cover and whether improving, consolidating, or repositioning one would serve the need better than creating a new asset. Account for fragmentation, maintenance burden, and cannibalization risk.
4. [AI] Judge audience value, business pathway, differentiation/evidence needs, and realistic usefulness. Competitor coverage and keyword volume are evidence inputs, not standalone reasons to publish.
5. [AI] Preserve a content/on-page Opportunity only when the gap is materially useful, evidence-backed, and plausibly addressable. The model/user chooses the eventual production or improvement method directly.
6. [HYBRID] When the gap is resolved, evaluate whether the resulting asset actually serves the intended need and relevant business/discovery outcome rather than measuring publication alone.

## Verification
- Demand evidence, user need, existing coverage, and business relevance remain distinguishable.
- A new Asset is not required merely because a gap exists.
- Content is not justified solely by keyword volume, competitor presence, or the ability to produce it.
