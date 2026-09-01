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
Prepare the platform-specific publication components needed to distribute an Asset cleanly across intended destinations.

## Business Outcome
Reduce repetitive packaging while preserving the native differences that materially improve each destination version.

## Run When
Use when one core Asset needs destination-specific derivatives, metadata, or publication preparation. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [DETERMINISTIC] Resolve the canonical Asset and intended destinations/PlatformProfiles; do not assume every platform needs a version.
2. [AI] Identify which destinations need a distinct derivative versus only metadata/caption/link packaging.
3. [AI] Prepare destination-specific caption/post text, title, description, tags/categories, thumbnail/cover, link/CTA, transcript/captions, and accessibility metadata as applicable.
4. [HYBRID] Verify each package preserves the source message and complies with destination, Brand, claim, accessibility, and real platform requirements that apply.
5. [DETERMINISTIC] Check file specs, URLs/tracking, account/destination, intended timing, and version lineage where those details are known.
6. [INTEGRATION] If the user requested publication/scheduling and the active harness has the real capability and permission, perform it through that host and preserve the returned external refs/status when useful. Otherwise preserve the ready distribution Assets and state plainly what remains unpublished/unscheduled. Create a WorkRequest only when a genuinely separate future executor needs a durable handoff; do not manufacture a manual-action packet or internal routing step.
7. [HYBRID] Preserve useful live/scheduled refs or publication state with the canonical Asset/derivatives when execution actually occurred. Link later MetricObservations when measurements are genuinely observed rather than pre-creating a lifecycle.
