---
id: seo.bootstrap.baseline.search-baseline
type: workflow
owner_system: seo-aeo
reads:
- Asset
- Observation
writes:
- SEOAssetState
- Asset
- MetricObservation
context:
- Brand
- Business
- Market
- Offer
- ProductService
evidence_inputs:
- Available search and first-party performance evidence
updates:
  SEOAssetState:
  - organic_performance
---
# Search Performance Baseline

## Purpose
Establish a trustworthy starting view of organic search visibility and performance for the queries, pages, markets, and surfaces that materially matter.

## Business Outcome
Give later SEO decisions a useful comparison point and connect search visibility to the organization’s business-value pathways without requiring a full-site measurement ritual.

## Run When
Use when current search-performance state is missing, materially stale, or needed to evaluate a concrete opportunity, change, diagnosis, or trend. A user/runtime may invoke re-baselining; AURA does not own the schedule.

## Process
1. [HYBRID] Gather the longest reliable history and comparison context that is useful for the decision from available search-performance, analytics, ranking, or other valid evidence sources.
2. [HYBRID] Normalize query/page/date/market/device/search-appearance or surface dimensions only where those dimensions materially affect interpretation.
3. [HYBRID] Describe impressions, clicks, CTR, position/visibility, coverage, trends, and uncertainty without over-interpreting averages or provider-specific metrics.
4. [HYBRID] Connect search signals to first-party engagement, conversion, lead quality, revenue, or other outcomes where evidence exists. Keep visibility, traffic, and business outcomes distinct while preserving the credible pathway among them.
5. [AI] Segment branded/nonbranded, intent, topic, audience, market, stage, or asset type only when the segmentation changes a useful conclusion.
6. [AI] Preserve the baseline distributions, important context, and material unknowns that future comparison will benefit from. Do not create Opportunities or downstream work merely because the baseline exists.

## Verification
- Baseline evidence is timestamped and scoped enough to make later comparisons meaningful.
- Ranking/visibility and traffic are treated as meaningful upstream signals where appropriate, not as automatic proof of leads or revenue.
- Missing integrations remain missing evidence rather than an AURA capability/setup state.
- Further demand, competitor, diagnosis, or execution methods are optional and chosen directly by the capable model/user.
