---
id: content.production.long-video
type: playbook
version: 1.3.0
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
subcontracts:
  required:
  - content.intake.content-brief
  - content.strategy.audience-context
  - content.strategy.core-message
  - content.strategy.hook
  - content.strategy.narrative-structure
  - content.strategy.evidence-proof-plan
  - content.production.outline
  - content.production.full-script
  - content.production.storyboard
  - content.production.shot-list
  - content.production.visual-direction
  - content.qa.pre-publish
---
# Long-Form Video Production

## Purpose
Create sustained video communication with narrative/educational progression, demonstrations, and retention-aware structure.

## Business Outcome
Create or improve long-form video production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires long-form video production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define viewer promise, audience knowledge, intended depth, proof/demo needs, and desired post-view action.
2. [AI] Design macro structure: opening payoff/stakes, roadmap/context, escalating sections, examples/demos, objections, synthesis, close.
3. [AI] Script or outline at the appropriate level for presenter style; include visual plan, B-roll, graphics, screen demos, and chapter transitions.
4. [HYBRID] Front-load value and establish why continued attention is worthwhile without artificially delaying the answer.
5. [AI] Use callbacks, open questions, examples, pacing changes, and visual reinforcement only when they improve retention/comprehension.
6. [HYBRID] Fact-check all consequential claims and ensure source/proof materials are production-accessible.
7. [INTEGRATION] Generate/render or package complete production instructions, thumbnails/title concepts where in scope, captions, and chapters.
8. [HYBRID] Review final asset against audience value, technical quality, brand, factual integrity, and platform requirements.
