---
id: seo.execution.technical.international-hreflang
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
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
---
# International Hreflang

## Purpose
Represent market/language variants correctly and avoid cross-market canonical conflicts.

## Business Outcome
Improve valuable organic discovery through international hreflang, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **International Hreflang**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory locale variants and intended audiences.
2. [DETERMINISTIC] Validate language/region codes and reciprocal alternate relationships where hreflang is used.
3. [HYBRID] Check self/cluster canonical behavior and locale URLs.
4. [HYBRID] Ensure localized content, offers, currency, legal text, contact details, and terminology fit target market.
5. [HYBRID] Detect missing/incorrect alternates and fallback behavior.
6. [INTEGRATION] Deploy and validate representative clusters at scale.


