---
id: seo.execution.indexing.publish-discovery
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Publish and Discovery Signaling

## Purpose
Help newly published, materially changed, or intentionally removed URLs become correctly discoverable by the relevant search surfaces without treating submission as indexing.

## Business Outcome
Make intended organic assets easier for crawlers and discovery systems to find while keeping URL truth, canonicalization, and observed index state clear.

## Run When
Use when a URL is newly published, materially changed, moved, or removed and discovery signals should be updated or verified.

## Process
1. [HYBRID] Confirm the production URL/change is real and intended. Check status behavior, canonical target, index directive, rendering, and required content before sending discovery signals.
2. [HYBRID] Update relevant internal links, navigation, hubs, XML sitemaps, feeds, or other discovery surfaces when they should reflect the change; remove obsolete URL variants where appropriate.
3. [HYBRID] When a supported URL-notification mechanism is useful for the relevant search surface, use it for eligible additions, updates, or deletions. IndexNow is one possible mechanism when the site and target engines support it; it is not a universal requirement.
4. [HYBRID] If a notification mechanism requires configuration or credentials, use the host's available integration securely rather than storing secrets in AURA. Batch or retry only as appropriate to the actual service and current limits.
5. [AI] Preserve the material publish/change time, affected URLs, intended canonical relationship, and relevant search/answer/local surfaces when remembering them improves later diagnosis or measurement.
6. [HYBRID] Verify the resulting crawl/index state through appropriate evidence. A successful sitemap update, URL submission, or notification response proves only that the signal was sent or exposed—not that a crawler processed it or that indexing/ranking occurred.

## Verification
- Discovery signals represent the intended live URL state rather than stale or accidental variants.
- Notification/submission success is not reported as crawl, indexing, ranking, or business-outcome proof.
- Mechanism choice follows the actual surfaces and host capabilities rather than a required provider abstraction.
