---
id: content.production.audio-direction
type: playbook
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
# Content Audio Direction

## Purpose
Plan voice, music, sound, pacing, and silence as communication elements rather than afterthoughts.

## Business Outcome
Improve clarity, emotion, and professionalism without letting audio obscure the message.

## Run When
Run for podcast, video, animation, avatar, or audio-first content needing defined sound treatment.

## Process
1. [DETERMINISTIC] Resolve audience, brand, script, format/platform, speaker/voice options, and rights constraints.
2. [AI] Define voice character, pacing, emphasis, pronunciation, conversational/formal level, and use of silence.
3. [AI] Identify where music/sound effects meaningfully support transitions, demonstrations, mood, or attention and where silence is stronger.
4. [HYBRID] Avoid emotionally manipulative sound choices that conflict with factual tone or accessibility.
5. [DETERMINISTIC] Specify loudness, music-under-dialogue, intro/outro, file/format, and accessibility requirements.
6. [AI] Mark exact script moments requiring pronunciation notes, emphasis, sound cue, or no-music treatment.
7. [DETERMINISTIC] Produce audio-direction instructions for human or generative production and final QA.
