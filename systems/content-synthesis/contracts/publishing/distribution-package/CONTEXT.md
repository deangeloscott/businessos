---
id: content.publishing.distribution-package
type: playbook
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
# Content Distribution Package

## Purpose
Prepare the platform-specific publication components needed to distribute an Asset cleanly across approved destinations.

## Business Outcome
Reduce repetitive manual packaging while preserving native differences between channels.

## Run When
Run when one core Asset has approved destination-specific derivatives or metadata ready for distribution.

## Process
1. [DETERMINISTIC] Resolve the canonical Asset and approved destination list/PlatformProfiles; do not assume every platform needs a version.
2. [AI] Identify which destinations need a distinct derivative versus only metadata/caption/link packaging.
3. [AI] Prepare destination-specific caption/post text, title, description, tags/categories, thumbnail/cover, link/CTA, transcript/captions, and accessibility metadata as applicable.
4. [HYBRID] Verify each package preserves the source message and complies with destination/brand/claim requirements.
5. [DETERMINISTIC] Check file specs, URLs/tracking, account/destination, schedule/publish status, and version lineage.
6. [INTEGRATION] Publish/schedule only where authorized; otherwise create precise Manual Action/WorkRequest.
7. [DETERMINISTIC] Return live/scheduled refs and link downstream MetricObservations to the canonical Asset/derivatives.
