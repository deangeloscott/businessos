---
id: seo.execution.indexing.index-status
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
# Index Status Tracking

## Purpose
Track whether priority assets move through expected discovery, crawl, canonical, and index states.

## Business Outcome
Improve valuable organic discovery through index status tracking, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Index Status Tracking**, or when an authorized incident response requires it.

## Process
1. [INTEGRATION] For each priority URL, retrieve available index/crawl/search observations and timestamps.
2. [INTEGRATION] Separate URL accessibility, crawl permission, crawl occurrence, renderability, canonical selection, index eligibility, indexed state, and serving/ranking evidence.
3. [INTEGRATION] Compare actual state with intended asset state and publish/change timeline.
4. [INTEGRATION] Classify normal lag, unobserved state, exclusion by design, canonical substitution, crawl issue, quality/duplication issue, or unknown.
5. [HYBRID] Create troubleshooting Opportunities only when the state is material and outside expected behavior.
6. [HYBRID] Close monitoring only when intended state is verified or the business explicitly accepts the observed state.


