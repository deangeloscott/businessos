---
id: seo.execution.internal-linking.broken-internal-links
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
  - cms.page.read
  - cms.page.update
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Broken Internal Links

## Purpose
Detect and resolve internal links that lead to errors, redirects, wrong canonicals, or retired assets.

## Business Outcome
Improve valuable organic discovery through broken internal links, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Broken Internal Links**, or when an authorized incident response requires it.

## Process
1. [INTEGRATION] Crawl internal links and classify direct errors, redirect chains, redirected-to-irrelevant pages, soft errors, and links to noncanonical variants.
2. [HYBRID] Recover historical destination purpose using page history, anchor/context, redirects, sitemap, and asset records.
3. [HYBRID] Choose the best live destination, content restoration, link removal, or redirect fix.
4. [HYBRID] Update links at source where practical rather than relying indefinitely on redirect chains.
5. [HYBRID] Verify every changed source-target relationship and update state.
6. [AI] Define SEO monitoring for recurrence patterns to identify template/CMS causes.


