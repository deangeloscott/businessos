---
id: content.production.captions
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
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Captions and On-Screen Text

## Purpose
Design captions/on-screen text that improve comprehension and accessibility without overwhelming the visual.

## Business Outcome
Make audiovisual content understandable in muted/noisy contexts and reinforce key information.

## Run When
Use for video, animation, or social content needing captions, translated subtitles, or readable on-screen text and graphics.

## Process
1. [DETERMINISTIC] Resolve final script/audio timing and platform caption constraints.
2. [AI] Segment spoken language into readable phrases preserving meaning and emphasis.
3. [AI] Decide what should be verbatim captions versus selective on-screen emphasis, labels, numbers, or definitions.
4. [HYBRID] Check names, figures, technical terms, punctuation, timing, speaker changes, and claims against source/script. Preserve important non-speech information when captions serve accessibility; a translation of dialogue alone may not cover that need.
5. [DETERMINISTIC] Enforce safe areas, reading speed, contrast, line length, and accessibility requirements.
6. [AI] Avoid redundant text that competes with diagrams/demonstrations or changes the meaning through shortening.
7. [DETERMINISTIC] Produce and preserve the useful caption file/text-overlay Asset and verify it against the final render when one exists.

## Optional craft references

For translated subtitles, terminology, text expansion, reading direction, or adapted graphics, use the [creative localization reference](../../../../../recipes/creative/creative-localization.md) when those concerns affect the result.
