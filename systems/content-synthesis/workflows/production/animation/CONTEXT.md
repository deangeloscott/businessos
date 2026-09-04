---
id: content.production.animation
type: workflow
owner_system: content-synthesis
reads:
- WorkRequest
- Opportunity
- Insight
- SourceRecord
- Asset
writes:
- Asset
- Observation
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
Use when animation/motion is the useful communication output and existing Assets do not already satisfy the need.

## Process
1. [AI] Define the exact communication objective, sequence, visual states, duration, and why motion improves understanding.
2. [AI] Storyboard keyframes/scenes with narration or text, transitions, timing, and interaction between visual elements.
3. [HYBRID] Validate data, claims, product states, and visual causality so motion does not imply unsupported relationships.
4. [INTEGRATION] Generate or render the animation with the active harness's available tools, or produce complete keyframe/timing specifications when that remains a useful deliverable.
5. [HYBRID] Review timing, legibility, loop behavior where relevant, compression, accessibility, and brand quality.
6. [DETERMINISTIC] Preserve the useful versioned Asset with production/source references. Use relevant QA operating knowledge when the artifact/destination warrants it; do not create an internal routing stage merely to complete the Workflow.
