---
id: seo.execution.internal-linking.contextual-linking
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
# Contextual Linking

## Purpose
Add useful links where one asset naturally answers the next question or advances the buyer journey.

## Business Outcome
Improve valuable organic discovery through contextual linking, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Contextual Linking**, or when an authorized incident response requires it.

## Process
1. [HYBRID] For the target opportunity, find candidate source pages through semantic relevance, shared entities, journey adjacency, and audience overlap.
2. [HYBRID] Inspect candidate passages to ensure the link is genuinely useful in that local context.
3. [HYBRID] Choose the correct target when multiple pages compete; open a cannibalization Opportunity if intent ownership is unclear.
4. [HYBRID] Write or edit the smallest amount of surrounding copy needed to make the link useful and understandable.
5. [DETERMINISTIC] Log the source-target relationship and intended user/search purpose.
6. [HYBRID] Verify the rendered link and define SEO monitoring for target/source effects.


