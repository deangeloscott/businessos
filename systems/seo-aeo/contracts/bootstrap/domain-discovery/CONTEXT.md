---
id: seo.bootstrap.domain-discovery
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- Asset
- CapabilityBinding
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
Initialize SEO-specific scope from minimal business information without recreating general Business Context.

## Business Outcome
Establish or execute the SEO/AEO capability needed to improve valuable organic discovery.

## Run When
Run when the scoped SEO/AEO job is required by bootstrap, diagnosis, Opportunity planning, or delegated execution.

## Do Not Run When
Do not use this contract to duplicate canonical customer, competitor, industry, content, marketing, or journey ownership.

## Process
1. [INTEGRATION] Fetch the owned website/domain and resolve canonical host/protocol, reachable subdomains, locale/location variants, and obvious public site boundaries.
2. [AI] Identify SEO-relevant products/services, markets, page types, discovery surfaces, and likely commercial/informational entry points while treating business facts not in Core as provisional.
3. [DETERMINISTIC] Inventory representative URLs/templates, robots/sitemaps, CMS/technology clues, redirects, and existing analytics/search identifiers when available.
4. [HYBRID] Identify search/AEO/local applicability, major technical constraints, known migrations, and properties requiring separate SEO state.
5. [AI] Propose missing Business Context updates only when material; do not create duplicate business context.
6. [DETERMINISTIC] Create SEO domain state roots and bootstrap work list.

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
