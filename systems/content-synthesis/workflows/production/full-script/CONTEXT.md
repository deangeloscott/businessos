---
id: content.production.full-script
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
- WorkRequest
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Full Content Script

## Purpose
Write a complete spoken or presentation script from an approved brief/structure with natural language and production cues.

## Business Outcome
Produce a record-ready script that communicates the intended message accurately and in the brand/platform voice.

## Run When
Run when video, podcast, presentation, webinar-support, avatar, or other spoken content requires full scripting.

## Process
1. [AI] Draft from the approved outline, preserving the exact purpose of each beat and evidence limitations.
2. [AI] Write for speech rather than essay prose: natural syntax, clear transitions, appropriate sentence length, and explicit context where visuals cannot carry it.
3. [AI] Integrate demonstrations, examples, proof, visual cues, pauses/emphasis, and transitions only where they support comprehension.
4. [AI] Ensure the hook is paid off quickly and the core message remains recognizable throughout.
5. [HYBRID] Check claims, tone, timing, jargon, pronunciation-sensitive terms, and any regulated/sensitive language.
6. [AI] Read/revise for spoken flow and remove repetition, throat-clearing, filler, and overly dense passages.
7. [DETERMINISTIC] Output final script with production cues and linked evidence/asset requirements.
