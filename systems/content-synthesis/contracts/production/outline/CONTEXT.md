---
id: content.production.outline
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
# Content Outline

## Purpose
Translate the approved brief and narrative structure into an executable section-by-section production outline.

## Business Outcome
Reduce drafting drift by making every section’s purpose, evidence, example, and transition explicit before writing.

## Run When
Run before long-form or structurally complex content when a production outline is useful.

## Process
1. [DETERMINISTIC] Load the approved brief, narrative structure, evidence plan, desired action, and platform constraints.
2. [AI] Create ordered sections/beats with one clear job each and expected audience state after each.
3. [AI] Attach required claims, evidence, examples, demonstrations, visuals/audio, and transitions to the relevant section.
4. [AI] Allocate depth according to audience need and objective, not equal length across sections.
5. [HYBRID] Remove duplicated points, missing prerequisites, unsupported sections, and sections that do not advance the core message.
6. [AI] Mark optional/cuttable sections and version-specific branches where needed.
7. [DETERMINISTIC] Produce a production-ready outline with source refs and constraints.
