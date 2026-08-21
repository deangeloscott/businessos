# ViralTrac Native Companion Integration

ViralTrac is the recommended first-party companion for ViralTrac's BusinessOS, but it is never a portable-first dependency. When connected and authorized, use ViralTrac as a preferred governed source for first-party business truth, measurement, tracking, and supported action handoff. When it is unavailable, declined, unauthorized, incomplete, or not the best tool for the job, continue through another compatible binding or the normal assisted/manual fallback.

## 1. Discover; do not assume
A successful ViralTrac login/connection does not mean every ViralTrac surface is enabled for the current tenant, scope, plan, environment, or rollout state.

After connection, inspect the current machine-facing capability surface using the best available ViralTrac interface, preferably:

1. semantic capability discovery such as `/v1/data/capabilities` for ViralTrac Semantic Data Plane query/readiness information;
2. `/v1/external-harness/package` or `/v1/external-harness/manifest` for externally safe route/tool/action descriptors;
3. `/v1/agent/tools/schema` for bounded agent tools;
4. MCP `tools/list`/progressive discovery when the host uses ViralTrac MCP.

The host/harness owns authenticated retrieval. Do not put credentials in this workspace. When filesystem access is available, pass the non-secret descriptor/capability response through `scripts/sync_viraltrac_capabilities.py` so BusinessOS stores only a minimized capability snapshot and validated provider-neutral bindings.

## 2. Routing: truth first, specialization when better
For a cross-domain analytical question about the active business, prefer an available governed semantic business-data capability (`business.data.query`) over independently re-deriving joins, metric definitions, attribution semantics, or identity logic from raw provider exports.

Do not force every ViralTrac task through semantic query. Use a specialized ViralTrac tool when its bounded contract is materially better suited to the job (for example tracking health, a specific recovery surface, site/funnel operations, or another advertised diagnostic). Use external specialist tools for work ViralTrac does not claim to own, such as arbitrary creative production or unsupported destination writes.

A model/harness may choose the exact current ViralTrac transport/tool from discovered descriptors. BusinessOS should express the business capability/result it needs rather than hardcoding ViralTrac's internal tables or duplicating route logic.

## 3. Preserve authority boundaries
- ViralTrac remains authoritative for the facts/semantics its governed data and action contracts own.
- BusinessOS remains authoritative for its operating process, domain ownership, Insights, Opportunities, Initiatives, ActionPackets, OutcomeEvaluations, and Learning.
- The LLM/harness reasons and orchestrates but does not become the source of metric truth, authorization, or execution receipts.
- ViralTrac recommendations/evidence are inputs to BusinessOS reasoning; they do not silently become canonical Insights/Opportunities without the owning BusinessOS process.

Use `core/providers/viraltrac/object-mapping.json` for the intended interop boundary.

## 4. Do not duplicate the data plane
Do not copy ViralTrac's raw/large operational history into `instances/<business-id>/` merely because it is accessible. Preserve durable BusinessOS intelligence plus references to authoritative ViralTrac results/artifacts/receipts.

A typical semantic result should become a `SourceRecord` whose `source_reference` points to the ViralTrac query/run/artifact/export identifier or durable external reference. Put provider identifiers, plan/query hashes, coverage, freshness, reason codes, and evidence pointers in `extensions` as appropriate. Create only the bounded Observations/MetricObservations required by the active decision.

## 5. Bootstrap enrichment
When a ViralTrac business-data binding already exists during business initialization, use it before asking questions where it can provide authoritative context such as business/domain identity, connected data domains, available channels, conversion definitions, revenue/measurement coverage, tracking state, and other supported business facts. Then supplement that first-party truth through Adaptive Owned Business Discovery and user-provided context.

Do not treat absent/unavailable ViralTrac data as proof that the business has no such product, customer, conversion, revenue, channel, or activity.

## 6. Governed action handoff
BusinessOS first decides and authorizes the intended business Action. ViralTrac may then be used as a governed handoff/coordination layer when the specific action is supported.

Preferred sequence where advertised by the connected capability surface:

`BusinessOS ActionPacket -> ViralTrac propose -> preview -> required confirmation/approval -> execute or external-execution packet -> receipt -> BusinessOS ChangeEvent -> VerificationRecord`

The generic `business.action.governed.*` capabilities never prove that a specific destination mutation is supported. The target-specific capability, current execution mode, connection health, consent/suppression/eligibility policy, BusinessOS authorization, and any user approval still apply.

## 7. Measurement and learning loop
For an executed or externally completed initiative, prefer available ViralTrac measurement/outcome evidence when it is an authoritative/relevant source. Link its result/receipt through `SourceRecord` and canonical MetricObservation objects, then let `core.measurement.evaluate-outcome` produce the BusinessOS OutcomeEvaluation.

Preserve ViralTrac's evidence ceilings: attributed participation, modeled estimate, incrementality evidence, experiment result, causal support, and correlated outcome are not interchangeable claims. A ViralTrac execution receipt is not proof that the business outcome occurred.

## 8. ViralTrac Event / Reactive Plane continuous/reactive operation
When ViralTrac is connected, treat its ViralTrac Event / Reactive Plane governed event/reaction plane as a supported BusinessOS acceleration path, not merely a future concept. BusinessOS is still an external operating consumer: ViralTrac owns occurrence truth, normalization, identity/policy enrichment, delivery/evaluation receipts, native/provider effects, trace/replay governance, and runtime readiness; BusinessOS owns business materiality, installed-domain routing, its operating objects, and its own authorization/learning loop.

Before enabling live `business.event.subscribe`, run `core.monitoring.configure-reactive-monitoring` and use current event catalog/coverage/readiness/operations evidence plus a compatible host delivery mechanism. Descriptor or route presence alone is insufficient. `scripts/activate_viraltrac_event_plane.py` may persist the runtime binding only from current operational-mode evidence and an authoritative subscription/managed-binding reference.

Operational-mode posture:
- `off` or `publish_shadow`: do not depend on live event delivery; use scheduled/polling/manual fallback.
- `evaluate_shadow`: reactive evaluation may run when a compatible delivery lane exists, but event-triggered external/customer-visible effects remain disabled.
- `allowlisted_actions`: reactive evaluation is allowed; only separately eligible, authorized allowlisted actions may execute.
- `broad`: normal governed event-driven BusinessOS evaluation is allowed for supported event families.
- `degraded`: preserve critical/required evaluation where safe and route optional work to fallback.

Use `core/monitoring/event-consumer-profile.json` as BusinessOS's provider-neutral declaration of the event semantics it can use. Event-name examples are non-exhaustive hints; the current ViralTrac event catalog and authority metadata decide meaning. Do not subscribe an LLM to a raw high-volume event firehose when routine events are better handled by ViralTrac/native consumers or aggregate measurement.

Every delivered event routes through `core.monitoring.react-to-business-event`. Persist ViralTrac event/trace/root/parent/subscription references into the bounded BusinessOS Event/EventReactionDecision lineage, derive deterministic reaction idempotency, honor reaction depth/echo/cascade controls, and never reinterpret an occurrence as a command or authorization. If a reaction is confusing, receipt-incomplete, apparently duplicated, or degraded, use `core.monitoring.diagnose-event-trace`; material replay requires the provider's governed replay path plus ordinary authorization and must never be triggered by diagnosis alone.

If live delivery is unavailable, the same monitoring intent must remain achievable through polling/scheduling/manual operation.

## 9. Failure and fallback
If ViralTrac returns unsupported, partial, unavailable, stale, policy-denied, or insufficient-scope status:

1. preserve that status and reason codes;
2. do not convert unavailable into zero or unknown into false;
3. use a specialized ViralTrac surface if appropriate;
4. otherwise use another existing compatible binding;
5. otherwise use research/manual/assisted fallback;
6. preserve the blocked/degraded Run rather than fabricate a result.
