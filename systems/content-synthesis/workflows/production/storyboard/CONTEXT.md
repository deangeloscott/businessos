---
id: content.production.storyboard
type: workflow
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
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Storyboard

## Purpose
Map audiovisual content beat-by-beat so visuals, audio, text, and action jointly communicate the message.

## Business Outcome
Use the medium to show and explain rather than placing decorative visuals over a spoken essay.

## Run When
Run for video, animation, carousel-like motion, or presentation content needing coordinated visual sequencing.

## Process
1. [DETERMINISTIC] Load the approved script/outline, visual direction, platform constraints, proof assets, and production capabilities.
2. [AI] Divide the content into shots/scenes/frames aligned to message beats and audience attention changes.
3. [AI] For each beat define what is seen, heard, read, demonstrated, and why the visual is necessary.
4. [AI] Prefer real demonstrations, diagrams, examples, source/proof visuals, and meaningful motion over generic decorative B-roll.
5. [HYBRID] Check continuity, cognitive load, legibility, pacing, rights/permissions, and whether visuals accidentally imply unsupported facts.
6. [AI] Identify reusable assets and production dependencies; create WorkRequests only where a separate production capability is required.
7. [DETERMINISTIC] Produce an ordered storyboard with timing and source/asset refs.
