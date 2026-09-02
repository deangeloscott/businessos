---
id: content.production.derivative-package
type: workflow
owner_system: content-synthesis
artifact_role: customer_facing_production_root
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
Run when an approved Asset needs production aids or additional representations that support the same underlying intervention and therefore do not justify separate Opportunities.

## Process
1. [DETERMINISTIC] Identify the canonical Asset, intended production/distribution uses, existing derivatives, and which additional outputs are actually required.
2. [AI] Select only useful derivatives such as full script, bulletized speaking script, shot/B-roll list, caption/subtitle text, title/description, thumbnail concepts, stills, quote cards, short clips, audio-only version, or transcript.
3. [AI] Adapt each derivative to its operational job while preserving the core meaning, proof constraints, CTA, and factual claims; do not mechanically duplicate formats that add no value.
4. [HYBRID] Use PlatformProfiles when a derivative will be consumed directly on a particular surface and native conventions materially change it.
5. [INTEGRATION] Generate/render available derivatives or produce clear manual production instructions for unavailable capabilities.
6. [HYBRID] QA each derivative for consistency with the canonical Asset while allowing necessary format-specific differences.
7. [DETERMINISTIC] Register derivatives as Assets linked to the canonical Asset/WorkRequest and avoid creating duplicate Opportunities.
