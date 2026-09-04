---
id: content.production.short-video
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
# Short-Form Video Production

## Purpose
Express one useful idea quickly through platform-native visual/audio pacing and proof.

## Business Outcome
Create or improve short-form video production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires short-form video production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Reduce the source idea to one viewer promise or tension that can be resolved within the intended duration. Draw on current audience, message, hook, script, storyboard, platform, or related operating knowledge only when useful.
2. [AI] Design the first seconds around immediate context, stakes, demonstration, surprising evidence, or clear question rather than generic introduction.
3. [AI] Build beat-by-beat script with spoken line, visual action/B-roll/on-screen text, proof/demo, pattern changes, and payoff.
4. [HYBRID] Ensure pacing serves comprehension; remove needless cuts/effects that compete with meaning.
5. [AI] Write captions/on-screen text for sound-off comprehension where appropriate and ensure visual claims match evidence.
6. [HYBRID] Specify platform aspect ratio, safe areas, duration, audio/music constraints, CTA, and render requirements.
7. [INTEGRATION] Generate/render available media or preserve a complete production specification when that remains useful. Local deterministic media processing such as FFmpeg may handle clip/transcode/frame/audio/render mechanics while the model/harness remains responsible for creative judgment and QA.
8. [HYBRID] Review final render for factual, visual, audio, brand, and platform integrity before Asset completion. Draw on platform/pre-publish QA operating knowledge when an additional integrated review is useful.
