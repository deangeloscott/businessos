---
id: content.production.captions
type: playbook
version: 1.3.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 2
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- ActionPacket
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
# Captions and On-Screen Text

## Purpose
Design captions/on-screen text that improve comprehension and accessibility without overwhelming the visual.

## Business Outcome
Make audiovisual content understandable in muted/noisy contexts and reinforce key information.

## Run When
Run for video/animation/social content where captions or text overlays are appropriate.

## Process
1. [DETERMINISTIC] Resolve final script/audio timing and platform caption constraints.
2. [AI] Segment spoken language into readable phrases preserving meaning and emphasis.
3. [AI] Decide what should be verbatim captions versus selective on-screen emphasis, labels, numbers, or definitions.
4. [HYBRID] Check names, figures, technical terms, punctuation, timing, speaker changes, and claims against source/script.
5. [DETERMINISTIC] Enforce safe areas, reading speed, contrast, line length, and accessibility requirements.
6. [AI] Avoid redundant text that competes with diagrams/demonstrations or changes the meaning through shortening.
7. [DETERMINISTIC] Produce caption file/text-overlay plan and verify against final render.
