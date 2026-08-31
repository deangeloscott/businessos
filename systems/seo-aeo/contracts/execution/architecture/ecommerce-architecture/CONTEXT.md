---
id: seo.execution.architecture.ecommerce-architecture
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
  - cms.page.read
  - cms.page.update
---
# Ecommerce Architecture

## Purpose
Organize categories, subcategories, products, filters, and merchandising paths for users and organic discovery.

## Business Outcome
Improve valuable organic discovery through ecommerce architecture, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Ecommerce Architecture**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory category tree, product relationships, variants, facets, internal search, and discontinued inventory behavior.
2. [AI] Map commercial demand and user shopping tasks to category/collection destinations.
3. [INTEGRATION] Separate index-worthy landing facets from crawl traps or near-duplicate parameter combinations.
4. [HYBRID] Define canonical, linking, sitemap, out-of-stock, discontinued, variant, and pagination behavior.
5. [AI] Identify missing commercial category/collection opportunities and cannibalization between categories/products.
6. [HYBRID] Stage architecture changes with redirect/canonical/link migration maps and verify revenue/analytics guardrails.


