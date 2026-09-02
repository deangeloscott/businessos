---
id: content.production.carousel
type: workflow
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
Run when an Opportunity or WorkRequest requires carousel / slideshow production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define one core takeaway and why sequential visual progression improves understanding.
2. [HYBRID] If the carousel uses a ProofRecord, preserve the exact supported claim, source/permission constraints, and original screenshot/media reference; do not turn one result into a universal claim.
3. [AI] Storyboard the sequence: cover promise/context → setup → evidence/steps/comparison → synthesis → action.
4. [AI] Limit each slide to one primary job; use diagrams, examples, charts, contrast, or typography rather than shrinking paragraphs.
5. [HYBRID] Ensure the cover is specific/truthful and the sequence works even when skimmed.
6. [AI] Write concise slide copy and visual direction, maintaining hierarchy and continuity.
7. [INTEGRATION] Generate/design the slides using available creative/rendering capabilities or a complete human production packet.
8. [HYBRID] Review legibility, platform dimensions, evidence accuracy, brand consistency, and sequence before Asset completion.