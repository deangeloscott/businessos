---
id: content.production.animation
type: playbook
version: 1.1.0
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
---
# Animation / Motion Production

## Purpose
Use motion to explain change, sequence, causality, demonstration, or attention hierarchy.

## Business Outcome
Create or improve animation / motion production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires animation / motion production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define the exact communication objective, sequence, visual states, duration, and why motion improves understanding.
2. [AI] Storyboard keyframes/scenes with narration or text, transitions, timing, and interaction between visual elements.
3. [HYBRID] Validate data, claims, product states, and visual causality so motion does not imply unsupported relationships.
4. [INTEGRATION] Generate or render the animation with the available capability, or produce complete keyframe/timing specifications for human production.
5. [HYBRID] Review timing, legibility, loop behavior where relevant, compression, accessibility, and brand quality.
6. [DETERMINISTIC] Save the versioned Asset with production/source references and route it to required QA.
