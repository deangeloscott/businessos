# AURA Workflow Authoring

An AURA **Workflow** is independently reusable procedural knowledge that helps a capable model or human accomplish a meaningful part of a business job. A Workflow may support one or more Playbooks and may also be useful on its own.

The goal is not to prescribe every move. Give capable intelligence the **fewest instructions necessary to repeatedly achieve the intended result at the required truth and quality standard**.

## Source of truth

Workflow frontmatter is lightweight machine-readable retrieval/context metadata. The body contains the actual operating knowledge. Generated indexes and navigation are derived; do not edit them manually.

Internal source paths and stable IDs may still use the historical word `contract` for compatibility. That is an implementation detail, not a model-facing concept and not execution authority.

## Required frontmatter

Use only:

- `id` — stable namespaced Workflow identifier;
- `type: workflow`;
- `owner_system` — the AURA operating area that maintains the knowledge;
- `reads` — durable organization object types/selectors that may help the Workflow;
- `writes` — durable outputs the Workflow may materially produce.

Add `context`, `workflows`, `evidence_inputs`, `artifact_role`, `completion_evidence`, or explicit references only when they add real value.

- `reads` and `writes` help retrieval/comprehension. They are not permissions, quotas, or a required object lifecycle.
- `workflows.required` / `workflows.conditional` identify other reusable Workflows that contain important supporting knowledge. They do **not** define execution order, service calls, handoffs, scheduling, or a required Run ledger.
- `completion_evidence` may describe useful structural evidence expectations for validation or qualification. It does not create a separate completion regime.

Do **not** add generic capability IDs, tool/provider bindings, `version`, `risk`, `autonomy_ceiling`, Approval, ActionPacket, scheduler, event, host-discovery, runtime-permission, or execution-status metadata to Workflows.

## Required body

- `# Name`
- `## Purpose` — the exact job this Workflow helps accomplish.
- `## Business Outcome` — why the job matters.
- `## Run When` — when this operating knowledge is useful.
- `## Process` — the minimum procedural guidance needed for reliable excellent work.

Optional sections such as `Do Not Run When`, `Decision Rules`, `Verification`, `Failure / Fallback`, `Completion Criteria`, and `References` should exist only when they materially improve the result.

## Steps: minimum sufficient guidance

A step should exist when omitting it would repeatedly reduce quality, truth, evidence discipline, continuity, or the likelihood of achieving the intended outcome.

Prefer outcome-oriented natural language. For example:

> Research the competitors customers actually consider, including meaningful substitutes, and verify that evidence belongs to the correct company before combining it.

Do not prescribe incidental mechanics such as exact clicks, tool names, pixel offsets, provider choices, or fixed sequencing unless that implementation is itself part of the requirement.

A Workflow may have many steps when the work genuinely requires them. Brevity is not the goal; **minimum sufficient guidance** is.

## Tool and Skill freedom

Describe the work that needs to happen in natural language. The active model/harness chooses the best available tools, APIs, browsers, files, renderers, external Skills, subagents, or other resources.

If the model discovers a better tool or method than the author anticipated, it should use it unless doing so would violate a real requirement. AURA Workflow metadata is not an allowlist.

If repeated real use reveals a missing non-obvious requirement, improve the Workflow itself rather than inventing another tool ontology.

## Inputs and outputs

Do not persist an object merely because it appears in `writes`. Persist it only when the work genuinely produced durable organizational meaning and future work benefits from keeping it.

Likewise, do not force a request through an AURA Workflow merely so the work can be recorded. A capable model may use a Playbook, one or more Workflows, an external Skill, a model-created method, or ad hoc reasoning as appropriate.

## Workflow composition

Use `workflows.required` only when supporting operating knowledge is normally essential to performing this Workflow well. Use `workflows.conditional` when it matters only under a stated condition.

Composition metadata means **knowledge composition**, not runtime orchestration. The model may sequence, parallelize, adapt, combine, partially use, or replace methods based on the actual job.

Do not split natural work merely to create departments, service boundaries, queues, or handoffs. Create another Workflow only when the procedure is independently reusable or materially distinct.

## Executor labels

Use `[AI]`, `[DETERMINISTIC]`, `[INTEGRATION]`, `[HUMAN]`, or `[HYBRID]` only when they materially clarify a step. They describe the nature of the work; they do not assign runtime authority.

## Keep runtime outside AURA

AURA may preserve an optional Run/work receipt when continuity is useful. A Workflow must not require a Run before work begins or use one as a permission token.

Tool selection, provider choice, credentials, availability, scheduling, retries, concurrency, subagents, publication execution, and other runtime mechanics belong to the active model/harness or the external system that actually provides them.
