---
id: content.production.bullet-script
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
# Bulletized Content Script

## Purpose
Convert an approved structure/full script into concise speaking beats for a presenter who should sound unscripted.

## Business Outcome
Preserve message, evidence, and sequence while giving the speaker flexibility in delivery.

## Run When
Run when a presenter prefers prompts/bullets rather than verbatim scripting.

## Process
1. [DETERMINISTIC] Resolve the approved full script or content outline and identify non-negotiable claims/evidence/CTA.
2. [AI] Reduce each beat to the minimum prompts needed to preserve sequence and intended point.
3. [AI] Keep exact wording only for facts, legal/claim-sensitive language, quotes, key definitions, or critical transitions.
4. [AI] Add brief cues for examples, demonstrations, visual changes, and audience interaction.
5. [HYBRID] Verify that removing verbatim language has not removed required qualifiers or made unsupported improvisation likely.
6. [AI] Add timing/priority markers and optional cut points if duration can vary.
7. [DETERMINISTIC] Produce a presenter-ready bullet script tied to source/visual refs.
