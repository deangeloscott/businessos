---
id: content.production.clip-extraction
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
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Long-Form Clip Extraction

## Purpose
Identify self-contained short clips from a longer Asset without distorting the original meaning.

## Business Outcome
Extend useful content into native short-form moments while preserving context and factual qualifiers.

## Run When
Use when a long video, podcast, webinar, or interview should produce shorter derivative Assets.

## Process
1. [AI] Review the source Asset for moments with a complete hook→idea/demo/story→payoff structure or a strong excerpt that can be contextualized.
2. [AI] Compare candidate clips by standalone value, audience relevance, evidence integrity, novelty, and target-platform fit—not only emotional intensity.
3. [HYBRID] Reject excerpts that become misleading when qualifiers, preceding context, or later correction are removed.
4. [AI] Define required cold open/context card, edit boundaries, caption/visual support, and native ending/CTA for each selected clip.
5. [DETERMINISTIC] Preserve source timestamps and lineage to the original Asset.
6. [AI] Adapt pacing/framing/text to the target PlatformProfile rather than merely cropping.
7. [DETERMINISTIC] Preserve useful derivative Assets and their relationship to the source idea. Create a WorkRequest only when an actual cross-person/model/session handoff must persist, not as a routine production stage.
