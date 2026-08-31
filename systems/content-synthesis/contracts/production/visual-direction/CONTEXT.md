---
id: content.production.visual-direction
type: playbook
version: 1.3.0
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - creative.image.generate
  - creative.audio.generate
  - creative.video.generate
  - creative.animation.generate
  - creative.avatar_video.generate
  - video.render
  - presentation.render
  - document.render
  - social.content.publish
  - social.content.schedule
  - cms.page.publish
  - email.content.publish
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Visual Direction

## Purpose
Define a coherent visual language that supports the message, brand, and platform before asset generation.

## Business Outcome
Make visuals purposeful and consistent instead of a series of unrelated generated images.

## Run When
Run when an asset needs a visual concept beyond existing brand templates or supplied footage.

## Process
1. [DETERMINISTIC] Resolve Brand visual context, message, audience, platform profile, existing reusable Assets, and production constraints.
2. [AI] Define visual concept, information hierarchy, subject treatment, composition, typography role, iconography/diagram style, motion approach, and realism/stylization where appropriate.
3. [AI] Tie each visual choice to communication function rather than aesthetic preference alone.
4. [HYBRID] Check brand consistency, accessibility, cultural/context appropriateness, and risk of misleading synthetic representation.
5. [AI] Specify consistency rules across frames/slides/scenes and what may intentionally vary.
6. [AI] Identify assets requiring real screenshots/proof versus generated illustration.
7. [DETERMINISTIC] Produce a visual-direction brief for image/video/presentation generation or human production.
