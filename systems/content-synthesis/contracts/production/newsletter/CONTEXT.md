---
id: content.production.newsletter
type: playbook
owner_system: content-synthesis
artifact_role: customer_facing_production_root
reads:
- WorkRequest
- Opportunity
- Insight
- SourceRecord
- Asset
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
subcontracts:
  required:
  - content.intake.content-brief
  - content.strategy.audience-context
  - content.strategy.core-message
  - content.strategy.hook
  - content.strategy.narrative-structure
  - content.qa.pre-publish
---
# Newsletter Production

## Purpose
Create a relationship-oriented email/newsletter suited to inbox context and the audience expectation.

## Business Outcome
Create or improve newsletter production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires newsletter production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define the subscriber context, expected relationship, single primary idea, value promise, and desired action.
2. [AI] Choose structure appropriate to newsletter type: insight note, curated analysis, story/lesson, update, digest, or educational sequence.
3. [AI] Draft subject/preheader/body with a compelling but truthful opening and early value delivery.
4. [HYBRID] Use links/CTAs proportionately; avoid turning every educational newsletter into a sales letter unless Marketing owns that objective.
5. [AI] Optimize scannability, paragraph length, hierarchy, and mobile inbox reading.
6. [HYBRID] Verify claims, links, personalization tokens, brand/compliance, and deliverable formatting.
7. [DETERMINISTIC] Save Asset and route publishing only when authorization/capability exists.
