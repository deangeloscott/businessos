---
id: seo.execution.technical.crawl-access
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Crawl Access

## Purpose
Ensure valuable assets can be discovered and fetched by intended crawlers without exposing unwanted/private areas.

## Business Outcome
Improve valuable organic discovery through crawl access, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Crawl Access**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Enumerate target URLs/sections and intended crawler eligibility.
2. [INTEGRATION] Fetch robots.txt and relevant HTTP/meta directives; inspect status, authentication, CDN/WAF barriers, and resource blocking.
3. [INTEGRATION] Compare crawl rules against sitemap and internal-link discovery paths.
4. [INTEGRATION] Test representative URLs with raw and rendered fetch where JavaScript or edge controls matter.
5. [AI] Identify blocked valuable resources versus intentionally blocked low-value/private areas.
6. [HYBRID] Model blast radius before changing wildcard/path rules.
7. [HYBRID] Prepare the smallest rule change; preserve security/privacy boundaries.
8. [HYBRID] Execute within autonomy tier and verify representative plus boundary URLs.


