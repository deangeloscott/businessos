---
id: content.production.carousel
type: workflow
owner_system: content-synthesis
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
context:
- AudienceSegment
- Brand
---
# Carousel / Slideshow Production

## Purpose
Turn an idea into a sequential visual argument where each frame earns the next.

## Business Outcome
Communicate the idea as a visual sequence that earns the next frame, builds understanding, and preserves evidence/Proof constraints.

## Run When
Use when a carousel/slideshow is the useful communication output and existing Assets do not already satisfy the need.

## Process
1. [AI] Define one core takeaway and why sequential visual progression improves understanding.
2. [HYBRID] If the carousel uses a ProofRecord, preserve the exact supported claim, source/permission constraints, and original screenshot/media reference; do not turn one result into a universal claim.
3. [AI] Storyboard the sequence: cover promise/context → setup → evidence/steps/comparison → synthesis → action.
4. [AI] Limit each slide to one primary job; use diagrams, examples, charts, contrast, or typography rather than shrinking paragraphs.
5. [HYBRID] Ensure the cover is specific/truthful and the sequence works even when skimmed.
6. [AI] Write concise slide copy and visual direction, maintaining hierarchy and continuity.
7. [INTEGRATION] Generate/design the slides using the active harness's available creative/rendering tools, or produce a complete production specification when final rendering is unavailable.
8. [HYBRID] Review legibility, platform dimensions, evidence accuracy, brand consistency, and sequence before preserving the useful Asset.
