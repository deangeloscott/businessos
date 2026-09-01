---
id: seo.execution.technical.robots
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
# Robots

## Purpose
Safely manage robots.txt crawler controls.

## Business Outcome
Improve valuable organic discovery through robots, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Robots**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Parse all applicable user-agent groups and rule precedence.
2. [AI] Identify intended versus accidental disallows/allows for target crawlers.
3. [HYBRID] Confirm robots.txt is not being used as a guaranteed indexing-removal method.
4. [AI] Check sitemap declarations and robots.txt accessibility/status.
5. [HYBRID] Simulate representative allowed/blocked URLs including wildcard/boundary cases.
6. [HYBRID] Create the smallest rule change possible and preserve a backup.
7. [INTEGRATION] Deploy, refetch, test boundary URLs, and define SEO monitoring for crawl/index effects.

## Verification
- Test affected URL sets and rollback path before broad deployment; verify crawl/index behavior afterward.


