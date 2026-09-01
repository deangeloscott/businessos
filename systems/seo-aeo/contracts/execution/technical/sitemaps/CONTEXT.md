---
id: seo.execution.technical.sitemaps
type: playbook
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - crawler.run
  optional:
  - webpage.fetch
  - cms.page.read
  - cms.page.update
  - search.index.inspect
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
- location/profile data, local-result observations, and local competitors
---
# Sitemaps

## Purpose
Maintain accurate discovery sitemaps for canonical, index-worthy URLs.

## Business Outcome
Improve valuable organic discovery through sitemaps, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Sitemaps**, or when an authorized incident response requires it.

## Process
1. [AI] Inventory sitemap indexes/files and generation logic.
2. [DETERMINISTIC] Validate XML/syntax, response status, canonical host/protocol, URL count/size, and meaningful `lastmod` behavior if used.
3. [HYBRID] Exclude redirects, errors, noncanonical, blocked, or intentionally non-indexable URLs.
4. [AI] Ensure important canonical URLs are represented without treating sitemap presence as an indexing guarantee.
5. [AI] Segment large or diagnostically useful site sections where helpful.
6. [INTEGRATION] Publish and notify supported search systems through configured mechanisms.
7. [INTEGRATION] Define SEO monitoring for submitted-versus-indexed diagnostics and investigate material gaps.

## Verification
- Verify location eligibility and business facts before changing public profile/location data.


