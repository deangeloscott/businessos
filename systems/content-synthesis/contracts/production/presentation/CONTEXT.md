---
id: content.production.presentation
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
  - content.strategy.core-message
  - content.strategy.narrative-structure
  - content.strategy.evidence-proof-plan
  - content.production.outline
  - content.production.visual-direction
  - content.qa.pre-publish
---
# Presentation / Slideshow Production

## Purpose
Build a presentation that supports a live or asynchronous audience journey instead of turning a document into slides.

## Business Outcome
Create or improve presentation / slideshow production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires presentation / slideshow production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define audience, setting, presenter/no-presenter mode, decision/learning objective, duration, and expected prior knowledge.
2. [AI] Build narrative arc and section sequence around audience questions/decisions rather than source-document headings.
3. [AI] Assign one main message per slide; choose charts, diagrams, examples, demonstrations, quotes, or sparse text according to the slide job.
4. [HYBRID] Separate speaker notes from visible slide content and prevent slide text from becoming a transcript.
5. [INTEGRATION] Render slides through available presentation capability or produce complete slide-by-slide production specification.
6. [HYBRID] Check narrative continuity, readability at viewing distance, data accuracy, source attribution, brand, and timing.
7. [DETERMINISTIC] Save the final presentation Asset and supporting notes/source references.
