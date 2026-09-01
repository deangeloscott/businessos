---
id: content.production.image
type: playbook
owner_system: content-synthesis
artifact_role: customer_facing_production_root
reads:
- WorkRequest
- Opportunity
- Insight
- SourceRecord
- Asset
- ProofRecord
writes:
- Asset
- Observation
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - creative.image.generate
  - creative.image.edit
  - creative.audio.generate
  - creative.video.generate
  - creative.animation.generate
  - video.render
  - presentation.render
  - document.render
context:
- AudienceSegment
- Brand
---
# Image / Graphic Production

## Purpose
Create a visual asset whose composition communicates the intended idea rather than adding decoration.

## Business Outcome
Create or improve image / graphic production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires image / graphic production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define what the visual must communicate and whether the job is diagram, data graphic, conceptual illustration, product visual, social creative, thumbnail, or explanatory image.
2. [AI] Select composition, hierarchy, subject, labels/text, aspect ratio, and visual metaphor based on audience/platform.
3. [HYBRID] Verify any depicted data, UI, product, people, logos, or claims are accurate/authorized and avoid misleading synthetic evidence.
4. [INTEGRATION] Generate or assemble image with the appropriate creative capability.
5. [HYBRID] Inspect final image for visual errors, legibility, unintended artifacts, brand fit, accessibility/alt-text needs, and platform crop/safe areas.
6. [DETERMINISTIC] Save versioned Asset plus source/prompt/design provenance where useful.
