---
id: seo.execution.indexing.indexnow
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
  - search.index.inspect
  optional:
  - search.index.request
  - cms.page.read
  - crawler.run
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# IndexNow Notification

## Purpose
Notify participating search engines of eligible URL additions, updates, or deletions when an IndexNow-capable adapter is configured.

## Business Outcome
Improve valuable organic discovery through indexnow notification, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **IndexNow Notification**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Confirm the URL change is real, public, canonical/intended, and appropriate for notification.
2. [HYBRID] Verify IndexNow key/configuration through the adapter without exposing secrets in workspace artifacts.
3. [INTEGRATION] Batch eligible changed URLs according to provider limits and submit addition/update/deletion notifications.
4. [DETERMINISTIC] Record request result, timestamp, URLs, and provider response; retry only transient failures safely.
5. [INTEGRATION] Do not treat successful notification as proof of crawl or indexing.
6. [INTEGRATION] Hand URLs to normal index/crawl monitoring.


