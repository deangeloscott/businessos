---
id: seo.execution.technical.structured-data
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
  - webpage.fetch
  - cms.page.read
  - cms.page.update
  - search.index.inspect
---
# Structured Data

## Purpose
Implement accurate supported structured data that matches visible content and real business facts.

## Business Outcome
Improve valuable organic discovery through structured data, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Structured Data**, or when an authorized incident response requires it.

## Process
1. [AI] Identify page/entity type and currently supported structured-data opportunities.
2. [AI] Map required/recommended properties to verified visible facts.
3. [HYBRID] Do not mark up entities/claims/reviews/offers that are not actually represented accurately on the page/business.
4. [AI] Generate or modify markup using the site’s preferred maintainable format.
5. [DETERMINISTIC] Validate syntax plus applicable rich-result requirements.
6. [INTEGRATION] Deploy and inspect rendered output.
7. [HYBRID] Monitor enhancement/errors and update markup when visible facts change.


