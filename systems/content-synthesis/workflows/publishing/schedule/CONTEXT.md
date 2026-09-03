---
id: content.publishing.schedule
type: workflow
owner_system: content-synthesis
reads:
- Insight
- Learning
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
# Content Scheduling

## Purpose
Choose a useful publication time and preserve the scheduling context while leaving timer, queue, API, account, and notification mechanics to the active host.

## Business Outcome
Publish content when it can best serve the intended audience and objective without treating arbitrary “best times” as universal truth or turning AURA into a scheduler.

## Run When
Use when publication should happen at a future time rather than immediately and scheduling is inside the user's requested action or another real execution scope.

## Process
1. [HYBRID] Resolve the exact Asset/version, destination/account, audience timezone, campaign or event window, embargoes, dependencies, existing schedule, and any real external constraints that can change timing.
2. [AI] Use current audience/platform performance evidence and relevant Learnings when they are strong enough to matter. Otherwise choose a reasonable, testable time and state the uncertainty rather than fabricate precision.
3. [AI] Avoid unnecessary collisions or cannibalization where several Assets compete for the same audience/action, unless concentration is intentional.
4. [HYBRID] Confirm the intended Asset/version is sufficiently ready for the destination and that scheduling remains inside the current request plus real organizational, legal, platform, account, contractual, or business constraints. AURA does not create an approval or permission layer.
5. [INTEGRATION] Ask the active harness to create the schedule using whatever real destination mechanism it has. If it cannot, explain the concrete limitation or preserve a genuine durable handoff only when another person/system needs to continue; do not manufacture a capability-binding or Manual Action fallback.
6. [HYBRID] Inspect the returned or observable scheduled state when practical. Preserve the destination, scheduled time, exact Asset/version, and durable publication reference on the Asset only when that information will help future work. An AURA timestamp is not proof that a future host scheduler job exists.
7. [AI] Define the useful post-publication measurement/checkpoint and the conditions that should trigger reconsideration or rescheduling if circumstances materially change.

## Verification
- Any claim that scheduling occurred is grounded in the host's returned or observed state.
- The exact Asset/version, destination, and scheduled time are unambiguous.
- AURA retains useful organizational continuity without owning the timer, queue, platform authorization, or scheduler.

## Completion Criteria
- The timing choice is evidence-informed or explicitly uncertain, and the requested scheduling work is either truthfully created by the host or the concrete real boundary preventing it is clear.
