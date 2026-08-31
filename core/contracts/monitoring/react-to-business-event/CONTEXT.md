---
id: core.monitoring.react-to-business-event
type: playbook
version: 1.8.1
owner_system: core
reads:
- Business
- SourceRecord
- Observation
writes:
- Event
- EventReactionDecision
- SourceRecord
- Observation
- AttentionItem
capabilities:
  required:
  - none
  optional:
  - business.event.subscribe
  - business.event.trace.read
  - business.event.evaluate.preview
  - business.data.query
context:
- Business
---
# React to Governed Business Event

## Purpose
Turn an authorized business occurrence/event into a bounded BusinessOS evaluation trigger without treating event delivery as a command, action authorization, or proof of outcome.

## Business Outcome
Allow continuous/reactive operation when a trustworthy event surface exists while preserving the same domain routing, evidence, approval, verification, and portability rules used by scheduled/manual BusinessOS work.

## Run When
When an authorized provider/harness delivers or reliably surfaces a business occurrence that may materially change a current decision, opportunity, risk, run, monitoring state, or action eligibility.

## Process
1. [DETERMINISTIC] Load the business reactive-monitoring profile and validate event identity, active business scope, producer/source authority, event/schema version, occurrence timestamp, trace/root/parent identifiers, delivery/subscription reference, and provider operational mode. Reject/quarantine ambiguous cross-business or malformed events.
2. [DETERMINISTIC] Derive/reuse the event-reaction idempotency key from business, authoritative event identity, subscription/evaluation version, and owning reaction scope. Check prior EventReactionDecision/Run/Action evidence before doing work so redelivery or recovery replay cannot create a duplicate effect.
3. [DETERMINISTIC] Apply root/parent/depth/visited-action safeguards. Stop or coalesce echoes, cycles, repeated edges, excessive reaction depth, or a downstream consequence of the same BusinessOS action when it would simply repeat prior work; preserve provider loop/fuse reason codes when available.
4. [HYBRID] Treat the event only as evidence. Using the provider event-catalog semantics plus `core/monitoring/event-consumer-profile.json`, determine materiality for the active objectives/initiatives: evaluate now, coalesce, defer, ignore, block, or use fallback. Routine high-volume occurrences should normally feed aggregate/provider-native state rather than launch one AI run per event.
5. [DETERMINISTIC] Persist the bounded Event with authoritative event/trace/root/parent/subscription references and persist an EventReactionDecision for the disposition/materiality/routed contract. Where evidence must remain external, save a SourceRecord reference rather than copying sensitive/raw event payloads.
6. [AI] For a material `evaluate` disposition, route to the smallest installed BusinessOS contract capable of deciding what the occurrence means. Do not create a domain Insight/Opportunity in Core when another installed system owns that semantic meaning; if the owner is omitted, follow module-independence rather than impersonating it.
7. [HYBRID] If evaluation proposes a mutation, route through the ordinary ActionPacket, capability preflight, authorization/approval, execution, ChangeEvent, and VerificationRecord lifecycle. If material work cannot proceed because approval/input/credential/capability is missing, create/update one deduplicated AttentionItem; do not emit a fresh alert for every redelivery/poll. Provider `evaluate_shadow` never permits event-triggered external effects, and an event in any mode grants no execution authority by itself.
8. [DETERMINISTIC] Link resulting Run/Action/Change/Verification references back to the EventReactionDecision and preserve the originating provider trace/root chain so later OutcomeEvaluation can distinguish action, exposure, correlated outcome, and causal evidence.
9. [HYBRID] If delivery/result is surprising, degraded, receipt-incomplete, or apparently duplicated, route to `core.monitoring.diagnose-event-trace` before retrying. Do not blindly replay after a possible external mutation.
10. [HYBRID] When no trustworthy live event delivery exists, preserve equivalent monitoring intent through scheduler/polling/manual fallback and record the fallback disposition; create Attention only when the fallback itself requires material user action, not merely because live delivery is unavailable; BusinessOS continuous goals must remain functional without one provider's event plane.

## Verification
A material occurrence is business-scoped, idempotent, loop-safe, evidence-linked, correctly routed, and unable to bypass provider mode, BusinessOS authorization, or domain ownership; irrelevant/repeated events do not create unnecessary runs, and the same monitoring goal has an explicit fallback when event delivery is unavailable.
