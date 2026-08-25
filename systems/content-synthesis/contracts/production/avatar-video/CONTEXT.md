---
id: content.production.avatar-video
type: playbook
version: 1.2.0
owner_system: content-synthesis
artifact_role: customer_facing_production_root
risk: medium
autonomy_ceiling: 3
reads:
- Insight
- Asset
- WorkRequest
- ProofRecord
- PlatformProfile
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.avatar_video.generate
  - creative.audio.generate
  - creative.video.generate
  - video.render
context:
- AudienceSegment
- Brand
---
# AI Avatar Video Production

## Purpose
Produce an approved avatar-presented video when synthetic presentation is appropriate, transparent, and efficient for the communication job.

## Business Outcome
Create scalable presenter-style video without lowering factual, brand, identity/consent, or audience-trust standards.

## Run When
Run when a Content WorkRequest explicitly permits synthetic/avatar presentation and a presenter-led format is useful for the target audience/platform.

## Process
1. [HYBRID] Confirm the business permits avatar/synthetic media for this use, the represented identity/voice has appropriate authorization, and any disclosure requirements are known.
2. [AI] Finalize the spoken script for natural delivery, pronunciation, pacing, emphasis, platform length, and visual cutaway needs; preserve proof/claim restrictions.
3. [DETERMINISTIC] Validate names, numbers, claims, links, pronunciation notes, disclosure language, and approved avatar/voice inputs before generation.
4. [INTEGRATION] Generate the avatar video with approved voice/avatar capability or create a manual/provider-neutral production package if unavailable.
5. [INTEGRATION] Add approved B-roll, screenshots, captions, graphics, proof visuals, music, or demonstrations only where they improve the message and rights permit.
6. [HYBRID] QA lip-sync/presentation quality, factual fidelity, disclosure, brand fit, uncanny/artifact risk, caption accuracy, and whether synthetic presentation harms trust for this context.
7. [DETERMINISTIC] Render/package the final Asset, preserve generation/source lineage, and record that the media is synthetic where policy requires.
