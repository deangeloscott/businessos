---
id: content.publishing.publish-asset
type: workflow
owner_system: content-synthesis
reads:
- Asset
writes:
- ChangeEvent
- VerificationRecord
- Asset
evidence_inputs:
- Business Constraints
---
# Publish or Schedule Content Asset

## Purpose
Publish or schedule the intended content Asset through the active harness when the user's requested action and real external constraints permit it.

## Business Outcome
Get the correct Asset/version onto the intended surface with the intended metadata, links, tracking, and timing without inserting an AURA approval or execution-control layer.

## Run When
When the user has asked for publishing/scheduling or that execution is otherwise clearly inside the current requested action scope, and the Asset is sufficiently ready for the intended destination.

## Do Not Run When
Do not turn a request to draft, review, analyze, or recommend into publication. Do not infer permission from an AURA status, WorkRequest, Run, Opportunity, or other internal object.

## Process
1. [HYBRID] Identify the exact Asset/version, destination, timing or scheduling intent, metadata/caption/title, links/CTA, tracking, and destination requirements that actually matter for this publication.
2. [AI] Confirm the execution remains inside the user's current request and any real organizational, legal, platform, account, contractual, or business constraints. AURA does not add a separate approval object or authority tier.
3. [INTEGRATION] Use the active harness's available destination capability to publish or schedule the Asset. If the needed capability is unavailable, use another valid host method when practical; otherwise explain the concrete unresolved capability/handoff need rather than creating a Manual Action Packet.
4. [HYBRID] Re-read or inspect the resulting published/scheduled state when practical and proportionate to the consequence.
5. [HYBRID] Check the exact Asset/version, formatting, links, media playback, visibility, metadata, and obvious rendering issues at the level the destination allows.
6. [DETERMINISTIC] Update the Asset with a durable publication reference/status when that information will matter later.
7. [HYBRID] Persist a ChangeEvent and/or VerificationRecord only when preserving the material external change or independent post-state evidence will genuinely improve future truth, troubleshooting, measurement, or continuity. Do not manufacture receipts for routine successful tool calls.

## Verification
- Any claim that publication/scheduling occurred is grounded in the host's actual returned/observed state.
- Draft/review scope never silently became publish scope.
- Scheduling state remains owned by the host/runtime; an AURA Asset field or timestamp is not proof that a future scheduler job exists.

## Failure / Fallback
- Preserve the concrete limitation and highest-fidelity useful next state when publication cannot be completed. Create a real durable handoff only when another person/system genuinely needs to continue the work.

## Completion Criteria
- The requested publication/scheduling work is either truthfully completed and inspectable, or the specific real boundary preventing completion is clear without invented approval, ActionPacket, or Manual Action Packet state.
