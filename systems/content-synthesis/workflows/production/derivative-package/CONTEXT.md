---
id: content.production.derivative-package
type: workflow
owner_system: content-synthesis
reads:
- Asset
- Insight
- ProofRecord
- WorkRequest
- PlatformProfile
writes:
- Asset
context:
- AudienceSegment
- Brand
- Objective
---
# Derivative Asset Package

## Purpose
Create only the useful supporting or derivative forms of an approved core Asset—such as full/bullet scripts, shot list, captions, clips, thumbnail concepts, audio, or graphics—without creating unnecessary variants.

## Business Outcome
Reduce repeated production work and make high-value content easier to execute/distribute while preserving one canonical idea, evidence chain, and brand standard.

## Run When
Use when an approved Asset needs production aids or additional representations that support the same underlying idea and do not justify separate Opportunities.

## Process
1. [DETERMINISTIC] Identify the canonical Asset, intended production/distribution uses, existing derivatives, and which additional outputs are actually required.
2. [AI] Select only useful derivatives such as full script, bulletized speaking script, shot/B-roll list, caption/subtitle text, title/description, thumbnail concepts, stills, quote cards, short clips, audio-only version, or transcript.
3. [AI] Adapt each derivative to its operational job while preserving the core meaning, proof constraints, CTA, and factual claims; do not mechanically duplicate formats that add no value.
4. [HYBRID] Use PlatformProfiles when a derivative will be consumed directly on a particular surface and native conventions materially change it.
5. [INTEGRATION] Generate/render available derivatives with the active harness's tools, or produce a clear production specification when final rendering is unavailable and the specification itself remains useful.
6. [HYBRID] QA each derivative for consistency with the canonical Asset while allowing necessary format-specific differences.
7. [DETERMINISTIC] Preserve useful derivative Assets linked to the canonical Asset. Link a WorkRequest only when one genuinely supplied durable handoff context; do not create one as routine production plumbing.
