---
id: seo.execution.technical.status-codes
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
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Status Codes

## Purpose
Correct HTTP response behavior that interferes with users, discovery, or diagnosis.

## Business Outcome
Improve valuable organic discovery through status codes, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Status Codes**, or when an authorized incident response requires it.

## Process
1. [INTEGRATION] Crawl representative/full site and aggregate 2xx/3xx/4xx/5xx and soft-error patterns.
2. [HYBRID] Separate intentional from accidental responses by asset type.
3. [HYBRID] Trace internal links, search traffic, conversions, and backlinks pointing to failures.
4. [AI] Fix origin/server/template issue or map moved content appropriately.
5. [HYBRID] Ensure genuinely removed content returns appropriate terminal behavior rather than misleading success.
6. [INTEGRATION] Re-crawl affected templates and define SEO monitoring for recurrence.


