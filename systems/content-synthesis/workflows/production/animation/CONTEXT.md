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
Create or improve animation, motion graphics, or character performance for explanation, storytelling, entertainment, emotion, or atmosphere.

## Business Outcome
Create or improve animation / motion production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Use for animated stories, a recurring mascot or character series, explanatory motion, or refinement of existing animation when current Assets do not satisfy the intended experience.

## Process
1. [AI] Define the intended understanding, feeling, performance, or experience, along with the useful sequence, duration, and role of motion. A story, joke, mood, or expressive moment need not become an explanation or sales message.
2. [AI] Plan key poses, scenes, or other useful visual states with action, transitions, timing, and narration/text only where needed. For character work, make intention, staging, contact, and reaction readable; a rough pose or timing pass can resolve a difficult performance before fine detail when useful.
3. [HYBRID] Validate data, claims, product states, and visual causality so motion does not imply unsupported relationships.
4. [INTEGRATION] Generate or render the animation with suitable native tools or combinations of code, image assets, motion tools, and renderers. A dedicated animation generator is not required. Preserve the requested quality and editability; produce complete keyframe/timing specifications when rendering is genuinely unavailable or the specification itself is requested.
5. [HYBRID] Review the actual sequence for the intended effect, readable performance, physical/spatial continuity, timing, and relevant legibility, loop behavior, compression, accessibility, and brand quality. Correct material weaknesses and compare the revision with the useful prior result; shared render/package guidance can help without prescribing a host execution loop.
6. [DETERMINISTIC] Preserve the useful versioned Asset with production/source references. Use relevant QA operating knowledge when the artifact/destination warrants it; do not create an internal routing stage merely to complete the Workflow.

## Optional craft references

For character acting and coherent settings, the [identity and continuity reference](../../../../../recipes/creative/video/notes/identity-and-continuity.md) and [continuity and narrative notes](../../../../../recipes/creative/video/notes/continuity-and-narrative.md) offer optional performance and staging advice. For actual models, rigs, or scenes, use the [3D production reference](../../../../../recipes/creative/3d-production.md) when those craft concerns matter.

When a motion graphic is the useful form, the [motion graphics starting points](../../../../../recipes/creative/motion-graphics/INDEX.md) offer adaptable ideas for numbers, statements, state changes, demo callouts, mechanisms, and title/closing moments. Use the [shared audio starting points](../../../../../recipes/creative/audio/INDEX.md) when voice, music, sound design, or an audio-only variation would improve the communication. These are optional references; the model or user may use another motion plan or tool-native method.
