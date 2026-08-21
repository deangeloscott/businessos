---
id: seo.execution.architecture.multilingual-architecture
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 3
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
  - cms.page.read
  - cms.page.update
---
# Multilingual / Multiregional Architecture

## Purpose
Represent languages and markets so each audience reaches the intended localized experience.

## Business Outcome
Improve valuable organic discovery through multilingual / multiregional architecture, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Multilingual / Multiregional Architecture**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory languages, countries/regions, currencies, legal requirements, offers, and existing localized URLs.
2. [HYBRID] Choose a durable URL/location strategy and define locale ownership; avoid automatic locale assumptions that block crawlers/users.
3. [AI] Map equivalent and non-equivalent localized assets; identify missing localized content rather than blindly translating.
4. [HYBRID] Define hreflang/alternate relationships, canonicals, language selectors, sitemaps, and internal links.
5. [DETERMINISTIC] Validate localized intent, terminology, offers, metadata, and conversion paths with market-specific evidence.
6. [HYBRID] Test reciprocal annotations, rendering, index eligibility, and market-specific performance after changes.


