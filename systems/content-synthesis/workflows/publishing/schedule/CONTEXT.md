---
id: content.publishing.schedule
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
# Content Scheduling

## Purpose
Choose and create an appropriate publication time based on audience/platform needs, dependencies, and campaign/event constraints.

## Business Outcome
Publish content when it can serve the intended audience/objective without treating arbitrary “best times” as universal truth.

## Run When
Run when an approved Asset should be scheduled rather than published immediately.

## Process
1. [DETERMINISTIC] Resolve target platform/account, timezone/audience, campaign/event window, dependencies, embargoes, and existing schedule.
2. [AI] Use current platform/audience performance Learnings where available; otherwise choose a reasonable testable time rather than fabricate precision.
3. [AI] Avoid collisions/cannibalization where multiple Assets compete for the same audience/action unless intentional.
4. [DETERMINISTIC] Confirm Asset is final/approved and destination capabilities/permissions are available.
5. [INTEGRATION] Create the scheduled publication using the capability binding or Manual Action fallback.
6. [DETERMINISTIC] Record scheduled timestamp/destination and verify the schedule exists with the correct Asset/version.
7. [AI] Define post-publication measurement/checkpoint and rescheduling conditions if external events change.
