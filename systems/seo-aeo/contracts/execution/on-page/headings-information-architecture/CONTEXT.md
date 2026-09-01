---
id: seo.execution.on-page.headings-information-architecture
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
  - cms.page.read
  optional:
  - search.serp.read
  - search.performance.read
  - cms.page.update
---
# Headings Information Architecture

## Purpose
Make page structure easy to scan, understand, and navigate.

## Business Outcome
Improve valuable organic discovery through headings information architecture, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Headings Information Architecture**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Extract current content/heading outline.
2. [AI] Map required user questions/tasks and buying decisions to sections.
3. [HYBRID] Group related information and eliminate redundant/fragmented sections.
4. [HYBRID] Use clear descriptive headings rather than keyword-stuffed labels.
5. [HYBRID] Correct heading hierarchy where it improves document structure/accessibility.
6. [HYBRID] Place important decision information where users can reach it efficiently.
7. [HYBRID] Add table of contents/jump navigation only when page length/complexity warrants it.


