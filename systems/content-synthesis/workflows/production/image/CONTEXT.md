---
id: content.production.image
type: workflow
owner_system: content-synthesis
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
Use when an image or graphic is the useful communication output and existing Assets do not already satisfy the need. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define what the visual must communicate and whether the job is diagram, data graphic, conceptual illustration, product visual, social creative, thumbnail, or explanatory image.
2. [AI] Select composition, hierarchy, subject, labels/text, aspect ratio, and visual metaphor based on audience/platform.
3. [HYBRID] Verify any depicted data, UI, product, people, logos, or claims are accurate/authorized and avoid misleading synthetic evidence.
4. [INTEGRATION] Generate or assemble the image with the appropriate creative capability available to the active model/harness/user.
5. [HYBRID] Inspect the final image for visual errors, legibility, unintended artifacts, brand fit, accessibility/alt-text needs, and platform crop/safe areas. Draw on additional QA knowledge when it materially improves the artifact; no separate QA Workflow is mandatory merely because it exists.
6. [DETERMINISTIC] Save the useful versioned Asset plus source/prompt/design provenance where future work benefits.
