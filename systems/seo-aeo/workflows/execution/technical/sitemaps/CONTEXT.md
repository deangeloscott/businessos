---
id: seo.execution.technical.sitemaps
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Sitemaps

## Purpose
Maintain accurate discovery sitemaps that represent the canonical index-worthy URLs the business actually wants search systems to discover and refresh.

## Business Outcome
Improve discovery efficiency and diagnostic clarity without treating sitemap inclusion as an indexing guarantee.

## Run When
Use when sitemap generation, coverage, freshness, segmentation, or consistency may materially affect discovery or make crawl/index diagnosis harder.

## Process
1. Inspect sitemap indexes/files and the generation logic or source data that determines which URLs appear.
2. Validate syntax, response status, canonical host/protocol, size/count constraints, and `lastmod` behavior when used; timestamps should reflect meaningful change rather than automatic churn.
3. Exclude redirects, errors, noncanonical URLs, intentionally non-indexable URLs, blocked/private resources, and other states that contradict the intended sitemap role.
4. Ensure important canonical index-worthy URLs are represented while keeping sitemap presence distinct from crawl, canonical selection, indexing, or ranking.
5. Segment very large or diagnostically different URL groups when that improves discovery management or makes submitted-versus-observed problems easier to isolate.
6. Publish/update the sitemap through the actual site/platform and use supported submission/notification mechanisms when useful and available; successful submission is not proof of crawl or indexing.
7. Compare submitted URLs with relevant crawl/index evidence when material gaps exist and use the appropriate indexing/crawl/URL method to investigate the cause.

## Proportionate Scope
Validate representative sitemap generation rules and high-value URL classes first. Expand toward full-file/full-index checks when scale, multiple generators, migration risk, or observed coverage gaps make sampling insufficient.

## Verification
- Sitemap entries match the intended canonical/indexable state.
- Generation does not continually reintroduce redirects, errors, noncanonical URLs, or meaningless timestamp changes.
- Important omissions and submitted-versus-indexed gaps are diagnosed rather than assuming submission itself should fix them.
