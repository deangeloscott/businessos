---
id: core.monitoring.diagnose-event-trace
type: playbook
version: 1.8.1
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Business
- Event
- EventReactionDecision
- ChangeEvent
- VerificationRecord
- SourceRecord
writes:
- SourceRecord
- Observation
capabilities:
  required:
  - none
  optional:
  - business.event.trace.read
  - business.event.reconciliation.read
  - business.event.replay.preview
  - business.event.evaluate.preview
  - business.data.query
context:
- Business
---
# Diagnose Reactive Event Trace

## Purpose
Explain why an expected reactive BusinessOS path acted, declined, blocked, duplicated, degraded, or produced no outcome without guessing from event proximity.

## Business Outcome
Make continuous operation inspectable and repairable while preserving provider authority, BusinessOS lineage, and safe replay boundaries.

## Run When
When a BusinessOS event reaction is missing, ambiguous, repeated, blocked, degraded, apparently looped, or inconsistent with an expected provider/BusinessOS outcome.

## Process
1. [DETERMINISTIC] Resolve the authoritative event/trace reference, active business, root/parent occurrence, BusinessOS EventReactionDecision/run, and any linked ActionPacket/ChangeEvent/VerificationRecord; reject cross-business or unverifiable trace requests.
2. [INTEGRATION] Read the safest available provider trace and reconciliation state. Distinguish occurrence, normalization, identity/policy, delivery, evaluation, eligibility, action request/acceptance/completion, exposure, correlated outcome, and causal evidence instead of collapsing them into one success state.
3. [DETERMINISTIC] Compare provider root/parent/depth/idempotency identities with the BusinessOS event/reaction lineage. Detect duplicate delivery, replay, echo/cycle, missing receipt, stale policy, blocked identity/consent, unsupported capability, subscription drift, or delivery/fan-out degradation from explicit evidence/reason codes.
4. [HYBRID] Determine the smallest repair owner: ViralTrac/provider configuration, host delivery/harness, BusinessOS routing/materiality, installed-domain logic, target action capability, or no repair because the no-action result is correct.
5. [INTEGRATION] If replay/re-evaluation could help, request preview only and inspect affected subscriptions, prior effects, current policy, expected cost, and duplicate-effect protection. Never execute material replay merely because diagnosis suggests it.
6. [AI] Produce a bounded Observation explaining what is known, what failed or correctly declined, the evidence ceiling, the recommended repair/next process, and what must not be inferred.
7. [DETERMINISTIC] Persist SourceRecord references to the trace/reconciliation/replay preview plus the Observation; retain prior immutable event/action evidence and never rewrite it to make the path look successful.

## Verification
The diagnosis identifies the evidenced stage/reason for the reaction result, preserves occurrence/action/outcome distinctions, points to the correct repair owner, and does not cause replay or external effects without the ordinary governed authorization path.
