# AURA SOP / Contract Authoring

AURA contracts are independently routable units of reusable operational knowledge. Keep the business method complete enough to be useful while inheriting universal AURA truth, provenance, persistence, and business-isolation rules instead of repeating them.

## Source of truth

Frontmatter is machine-readable method metadata. The body contains job-specific operating logic. Generated registries are derived; never edit them manually.

## Required frontmatter

`id`, `type`, `version`, `owner_system`, `reads`, `writes`, and `capabilities`.

- `reads` and `writes` describe canonical organizational object types the SOP may use or materially produce.
- `capabilities` describe provider-neutral abilities the method needs or benefits from. They do **not** bind tools/providers or assert live availability.
- Add `context`, `subcontracts`, `evidence_inputs`, `artifact_role`, `completion_evidence`, or explicit references only when they add real method value.

Do **not** add generic `risk`, `autonomy_ceiling`, Approval, ActionPacket, provider-binding, scheduler, host-discovery, or runtime-permission metadata to new AURA contracts.

## Required body

- `# Name`
- `## Purpose` — exact job.
- `## Business Outcome` — why the job matters.
- `## Run When` — concrete trigger/condition.
- `## Process` — complete ordered SOP with meaningful executor labels when useful.

Optional sections such as `Do Not Run When`, `Decision Rules`, `Verification`, `Failure / Fallback`, `Completion Criteria`, and `References` should exist only when they add job-specific value.

## Inputs and outputs

`reads` and `writes` are possible durable organizational inputs/outputs, not write quotas. Do not persist an object merely because it is declared in metadata. Persist it only when the work genuinely produced that durable meaning.

## Executor labels

Use `[AI]`, `[DETERMINISTIC]`, `[INTEGRATION]`, `[HUMAN]`, or `[HYBRID]` when they clarify who/what performs a meaningful SOP step. They describe the method; they do not create AURA-owned runtime authority.

## Separate contract vs step

Create a contract when the work is independently routable/reusable, has materially different context/capability/output/quality behavior, or is shared by several parents. Keep small mechanical actions as steps or deterministic utilities.

## Specify invariants, not incidental implementation

Contracts should specify the business outcome, evidence discipline, important constraints, essential method/quality invariants, relevant outputs, and verification needed for reliable completion. Do not hardcode a vendor, renderer, model, exact creative structure, file-generation technique, or other incidental implementation detail unless it is genuinely part of the requirement.

The active model/harness may choose better implementation techniques while preserving the SOP's essential value.
