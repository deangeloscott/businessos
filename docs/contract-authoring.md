# AURA SOP / Contract Authoring

AURA contracts are independently reusable units of operational knowledge. Keep the business method complete enough to be useful while inheriting universal AURA truth, provenance, persistence, and organization-isolation rules instead of repeating them.

## Source of truth

Frontmatter is machine-readable method metadata. The body contains job-specific operating logic. Generated registries are derived; never edit them manually.

## Required frontmatter

`id`, `type`, `owner_system`, `reads`, `writes`, and `capabilities`.

- `reads` and `writes` describe canonical organizational object types the SOP may use or materially produce. They are retrieval/comprehension metadata, not runtime permissions or write quotas.
- `capabilities` describe provider-neutral abilities the method needs or benefits from. They do **not** bind tools/providers or assert live availability.
- Add `context`, `subcontracts`, `evidence_inputs`, `artifact_role`, `completion_evidence`, or explicit references only when they add real method value.
- `subcontracts` describe reusable supporting operating knowledge that may be composed into the method. They do not create an execution graph, required Run ledger, or internal service handoff.
- `completion_evidence` may describe useful structural evidence expectations for qualification or deterministic verification. It does not create a special Run completion regime.

Do **not** add generic `version`, `risk`, `autonomy_ceiling`, Approval, ActionPacket, provider-binding, scheduler, event, host-discovery, runtime-permission, or execution-status metadata to AURA contracts.

## Required body

- `# Name`
- `## Purpose` — exact job.
- `## Business Outcome` — why the job matters.
- `## Run When` — concrete trigger/condition.
- `## Process` — complete operating method with meaningful executor labels when useful.

Optional sections such as `Do Not Run When`, `Decision Rules`, `Verification`, `Failure / Fallback`, `Completion Criteria`, and `References` should exist only when they add job-specific value.

## Inputs and outputs

`reads` and `writes` are possible durable organizational inputs/outputs, not a lifecycle and not a permission model. Do not persist an object merely because it is declared in metadata. Persist it only when the work genuinely produced that durable meaning and future organizational work benefits from keeping it.

Likewise, do not force a request through an AURA contract merely so the work can be recorded. A capable model may use AURA operating knowledge, an external Skill, a model-created method, or ad-hoc reasoning as appropriate.

## Executor labels

Use `[AI]`, `[DETERMINISTIC]`, `[INTEGRATION]`, `[HUMAN]`, or `[HYBRID]` when they clarify who/what performs a meaningful SOP step. They describe the method; they do not create AURA-owned runtime authority.

## Separate contract vs step

Create a contract when the work is independently reusable, has materially different context/capability/output/quality behavior, or is shared by several methods. Keep small mechanical actions as steps or deterministic utilities.

Do not split a natural piece of work merely to create internal departments, service boundaries, queues, or handoffs. When several areas of AURA knowledge are useful to one task, the active model can compose them directly.

## Specify invariants, not incidental implementation

Contracts should specify the business outcome, evidence discipline, important constraints, essential method/quality invariants, relevant outputs, and verification needed for reliable work. Do not hardcode a vendor, renderer, model, exact creative structure, file-generation technique, or other incidental implementation detail unless it is genuinely part of the requirement.

The active model/harness may choose better implementation techniques while preserving the method's essential value.

## Keep runtime outside AURA

AURA may preserve a lightweight optional Run/work receipt when continuity is useful. A contract must not require creation of that receipt before work can begin or use the receipt as a permission token.

Tool selection, provider choice, credentials, live capability availability, scheduling, retries, concurrency, subagents, publication execution, and other host/runtime mechanics belong to the active model/harness or external system that actually provides them.
