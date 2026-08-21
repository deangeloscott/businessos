---
id: seo.execution.technical.javascript-rendering
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
# Javascript Rendering

## Purpose
Ensure important content, links, metadata, and directives survive the rendering path.

## Business Outcome
Improve valuable organic discovery through javascript rendering, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Javascript Rendering**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Compare raw HTML, rendered DOM, and user-visible output across representative templates.
2. [HYBRID] Check main content, internal links, titles/meta, canonical, robots directives, structured data, lazy-loaded media, and error states.
3. [AI] Identify blocked resources, hydration failures, delayed/infinite loading, interaction-only content, or client-side routing defects.
4. [HYBRID] Prefer robust server/pre-rendered delivery for critical discovery elements when appropriate; otherwise make client rendering reliable.
5. [HYBRID] Test slow/error paths and representative devices/agents.
6. [INTEGRATION] Deploy and re-test raw/rendered parity and crawlability.


