---
id: seo.execution.technical.redirects
type: playbook
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
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Redirects

## Purpose
Design and validate redirects that preserve user journeys, discovery, and historical value.

## Business Outcome
Improve valuable organic discovery through redirects, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Redirects**, or when an authorized incident response requires it.

## Process
1. [AI] Identify source URLs, reason, destination, permanence, traffic/backlinks, and conversion role.
2. [HYBRID] Avoid irrelevant mass redirects to home/category where no equivalent exists.
3. [HYBRID] Detect chains, loops, protocol/host hops, regex overreach, and destination errors.
4. [HYBRID] Create one-hop mapping to the closest equivalent canonical destination.
5. [HYBRID] Backup routing configuration and test mapping before production.
6. [INTEGRATION] Deploy controlled batch; crawl source/destination set.
7. [HYBRID] Update internal links, sitemaps, canonicals, hreflang, and navigation to final URLs.
8. [HYBRID] Monitor errors, traffic, indexing, conversions, and important backlinks.

## Verification
- Test affected URL sets and rollback path before broad deployment; verify crawl/index behavior afterward.


