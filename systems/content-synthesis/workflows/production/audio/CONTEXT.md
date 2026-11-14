---
id: content.production.audio
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
# Audio Asset Production

## Purpose
Produce voiceover, narration, a musical cue, sound design, or another audio asset suited to its actual use context.

## Business Outcome
Create or improve audio asset production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Use when producing or improving narration, voiceover, a musical cue, sound design, or an audio loop and existing Assets do not satisfy the need.

## Process
1. [AI] Define function, duration, intended effect, and surrounding media context, including relevant voice/persona or musical constraints.
2. [AI] For speech, write or adapt text for listening. For music or designed sound, define the useful structure, cue points, or sound relationships without requiring a spoken script.
3. [HYBRID] Specify relevant delivery, pronunciation, timing, endings/loops, and accessibility needs; use transcripts when the content calls for them.
4. [INTEGRATION] Generate/record/edit audio with the active harness's available tools.
5. [HYBRID] Listen/review for the intended effect, artifacts, pacing, audibility, relevant pronunciation and factual accuracy, and a suitable ending or loop. Use render/package guidance for material corrections when helpful.
6. [DETERMINISTIC] Preserve the useful versioned Asset, relevant transcript, and useful editable source with production lineage where future work benefits.

## Optional craft references

When the audio needs a starting idea, open the [shared audio starting points](../../../../../recipes/creative/audio/INDEX.md) and borrow the smallest useful treatment. The recipes are cross-medium creative references, not a required prompt format or mixing specification.
