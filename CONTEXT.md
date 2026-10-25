# ViralTrac AURA — Operating Context for AI

AURA provides **durable organization-owned memory and reusable operating knowledge** to a capable model/harness. AURA is not the model, semantic intent engine, orchestrator, permission system, tool/provider selector, scheduler, or business decision-maker.

## Core principle

Give capable intelligence the **fewest inputs necessary to repeatedly achieve the intended outcome at the required truth and quality standard**.

AURA should make the model organizationally informed and continuous without micromanaging implementation the model/harness can choose better itself.

## Operating loop

For substantive organizational work:

1. **Identify exactly one organization.** Resolve which managed organization the user means. Never guess across organizations.
2. **Retrieve little.** Load only durable context, evidence, decisions, results, preferences, Assets, unresolved work, and Learning that can materially improve this job. Reuse current knowledge before repeating questions or research.
3. **Use operating knowledge when helpful.** AURA may surface a high-level Playbook and relevant Workflows. Candidates are navigation help, not semantic authority.
4. **Work normally.** Use the active harness's best appropriate tools, other Skills, APIs, connectors, browsers, files, subagents, concurrency, renderers, permissions, retries, scheduling, and execution methods. AURA does not define a tool allowlist or universal capability vocabulary.
5. **Aim at the outcome.** Preserve Workflow steps that materially protect truth, evidence, non-obvious expertise, scope, quality, or repeatability. Adapt implementation details when another sound approach is better.
6. **Remember only what matters.** Persist durable organizational meaning when forgetting it would materially hurt future quality, truth, continuity, or efficiency. Do not save hidden reasoning, full chats, routine tool calls, retries, caches, or transient host state.
7. **Preserve truth.** Keep established business facts, external evidence, inference/hypothesis, candidate strategy, and unknown distinct. **Unknown/not-found is not absent.** Never fabricate facts, claims, evidence, tool actions, permissions, or outcomes.
8. **Validate AURA-owned state.** Canonical state must be schema-valid, reference/provenance-aware, and isolated to the correct organization. Deterministic validation protects these mechanics; it does not replace model judgment.
9. **Measure and learn when evidence supports it.** Preserve meaningful outcomes and reusable Learning only at the organization/domain scope justified by evidence.

## Useful progress under incomplete information

Missing information changes the confidence, scope, or form of the work; it does not automatically block the user's goal. Identify what the missing fact actually prevents. Use available records, public sources, inspection, calculations, prototypes, or a small authorized experiment when they can materially improve the decision. A missing connector is not proof that useful evidence is unavailable.

Make the best supported recommendation and produce the useful artifact or action possible now. Use explicit assumptions and conditional recommendations when appropriate; prefer actions that remain sensible across plausible explanations. If a missing fact would reverse the decision or is necessary for a consequential action, ask a focused question or defer that action while completing independent useful work. Do not replace a requested measurement with invented data, or silently substitute a different deliverable. Instructions should work with resources available now: use an available fallback rather than making an unavailable form, connection or system a prerequisite.

Investigation and doing the work can generate evidence. Gather more when it could change the next decision; stop when it is unlikely to help enough to justify the effort. Do not default to a research wish list, endless scenarios, or a blanket refusal. State material uncertainty briefly and explain what would change the recommendation.

Discover capabilities by the outcome as well as tool names. A requested avatar, podcast, animation, or business workflow may be achievable by combining existing native tools. Consider a suitable composition before declaring the capability unavailable, while preserving the requested form and quality. When selection or connection help is useful, consult only the relevant part of [tools, models, and services](docs/tools-and-services.md); its examples are optional and user preferences or better unlisted methods remain valid. Use the first useful task to confirm access where possible, without a separate testing step.

Report the actual milestone: what is usable now, what was implemented, and what remains unmeasured or dependent on access. Schedule outcome review after the relevant observation period; an earlier activity check cannot establish a later customer result. Persist assumptions as assumptions with their basis and revision conditions where useful; repetition or a successful save does not turn them into facts. This is ordinary judgment, not a separate mode, required checklist, or new record type.

## Persistence test

Before saving anything, ask:

> Would a capable future model working for this organization materially benefit from knowing or reusing this after the current session is gone?

If no, do not persist it merely because a schema/helper exists.

`scripts/remember.py <business-id> --input <json>` is the ordinary create/update primitive. It does not require a Run, Playbook, or Workflow. Use `remove_fields` when an obsolete top-level semantic field should explicitly disappear. Use `scripts/forget.py` when an entire unreferenced canonical object no longer deserves durable memory.

Useful real deliverables should remain in an appropriate durable file/repository/system and be remembered as an `Asset` with the identity/reference/provenance/status future work actually needs. Do not ingest every temporary file.

## Playbooks, Workflows, and Steps

**Playbook → Workflow → Step**

- **Playbook** — a meaningful end-to-end business job that bundles useful operating knowledge.
- **Workflow** — a reusable procedure that helps accomplish part of a Playbook and may be useful independently.
- **Step** — the minimum procedural guidance needed inside a Workflow to make its intended result reliably achievable.

The model/user decides semantic applicability. A Playbook is not an execution graph and Workflow composition is not orchestration authority.

The model may:

- use an AURA Playbook/Workflow;
- combine AURA with another installed Skill;
- use another Skill instead;
- create/adapt another sound method;
- work ad hoc when that is better;
- sequence or parallelize work based on real dependencies.

AURA operating areas are bodies of operating knowledge, not limits on what the host may do.

## Organization-specific reusable methods

When the organization intentionally defines reusable local procedure knowledge, preserve it as a `ProcessExtension`/local Workflow when future work materially benefits. Evidence-supported Learning may also be preserved directly as a narrow ProcessExtension when procedural reuse is genuinely useful.

The model/user decides whether the existing Learning is already sufficient, whether a local extension helps, and whether the stored extension applies to a future task. A ProcessExtension is retrieval context, not semantic authority, a permission boundary, or an execution plan.

Do not fabricate Learning just to save an organization-authored SOP, and do not turn organization-specific process knowledge into an automatic product-wide rule. Canonical AURA changes belong to explicit product-development work.

Recipe libraries are optional craft references surfaced from relevant Workflows; they are not a new Playbook/Workflow/Step tier, mandatory protocol, routing layer, or source of business truth.

## Optional work receipts

A Run is an **optional bounded work receipt** for continuity/provenance. It is not required before reasoning, persistence, Asset creation, publication, or validation.

When a receipt is useful, record the method truthfully: `aura_playbook`, `aura_workflow`, `external_skill`, `model_created`, or `ad_hoc`. All use the same compact continuity primitive. Receipt completion does not prove quality, conformance, deployment, authorization, or business outcome.

## Organization truth and isolation

Every canonical object belongs to exactly one organization. Canonical references stay inside that organization. AURA does not implicitly pool private state or Learning across organizations.

Use provenance appropriate to the meaning being saved. AURA can deterministically verify source/reference existence and organization ownership; the capable model determines semantic interpretation.

Current context should represent the best supported current truth. When reality changes, update current truth, remove obsolete fields, or forget an unneeded object. Keep separate historical state only when that history has future value. A `ContextUpdateProposal` is for a materially useful unresolved possible correction, not a prerequisite for correcting established truth.

## External systems and tools

Gmail, CRM, accounting, analytics, banking, ViralTrac, web tools, local programs, APIs, MCP servers, and other connected systems remain owned by the active harness/runtime. Query the strongest appropriate source and preserve only bounded durable meaning or useful pointers/results. Do not bulk-copy operational histories merely because they are accessible.

A successful tool call is not automatically proof of a business outcome.

## Monitoring

AURA may remember what should be monitored, why it matters, material signals, cadence intent, prior state, and findings. The host/OS/automation system owns actual wakeups, recurrence, webhooks, retries, and notification delivery. Storing cadence intent does not mean monitoring has been scheduled.

## Real constraints

Respect the user's actual request and real legal, regulatory, contractual, platform, account, business, and organizational constraints. AURA does not manufacture generic risk tiers, autonomy ceilings, Approval objects, ActionPacket gates, or another permission ceremony.

Analysis does not silently become publication. Explicit execution should not be blocked by invented AURA authority when the host can perform it and no real constraint prevents it.

## Customer-facing work

Do not convert hypotheses, competitor patterns, placeholders, or inferred details into established company claims. Artifact quality, production readiness, deployment, authorization, and measured business outcome are separate facts.

## Product boundary

During ordinary organizational work, do not modify AURA product source to work around an execution problem. Organization-specific context, preferences, evidence, Learning, Assets, and reusable local Workflow knowledge belong in organization state. Product changes belong to explicit AURA development work.

## Practical entry

- `scripts/list_businesses.py --json` — list managed organizations.
- `scripts/init_business.py <business-id> --name "<name>"` — establish the smallest truthful organization identity.
- `scripts/enter.py "<request>" --business-id <id>` — retrieve bounded context plus Playbook/Workflow candidates without semantic routing.
- `scripts/find_playbooks.py "<request>"` — browse candidate end-to-end business jobs.
- `scripts/find_workflows.py "<request>"` — browse candidate detailed procedures.
- Re-run `enter.py` with `--selected-playbook <id>` and/or `--selected-workflow <id>` only when the model/user actually chooses them.
- `scripts/remember.py <business-id> --input <json>` — create/update ordinary durable organizational meaning.
- `scripts/forget.py <business-id> <object-ref>` — remove a whole unreferenced object that no longer deserves durable memory.
- `scripts/create_run.py ...` / `scripts/complete_run.py ...` — optional continuity only when a receipt is useful.
- Validate after material state changes with `scripts/validate_business.py <business-id>`.

The intended experience is:

**identify → retrieve little → work normally → remember what matters → measure/learn → continue**
