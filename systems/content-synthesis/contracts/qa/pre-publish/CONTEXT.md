---
id: content.qa.pre-publish
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
# Content Pre-Publish QA

## Purpose
Perform the final integrated check that the correct Asset is accurate, complete, native, accessible, and ready for the intended destination.

## Business Outcome
Prevent avoidable publication errors after strategy and production are complete.

## Run When
Run immediately before publication/scheduling or final delivery.

## Process
1. [DETERMINISTIC] Verify correct final version, destination, format, links, metadata, filenames, tracking, dates, and required approvals.
2. [HYBRID] Confirm Brand, editorial, fact/claim, platform-native, accessibility, and originality QA have passed where applicable. For customer-facing rendered media, inspect the actual final artifact—not only its source file, prompt, transcript, or metadata. Every material product behavior, integration, timing, outcome, proof, or performance statement must be supported by trusted business/evidence state or removed/narrowed; conceptual or illustrative workflow content must be visibly framed as such instead of implying the business/product performs it.
3. [HYBRID] For opaque/rendered media, verify `extensions.businessos.claim_surface_ref` resolves to the exact Asset and accurately inventories audience-visible text, spoken text, and material visual claims (or truthfully states why none exist). Compare the declared claim surface to the actual render; a safe sidecar paired with a contradictory image/video/audio file is a QA failure.
4. [AI] Check that hook/title/thumbnail/opening match the actual content and the desired action is clear/proportionate.
5. [DETERMINISTIC] Verify referenced proof/source assets are available and usage permissions remain valid.
6. [AI] Inspect for broken context introduced during editing/rendering: missing qualifier, wrong graphic, stale stat, truncated CTA, malformed pricing/terms, inaccessible text/contrast, or inconsistent version.
7. [DETERMINISTIC] Produce a publication checklist/pass record and block release on material unresolved failures.
8. [HYBRID] Route only high-risk/sensitive approval to human; do not add ceremonial approvals to low-risk routine content.
9. [DETERMINISTIC] Save the publication checklist/pass record as JSON under the active Run with `contract_id: "content.qa.pre-publish"`, `status: "pass"|"fail"`, checks performed, blockers, and tested Asset/version; record it with `scripts/record_contract_completion.py`. A final-answer statement that QA ran is not completion evidence by itself.
