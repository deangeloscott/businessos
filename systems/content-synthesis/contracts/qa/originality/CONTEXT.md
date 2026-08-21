---
id: content.qa.originality
type: playbook
version: 1.3.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 2
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- ActionPacket
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - creative.image.generate
  - creative.audio.generate
  - creative.video.generate
  - creative.animation.generate
  - creative.avatar_video.generate
  - video.render
  - presentation.render
  - document.render
  - social.content.publish
  - social.content.schedule
  - cms.page.publish
  - email.content.publish
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Originality QA

## Purpose
Ensure inspiration and pattern learning have not become copying of another creator’s distinctive expression.

## Business Outcome
Create original business content that can learn from mechanisms without plagiarism or confusing source ownership.

## Run When
Run when content was influenced by competitor/creator/trending material or uses substantial source examples.

## Process
1. [DETERMINISTIC] Resolve the inspiration/source Assets and the produced draft/final Asset.
2. [AI] Compare distinctive wording, sequence, examples, visual composition, jokes/metaphors, hooks, and expressive choices—not just topic overlap.
3. [AI] Identify which underlying mechanisms/structures are generic/transferable versus source-distinctive expression.
4. [HYBRID] Rewrite/redesign sections that are too close while preserving the intended mechanism and business-specific message.
5. [DETERMINISTIC] Verify quotations/media use, licenses, attribution, and source permissions where material is intentionally reused.
6. [AI] Confirm the final examples, voice, evidence, and point of view are grounded in this business/audience.
7. [DETERMINISTIC] Record QA result and source relationships where useful for provenance.
