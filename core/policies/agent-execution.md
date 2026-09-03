# Agent Work Policy

AURA supports organizational work with durable memory and reusable operating knowledge. It is not the active model, harness, semantic intent engine, permission system, scheduler, universal orchestrator, tool/provider registry, or business decision-maker.

## Core operating loop

1. **Preserve the request.** Keep the user's complete requested outcome and actual action boundary intact.
2. **Resolve the organization.** For organization-specific work, operate against exactly one active `business_id`.
3. **Retrieve little.** Reuse only current business facts, evidence, preferences/instructions, prior decisions, Assets/results, unresolved work, outcomes, and Learning that can materially improve the current job.
4. **Use operating knowledge when helpful.** AURA may surface a high-level Playbook and detailed Workflows. Candidates are navigation help, not semantic authority.
5. **Choose the best method with model/user judgment.** Use an AURA Playbook/Workflow, combine it with other Skills, use another Skill or method, or work ad hoc. Sequence or parallelize according to real dependencies.
6. **Use the host normally.** The active harness owns its actual tools, models, providers, connectors, APIs, browsers, files, subagents, concurrency, permissions, retries, rendering, scheduling, and execution.
7. **Do the real work.** Produce the useful business result the user requested. Do not substitute bookkeeping, setup, routing, or schema creation for substantive work.
8. **Persist only material organizational meaning.** Save durable facts/evidence, decisions, reusable instructions/preferences, useful Assets/results, real handoffs, unresolved work, outcomes, and evidence-supported Learning when future work will benefit.
9. **Validate what AURA owns.** Persisted state must be schema-valid, reference-valid, provenance-aware, epistemically honest, and isolated to the correct organization.
10. **Continue from memory.** Future models should be able to understand what materially happened without needing the original conversation, hidden reasoning, or runtime logs.

## Minimum sufficient guidance

AURA uses:

**Playbook → Workflow → Step**

- **Playbook** — a meaningful end-to-end business job.
- **Workflow** — a reusable procedure that helps accomplish part of a Playbook and may also be useful independently.
- **Step** — the minimum procedural guidance needed to make the Workflow reliably useful.

Specify a Step when it materially protects truth, evidence, scope, non-obvious expertise, quality, or repeatability. Do not prescribe incidental implementation details merely because they can be written down.

AURA should give capable intelligence the **fewest inputs necessary to repeatedly achieve the intended outcome at the required truth and quality standard**.

The model/harness may adapt implementation, use better tools/resources, combine Workflows, use other Skills, or choose another sound method when that better serves the outcome.

## Tools and Skills

AURA does **not** define a universal capability vocabulary, provider registry, or tool allowlist.

Describe what the work requires in natural language. The active model/harness determines how to accomplish it with the real resources available now.

Examples:

- “Research current competitor websites, relevant review sites, social/public conversations, advertising evidence, news, and other sources that materially answer the question.”
- “Inspect the actual final presentation for readability, factual fidelity, visual hierarchy, and accessibility.”

Those statements describe the work. They do not require functions with particular AURA-created names.

External/user-installed Skills are first-class options. AURA operating knowledge may complement them, be complemented by them, or be replaced by a better Skill/method for the task.

## Persistence boundary

Before writing durable AURA state, ask:

> Would a capable future model working for this organization materially benefit from knowing or reusing this after the current session is gone?

Persist when the answer is materially yes. Do **not** persist merely because a schema exists.

Do not store as organizational memory:

- hidden chain-of-thought or scratch reasoning;
- full chats/transcripts merely for completeness;
- routine tool calls, retries, temporary calculations, or subagent chatter;
- transient host/tool availability;
- arbitrary execution logs that carry no durable organizational meaning.

Use `scripts/remember.py` for ordinary durable canonical create/update operations. Use a specialized helper only where genuinely special evidence, identity, or state semantics warrant one.

Useful real deliverables should remain in an appropriate durable file/repository/system and be remembered as an `Asset` with the identity/reference/provenance/status future work actually needs. Do not automatically ingest every transient file.

## Method provenance and optional Runs

A Run/work receipt is useful only when bounded continuity or method provenance materially helps later work. It is not required before reasoning, persistence, Asset creation, publication, or validation.

When a receipt is useful, record the method truthfully:

- `aura_playbook`
- `aura_workflow`
- `external_skill`
- `model_created`
- `ad_hoc`

A Playbook/Workflow reference records what materially informed the work. It does **not** create an execution graph, conformance regime, permission state, special completion lifecycle, or stronger truth claim.

Canonical organizational facts/results stand independently. A receipt may point to them; they should not need Run backlinks merely to exist.

## Organization-specific reusable methods

A `ProcessExtension` is organization-owned reusable Workflow knowledge. It may augment an installed Workflow or define a local Workflow.

An explicitly supplied organization SOP may be saved directly as organization-authored Workflow knowledge without fabricating Learning first.

When evidence-supported Learning suggests a reusable procedure should change, the active model/user may create or update a ProcessExtension directly. Preserve relevant Learning/evidence references when they exist.

A ProcessExtension is not execution authority, provider configuration, or automatic self-modification.

## Truth and evidence

Follow `core/policies/active-business-truth.md`, `core/policies/evidence.md`, `core/policies/provenance.md`, and `core/policies/context-provenance-and-claims.md` where applicable.

Keep distinct:

- explicit user/first-party facts;
- verified first-party facts;
- external evidence;
- derived inference;
- candidate strategy/hypothesis;
- unknown.

**Unknown/not-found is not absent.**

Never invent prices, performance, service areas, offers, promises, metrics, audiences, outcomes, tool actions, permissions, or other business facts to make an artifact look complete.

The capable model interprets semantic meaning and evidence sufficiency. Deterministic AURA verifies structural/reference/provenance facts it can actually know. Strong literal support remains appropriate where exact wording materially matters, especially outward-facing claims.

For outward-facing work, do not turn hypotheses, competitor patterns, placeholders, or inferred details into established company claims. Artifact quality, production readiness, publication/deployment, and measured outcome are separate facts.

## Decisions and constraints

Respect actual constraints from the user, organization, law, regulation, contract, platform, account, or environment. Record a material organizational choice as `DecisionRecord` when future work benefits from knowing it.

AURA does not create generic `Approval` objects, autonomy ceilings, permission tiers, or `ActionPacket` authority gates. Absence of an AURA decision record does not itself forbid action.

The user's requested scope still matters. A request to analyze does not silently become a request to publish or mutate external state; an explicit request to execute should not be blocked by invented AURA ceremony when the harness can perform it and no real constraint prevents it.

## Handoffs, changes, verification, and attention

Create durable coordination/state only when it has future organizational value:

- `WorkRequest` for a real handoff worth remembering;
- `AttentionItem` for a material condition worth future awareness;
- `ChangeEvent` when remembering a material change will help later work;
- `VerificationRecord` when verification itself is materially useful.

Do not mirror every subagent call, tool invocation, deployment step, conceptual Workflow component, or runtime event into AURA canonical state.

Verification is not universal ceremony. Use it where the actual work or consequence warrants it.

## Monitoring

AURA may remember monitoring intent: what to watch, why it matters, materiality criteria, cadence intent, last meaningful state, notification intent, and findings.

The host/runtime owns actual schedules, polling, retries, wakeups, webhooks, event processing, notification delivery, and scheduler truth. Saving `next_check_at` or cadence intent does not prove automation exists.

## Product integrity

During ordinary organizational operation, do not modify AURA product source (`core/`, `systems/`, `scripts/`, schemas, tests, registries, manifests) to work around an execution problem. Product changes are appropriate only when the request itself concerns developing, repairing, configuring, migrating, or upgrading AURA.

## Completion

Judge the work by whether the requested useful result was actually produced at the appropriate quality and truth standard. Judge AURA-owned state separately by whether what was persisted is truthful, structurally sound, well-referenced, organization-isolated, and useful later.

If an optional Run exists, completing it means only that its material continuity receipt was closed. Do not equate Run completion with Playbook/Workflow certification, QA, deployment, customer-facing readiness, authorization, tool availability, business outcome, or causal proof.

The intended experience is:

**identify → retrieve little → work normally → remember what matters → measure/learn → continue**

not:

**request → bureaucracy → permission calculation → work**
