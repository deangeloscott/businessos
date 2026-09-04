---
id: content.production.podcast
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
# Podcast Episode Production

## Purpose
Create an audio-first episode whose structure and delivery fit listening context.

## Business Outcome
Create or improve podcast episode production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires podcast episode production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define listener promise, format (solo/interview/cohost/narrative), expected listening context, depth, and CTA. Draw on current audience, message, narrative, outline, audio-direction, or related operating knowledge only when useful.
2. [AI] Build episode arc with cold open/introduction, segments/questions, stories/examples, transitions, synthesis, and close.
3. [HYBRID] For interviews, design questions that elicit evidence/stories rather than scripted agreement.
4. [AI] Produce host script/talking points, research notes, pronunciation/source notes, and edit markers.
5. [INTEGRATION] Record/generate/edit audio where capabilities exist or preserve a complete recording/edit specification when that remains useful.
6. [HYBRID] Review audio quality, factual claims, pacing, repetition, ads/disclosures, and final metadata/show notes. Draw on pre-publish QA operating knowledge when an additional integrated review is useful.
7. [DETERMINISTIC] Save the useful versioned episode Asset and transcript/source references.
