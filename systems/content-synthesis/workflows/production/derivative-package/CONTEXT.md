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
Create only useful supporting or derivative forms of a core Asset or working source, such as scripts, shot lists, captions, clips, audio, graphics, or localized versions.

## Business Outcome
Reduce repeated production work and make high-value content easier to execute/distribute while preserving one canonical idea, evidence chain, and brand standard.

## Run When
Use when an existing core Asset or working source needs production aids, translated captions, localized media, or additional representations supporting the same underlying idea. Preserve an approved/canonical Asset when one exists; do not make approval a prerequisite for useful local drafting.

## Process
1. [DETERMINISTIC] Identify the canonical Asset or current working source, intended production/distribution uses, existing derivatives, and which additional outputs are actually required.
2. [AI] Select only useful derivatives such as full script, bulletized speaking script, shot/B-roll list, caption/subtitle text, title/description, thumbnail concepts, stills, quote cards, short clips, audio-only version, or transcript.
3. [AI] Adapt each derivative to its operational job while preserving the core meaning, proof constraints, any relevant CTA, and factual claims; do not mechanically duplicate formats that add no value. For another language or market, the optional localization reference can help preserve meaning across speech, graphics, and timing.
4. [HYBRID] Use PlatformProfiles when a derivative will be consumed directly on a particular surface and native conventions materially change it.
5. [INTEGRATION] Generate/render available derivatives with the active harness's tools, or produce a clear production specification when final rendering is unavailable and the specification itself remains useful.
6. [HYBRID] QA each derivative for consistency with the canonical Asset while allowing necessary format-specific differences.
7. [DETERMINISTIC] Preserve useful derivative Assets linked to the canonical Asset. Link a WorkRequest only when one genuinely supplied durable handoff context; do not create one as routine production plumbing.

## Optional craft references

Use the [creative localization reference](../../../../../recipes/creative/creative-localization.md) when language or market adaptation needs specialist craft beyond the current plan.
