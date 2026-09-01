---
id: seo.bootstrap.domain-discovery
type: playbook
owner_system: seo-aeo
reads:
- Asset
writes:
- OrganicDemandUnit
- SEOAssetState
- OrganicCompetitorState
- Observation
- ContextUpdateProposal
capabilities:
  required:
  - webpage.fetch
  optional:
  - crawler.run
  - search.performance.read
  - analytics.read
context:
- Brand
- Business
- Market
- Offer
- ProductService
---
# SEO Domain Discovery

## Purpose
Initialize SEO-specific scope from minimal business information without recreating general Business Context or treating host capability state as AURA memory.

## Business Outcome
Establish the SEO/AEO domain, assets, discovery surfaces, and initial work needed to improve valuable organic discovery.

## Run When
Run when SEO/AEO bootstrap or later diagnosis needs a grounded view of the owned web presence and relevant discovery surfaces.

## Do Not Run When
Do not use this contract to duplicate canonical customer, competitor, industry, content, marketing, or journey ownership.

## Process
1. [INTEGRATION] Using the active harness's available web capabilities, fetch the owned website/domain and resolve canonical host/protocol, reachable subdomains, locale/location variants, and obvious public site boundaries.
2. [AI] Identify SEO-relevant products/services, markets, page types, discovery surfaces, and likely commercial/informational entry points while treating business facts not in Core as provisional.
3. [DETERMINISTIC] Inventory representative URLs/templates, robots/sitemaps, CMS/technology clues, redirects, and existing analytics/search identifiers when actually available.
4. [HYBRID] Identify search/AEO/local applicability, major technical constraints, known migrations, and properties requiring separate SEO state.
5. [AI] Propose missing Business Context updates only when material; do not create duplicate business context.
6. [DETERMINISTIC] Persist only the SEO-specific state and observations that future organizational work would materially benefit from.

## Verification
- Validate written AURA state, preserve evidence lineage, and keep unavailable host/tool data explicitly unknown rather than inventing a capability record.

## Measurement
- Establish relevant baseline measures when trustworthy first-party or observable evidence is available and the downstream work needs them.

## Learning
- Later OutcomeEvaluation evidence may inform SEO Domain Learning when it materially changes what the organization should remember about its organic-discovery work.

## Failure / Fallback
- If a preferred tool is unavailable, use another valid method available to the active harness when practical. Otherwise preserve the unresolved need honestly; do not create a fake CapabilityBinding or pretend the inspection occurred.

## Completion Criteria
- The required SEO bootstrap state exists, validates, and has explicit lineage/next route where useful.
