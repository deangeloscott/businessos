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
Use for video/animation/social content where captions or text overlays are appropriate.

## Process
1. [DETERMINISTIC] Resolve final script/audio timing and platform caption constraints.
2. [AI] Segment spoken language into readable phrases preserving meaning and emphasis.
3. [AI] Decide what should be verbatim captions versus selective on-screen emphasis, labels, numbers, or definitions.
4. [HYBRID] Check names, figures, technical terms, punctuation, timing, speaker changes, and claims against source/script.
5. [DETERMINISTIC] Enforce safe areas, reading speed, contrast, line length, and accessibility requirements.
6. [AI] Avoid redundant text that competes with diagrams/demonstrations or changes the meaning through shortening.
7. [DETERMINISTIC] Produce and preserve the useful caption file/text-overlay Asset and verify it against the final render when one exists.
