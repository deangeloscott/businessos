---
id: content.production.podcast
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
  - content.strategy.narrative-structure
  - content.production.outline
  - content.production.audio-direction
  - content.qa.pre-publish
---
# Podcast Episode Production

## Purpose
Create an audio-first episode whose structure and delivery fit listening context.

## Business Outcome
Create or improve podcast episode production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires podcast episode production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define listener promise, format (solo/interview/cohost/narrative), expected listening context, depth, and CTA.
2. [AI] Build episode arc with cold open/introduction, segments/questions, stories/examples, transitions, synthesis, and close.
3. [HYBRID] For interviews, design questions that elicit evidence/stories rather than scripted agreement.
4. [AI] Produce host script/talking points, research notes, pronunciation/source notes, and edit markers.
5. [INTEGRATION] Record/generate/edit audio where capabilities exist or produce a complete recording/edit packet.
6. [HYBRID] Review audio quality, factual claims, pacing, repetition, ads/disclosures, and final metadata/show notes.
7. [DETERMINISTIC] Save episode Asset and transcript/source references.
