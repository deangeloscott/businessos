---
id: content.qa.pre-publish
type: workflow
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes: []
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
Use immediately before publication/scheduling or final delivery when an integrated final-artifact review is useful.

## Process
1. [DETERMINISTIC] Verify correct final version, destination, format, links, metadata, filenames, tracking, dates, and any real organizational/platform approvals that actually apply.
2. [HYBRID] Confirm Brand, editorial, fact/claim, platform-native, accessibility, and originality QA have been satisfied where applicable. For customer-facing rendered media, inspect the actual final artifact—not only its source file, prompt, transcript, or metadata. Every material product behavior, integration, timing, outcome, proof, or performance statement must be supported by trusted business/evidence state or removed/narrowed; conceptual or illustrative workflow content must be visibly framed as such instead of implying the business/product performs it.
3. [HYBRID] For opaque/rendered media, verify `extensions.businessos.claim_surface_ref` resolves to the exact Asset and accurately inventories audience-visible text, spoken text, and material visual claims (or truthfully states why none exist). Compare the declared claim surface to the actual render; a safe sidecar paired with a contradictory image/video/audio file is a QA failure.
4. [AI] Check that hook/title/thumbnail/opening match the actual content and the desired action is clear/proportionate.
5. [DETERMINISTIC] Verify referenced proof/source assets are available and usage permissions remain valid.
6. [AI] Inspect for broken context introduced during editing/rendering: missing qualifier, wrong graphic, stale stat, truncated CTA, malformed pricing/terms, inaccessible text/contrast, or inconsistent version.
7. [HYBRID] Return a clear pass/fail/readiness assessment for the inspected Asset/version, with material defects and the smallest corrections required. If material unresolved failures exist, recommend against publication until they are corrected; the user/host and real permissions own the publication decision.
8. [HYBRID] Seek a real human/organizational review only when the content or external policy actually requires it. Do not manufacture an AURA approval object or ceremonial approval step.
9. [HYBRID] Preserve the QA result in the Asset or a VerificationRecord only when future continuity, auditability, or downstream work materially benefits from remembering it. A Run/work receipt is optional and is not required for QA validity or publication readiness.
