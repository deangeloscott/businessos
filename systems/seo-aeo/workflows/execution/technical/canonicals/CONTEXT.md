---
id: seo.execution.technical.canonicals
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- OrganicDemandUnit
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
- records topic intent evidence
---
# Duplicate & Canonical Consolidation

## Purpose
Resolve duplicate and near-duplicate owned URLs/assets so search/discovery signals are coherent without suppressing legitimately distinct customer intents, markets, languages, or page purposes.

## Business Outcome
Reduce duplicate-content confusion and wasted signals while preserving useful variants and the business value attached to them.

## Run When
Use when duplicate/near-duplicate assets, conflicting canonical signals, URL variants, or overlapping index states may be diluting or misdirecting valuable organic discovery.

## Process
1. Identify likely duplicate/near-duplicate clusters using the evidence appropriate to the site: URL patterns/parameters, content similarity, titles, canonicals, hashes, search/index observations, or another reliable method.
2. Determine which members are genuinely interchangeable versus legitimately distinct by customer intent, audience, market/language, page type, Offer/conversion role, or other material purpose.
3. Compare the signals that affect consolidation and discovery—rel=canonical, redirects, internal links, sitemap URLs, hreflang, host/protocol, index directives, backlinks, traffic, conversions, and content differences—only where relevant to the cluster.
4. Identify contradictions such as canonical loops/chains, cross-market/page-type canonicals, redirects and canonicals pointing differently, or internal/sitemap links continuing to promote non-primary variants.
5. Choose the smallest appropriate treatment per cluster: keep distinct, improve/differentiate, consolidate/redirect, canonicalize, noindex/remove, control parameters/URL generation, or another technically sound method. Do not canonicalize genuinely different useful pages merely because they look similar.
6. Align material internal links, sitemaps, alternate-language relationships, and other discovery signals with the intended state when necessary.
7. Verify representative and high-value affected URLs after changes and evaluate combined cluster/topic performance where consolidation occurred rather than judging only the surviving URL.

## Proportionate Scope
Analyze enough of each pattern/cluster to establish whether the issue is systemic and what useful variants exist. Expand toward broader crawling or full-cluster review when template behavior, scale, market/language complexity, or business risk makes sampling insufficient.

## Verification
- Similarity alone does not establish that one page should disappear.
- Customer intent, market/language, conversion role, and existing value are preserved where legitimately distinct.
- Redirect, canonical, index, internal-link, sitemap, and hreflang signals do not materially contradict the intended state.
- Broad changes are tested on representative/high-value cases and have a realistic rollback or recovery path when stakes justify it.
