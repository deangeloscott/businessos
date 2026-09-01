---
id: content.production.thumbnail
type: playbook
owner_system: content-synthesis
artifact_role: customer_facing_production_root
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
# Content Thumbnail Concept

## Purpose
Design a thumbnail/cover image that quickly communicates the content’s real subject, tension, or outcome at browsing scale.

## Business Outcome
Increase qualified starts while maintaining expectation match with the actual content.

## Run When
Run for platforms/formats where a thumbnail or cover materially affects selection.

## Process
1. [AI] Determine the single visual idea that best communicates subject/value before reading detailed text.
2. [AI] Coordinate with the title so image and text add information rather than redundantly repeat it.
3. [AI] Generate distinct concepts using subject, demonstration/result, contrast, recognizable object/context, or simple visual tension.
4. [HYBRID] Reject deceptive before/after, fabricated reaction, unreadable complexity, misleading scale, or synthetic evidence presented as real.
5. [AI] Specify composition, focal subject, minimal text if needed, visual hierarchy, and brand/platform constraints.
6. [DETERMINISTIC] Define mobile/small-size legibility and variant-test plan where relevant.
7. [AI] Create a Content WorkRequest/Asset brief for image production and verify final title-thumbnail match.
