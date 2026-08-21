---
id: content.production.audio
type: playbook
version: 1.1.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
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
# Audio Asset Production

## Purpose
Produce voiceover, narration, clip, or other audio asset optimized for its actual use context.

## Business Outcome
Create or improve audio asset production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires audio asset production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define function, duration, voice/persona constraints, pronunciation, emotional delivery, and surrounding media context.
2. [AI] Write or adapt script for spoken language rather than reading written prose verbatim.
3. [HYBRID] Mark emphasis, pauses, pronunciation, timing, and accessibility/transcript requirements.
4. [INTEGRATION] Generate/record/edit audio with available capability.
5. [HYBRID] Listen/review for mispronunciation, artifacts, pacing, factual accuracy, and brand tone.
6. [DETERMINISTIC] Save versioned Asset and transcript.
