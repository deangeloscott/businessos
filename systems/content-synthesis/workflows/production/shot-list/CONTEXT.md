---
id: content.production.shot-list
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
# Video Shot List

## Purpose
Convert the storyboard into an executable capture/generation list with coverage, continuity, and evidence requirements.

## Business Outcome
Ensure production captures everything required to edit the intended video without unnecessary footage or missing proof.

## Run When
Run before filming/generating a video with multiple shots or demonstrations.

## Process
1. [DETERMINISTIC] Resolve storyboard scenes, available Assets, presenter/location constraints, and production method.
2. [AI] List each required shot with subject, framing, action, duration/priority, audio needs, and linked script beat.
3. [AI] Add inserts, demonstrations, screen recordings, product/process views, reaction/context shots, and safety coverage only where useful.
4. [HYBRID] Identify shots requiring permission, sensitive data masking, brand/product accuracy, or proof authenticity.
5. [AI] Group shots into an efficient production order without changing final narrative order.
6. [DETERMINISTIC] Mark required versus optional coverage and technical specs for the target platform/render.
7. [AI] Produce a capture checklist suitable for human, generative, or hybrid production.
