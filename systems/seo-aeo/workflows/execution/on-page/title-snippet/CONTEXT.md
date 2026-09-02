---
id: seo.execution.on-page.title-snippet
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- query-page impressions clicks CTR position SERP
---
# Search Presentation & CTR

## Purpose
Determine whether a material click-through gap is actually caused by controllable search-result presentation and improve titles/snippet-supporting content when the evidence supports that mechanism.

## Business Outcome
Increase qualified organic clicks without mistaking ranking, SERP layout, zero-click behavior, reputation, intent mismatch, or measurement noise for a copy problem—and without using clickbait or misleading presentation.

## Run When
Use when important query/page combinations have enough comparable search-result evidence to suggest materially weak CTR or when the user wants to improve how an owned result is presented.

## Process
1. [HYBRID] Gather the relevant query-page evidence: impressions, clicks, CTR, position/visibility, device, market, branded/nonbranded context, intent, result features, current title/meta description, observed snippets, page content, ratings/reputation signals where relevant, and competitor/result presentation.
2. [AI] Decide what comparison is actually meaningful. Compare CTR against similar position, query/intent, device, market, and result-layout conditions where possible; do not treat every below-average row or arbitrary benchmark as underperformance.
3. [HYBRID] Judge whether the gap is materially important relative to business value and evidence quality. If there is enough comparable first-party history, use it to improve expectations; otherwise keep uncertainty visible rather than fabricating a precise expected CTR.
4. [AI] Diagnose the most plausible contributors: title/snippet relevance, query-page mismatch, intent mismatch, position movement, SERP features/zero-click behavior, brand familiarity, reputation/ratings, structured result appearance, dynamic snippet selection, or stronger competitor presentation.
5. [AI] Only when presentation is a plausible controllable contributor, draft title and supporting snippet-content options that make the page's real relevance, differentiator, and user value easier to understand. Search engines may generate snippets dynamically, so optimize the underlying truthful presentation rather than assuming the meta description will be displayed verbatim.
6. [AI] Check options for accuracy, readability, likely truncation/context, audience fit, and consistency with the actual page. Avoid unsupported superlatives, false urgency, clickbait, or promises the destination cannot substantiate.
7. [HYBRID] Apply the selected change through the available site controls under the user's request, preserving a material ChangeEvent when later evaluation benefits from knowing what changed.
8. [HYBRID] Evaluate subsequent CTR under reasonably comparable query/position/device/market/result conditions so ranking or SERP movement is not credited to copy. Also check click quality or downstream business value when a higher CTR could attract less-qualified traffic.
9. [AI] Preserve an Opportunity only when a valuable presentation problem remains unresolved; do not create one merely because a row falls below a generic CTR benchmark.

## Verification
- CTR comparisons use sufficiently relevant conditions and acknowledge material data limitations.
- A presentation change is not prescribed when the supported cause lies primarily in ranking, intent, SERP layout, reputation, or another mechanism.
- Proposed result presentation accurately matches page content and business truth.
- Improvement claims distinguish CTR movement from rank/SERP changes and, where relevant, from downstream traffic quality.
