---
id: content.publishing.publish-asset
type: playbook
version: 1.2.0
owner_system: content-synthesis
reads:
- Asset
writes:
- ChangeEvent
- VerificationRecord
- Asset
capabilities:
  required:
  - none
  optional:
  - social.content.publish
  - cms.page.publish
  - email.content.publish
  - social.content.schedule
evidence_inputs:
- Business Constraints
---
# Publish or Schedule Content Asset

## Purpose
Publish or schedule an approved content Asset to the intended owned/distribution surface while preserving metadata, timing, tracking, and verification.

## Business Outcome
Deliver the approved Asset to the correct surface and time with the intended metadata/tracking, then independently verify the published or scheduled state.

## Run When
When an authorized WorkRequest/Action requires publishing and final content/brand/fact QA has passed.

## Process
1. [DETERMINISTIC] Confirm final approved Asset version, destination, timing/schedule, metadata/caption/title, links/CTA, tracking, and platform requirements.
2. [DETERMINISTIC] Resolve publishing capability and effective authorization; do not publish if approval/policy is incomplete.
3. [INTEGRATION] Publish/schedule via the available destination capability or create a Manual Action Packet.
4. [DETERMINISTIC] Record ChangeEvent with destination and returned publication identifier/URL.
5. [INTEGRATION] Independently re-read the published state when possible.
6. [HYBRID] Verify correct Asset/version, formatting, links, media playback, visibility, metadata, and obvious rendering issues.
7. [DETERMINISTIC] Save VerificationRecord and final publication reference on Asset.
