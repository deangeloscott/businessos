---
id: seo.bootstrap.asset-state-inventory
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- Asset
writes:
- SEOAssetState
- Observation
- Asset
capabilities:
  required:
  - crawler.run
  optional:
  - cms.page.read
  - search.performance.read
  - search.index.inspect
  - analytics.read
context:
- Brand
- Business
- Market
- Offer
- ProductService
---
# SEO Asset State Inventory

## Purpose
Attach SEO-specific state to canonical Assets without creating duplicate asset identities.

## Business Outcome
Establish or execute the SEO/AEO capability needed to improve valuable organic discovery.

## Run When
Run when the scoped SEO/AEO job is required by bootstrap, diagnosis, Opportunity planning, or delegated execution.

## Do Not Run When
Do not use this contract to duplicate canonical customer, competitor, industry, content, marketing, or journey ownership.

## Process
1. [DETERMINISTIC] Discover owned URLs/assets through sitemaps, crawl, CMS, analytics/search data, and known canonical Asset registry.
2. [DETERMINISTIC] Resolve each discoverable item to one Core Asset ID or submit a new Asset registration when truly missing.
3. [INTEGRATION] Collect URL/status/indexability/canonical/render/search-performance/structured-data/internal-link data for SEO-relevant Assets.
4. [AI] Classify page type, probable search intent role, market/language, template, and organic relevance.
5. [DETERMINISTIC] Create/update SEOAssetState keyed to Asset ID; do not copy generic asset metadata.
6. [HYBRID] Identify material coverage/data gaps and route baseline contracts.

## Verification
- Validate all written objects and independently verify external state changes.

## Measurement
- Define the SEO mechanism metric and relevant business outcome before execution when this contract changes external state.

## Learning
- Return OutcomeEvaluation evidence to SEO Domain Learning and relevant upstream/downstream systems.

## Failure / Fallback
- Missing tools create manual work; missing upstream intelligence permits bounded provisional SEO research with source provenance.

## Completion Criteria
- The required SEO output exists, validates, and has explicit lineage/next route.
## Deterministic local-site evidence
When the scoped evidence is a local/first-party website export, do not hand-author material direct site facts from model memory or prose inspection. Run `scripts/inspect_site_evidence.py`, then persist material direct Observations through `scripts/persist_site_observation.py` using the captured fact IDs. Keep consequences, severity, and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.

