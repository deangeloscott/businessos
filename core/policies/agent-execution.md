# Agent Work Policy

AURA supports organizational work with durable memory and reusable operational knowledge. It is not the active model, harness, semantic intent engine, permission system, scheduler, universal orchestrator, or business decision-maker.

## Core operating loop

1. **Preserve the request.** Keep the user's complete requested outcome and actual action boundary intact.
2. **Resolve the organization.** For organization-specific work, operate against exactly one active `business_id`.
3. **Retrieve relevant durable context.** Reuse current business facts, evidence, preferences/instructions, prior decisions, assets/results, unresolved work, outcomes, and Learning before repeating questions or research.
4. **Choose the best method with model/user judgment.** AURA may surface bounded candidate playbooks or organization-local SOPs. Candidates are retrieval hints, not semantic authority. The model/user may select one, use an external Skill, create another method, or work ad hoc. Do not force work into an AURA contract merely to make it recordable.
5. **Use the host normally.** The active harness owns its actual tools, models, subagents, concurrency, permissions, retries, scheduling, and live capability discovery. AURA may describe provider-neutral capability needs for an AURA playbook but must not override live host truth.
6. **Do the real work.** Produce the useful business result the user requested. Do not substitute bookkeeping, setup, routing, or schema creation for the substantive work.
7. **Persist material organizational meaning.** Save only durable facts/evidence, meaningful decisions, reusable instructions/preferences, material assets/results, real handoffs, unresolved work, outcomes, and evidence-supported Learning that future organizational work would materially benefit from.
8. **Validate what AURA owns.** Persisted state must be schema-valid, reference-valid, provenance-aware, epistemically honest, and isolated to the correct organization. Apply relevant artifact/evidence/QA checks because they protect the actual work—not because a Run or contract ledger demands them.
9. **Continue from memory.** Future models should be able to understand what materially happened without needing the original conversation, hidden reasoning, or runtime logs.

## Persistence boundary

Before writing durable AURA state, ask:

> Would a capable future model working for this organization materially benefit from knowing this after the current session/runtime is gone?

Persist when the answer is materially yes. Do **not** persist merely because a schema exists.

Do not store as organizational memory:
- hidden chain-of-thought or scratch reasoning;
- full chats/transcripts merely for completeness;
- routine tool calls, retries, temporary calculations, or subagent chatter;
- transient host capability state;
- arbitrary execution logs that carry no durable organizational meaning.

Use `scripts/remember.py` for ordinary durable canonical create/update operations. Use a specialized helper only where that object has genuinely special evidence, identity, or state semantics, such as research evidence, preferences, attention, or platform-change history.

A bounded Run/work receipt is useful when continuity, method provenance, or later understanding benefits from one. It is not required before ordinary reasoning begins or merely to remember organizational meaning. Canonical results are persisted normally and stand on their own; if a receipt is useful, `scripts/complete_run.py` may reference those already-valid results without adding Run fields back onto them.

## Method provenance

A Run, when useful, identifies the method actually used:
- `aura_playbook`
- `external_skill`
- `model_created`
- `ad_hoc`

Every method uses the same optional receipt primitive. An AURA playbook ID records which reusable AURA method informed the work; it does **not** create a contract-execution manifest, subcontract ledger, permission state, execution hierarchy, or special completion regime. External Skill, model-created, and ad-hoc work may create the same legitimate organizational results without fabricated contract IDs.

Method provenance belongs in the optional receipt when preserving it materially improves continuity. Canonical organizational facts/results should not be coupled to a Run merely to record which runtime path produced them. Their own source/evidence/lineage semantics remain authoritative.

The model supplies substantive business meaning. Deterministic AURA helpers may supply mechanical IDs, timestamps, storage paths, local-reference resolution, schema checks, reference/isolation checks, and safe transactional writes.

## AURA playbooks

A contract ID identifies reusable AURA operating knowledge, not an executable program, internal service, or authority over the active model/runtime.

When AURA playbook knowledge is useful:
- load only the relevant playbook/context;
- apply the parts of its process, evidence discipline, and quality invariants that materially define the job;
- treat declared writes as **possible durable outputs**, not quotas or permissions;
- treat capability declarations as provider-neutral method needs;
- use relevant QA/evidence checks because the actual artifact or decision warrants them.

The model/user may adapt incidental implementation details or choose another sound method. Record method provenance honestly only when a receipt is worth preserving; do not create paperwork merely to prove that a playbook ran.

Organization-local `ProcessExtension` playbooks are the organization's own reusable operating knowledge. They are not preferences or notes, and they do not become AURA product-wide source. Explicitly supplied organization SOPs and evidence-supported Learning may both become ProcessExtensions with truthful provenance. AURA may surface them as candidates; the model/user decides semantic applicability.

## Truth and evidence

Follow `core/policies/active-business-truth.md`, `core/policies/evidence.md`, `core/policies/provenance.md`, and `core/policies/context-provenance-and-claims.md` where applicable.

Keep distinct:
- explicit user/first-party facts;
- verified first-party facts;
- external evidence;
- derived inference;
- candidate strategy/hypothesis;
- unknown.

Never invent prices, performance, service areas, offers, promises, metrics, audiences, outcomes, tool actions, permissions, or other business facts to make an artifact look complete. `not supplied` / `not found` is not proof of absence.

For ordinary organization context, deterministic AURA verifies provenance/reference integrity rather than trying to decide semantic equivalence with keyword or token rules. The capable model interprets meaning. Strong literal support remains appropriate where exact wording materially matters, especially outward-facing BusinessClaims.

For outward-facing work, do not turn hypotheses, competitor patterns, placeholders, or inferred details into established company claims. Artifact quality, production readiness, publication/deployment, and measured outcome are separate facts.

## Decisions and constraints

Respect actual constraints from the user, organization, law, regulation, contract, platform, account, or environment. Record a material organizational choice as `DecisionRecord` when future work benefits from knowing it.

AURA does not create generic `Approval` objects, autonomy ceilings, permission tiers, or `ActionPacket` authority gates. Absence of an AURA decision record does not itself forbid action.

The user's requested scope still matters. A request to analyze does not silently become a request to publish or mutate external state; an explicit request to execute should not be blocked by invented internal ceremony when the harness can perform it and no real constraint prevents it.

## Handoffs, changes, verification, and attention

Create durable coordination/state only when it has future organizational value:
- `WorkRequest` for a real handoff worth remembering;
- `AttentionItem` for a material condition worth future awareness;
- `ChangeEvent` when remembering a material change will help later work;
- `VerificationRecord` when verification itself is materially useful for the task, consequence, or future understanding.

Do not mirror every subagent call, tool invocation, deployment step, conceptual playbook component, or runtime event into AURA canonical state.

Verification is not a universal ceremony. Use it where the actual work or consequence warrants it.

## Monitoring and capabilities

AURA may remember monitoring intent: what to watch, why it matters, materiality criteria, cadence intent, last meaningful state, and findings. The host/runtime owns actual schedules, polling, retries, event processing, notification delivery, and scheduler truth.

Likewise, AURA playbooks may declare provider-neutral capabilities. The host/runtime resolves actual tools/providers and live availability. Environment caches/bindings are execution aids, not durable business truth and not universal AURA policy.

## Product integrity

During ordinary organizational operation, do not modify AURA product source (`core/`, `systems/`, `scripts/`, schemas, tests, registries, manifests) to work around an execution problem. Product changes are appropriate only when the request itself concerns developing, repairing, configuring, or upgrading AURA.

## Completion

Judge the work by whether the requested useful result was actually produced at the appropriate quality and truth standard. Judge AURA-owned state separately by whether what was persisted is truthful, structurally sound, well-referenced, and useful later.

If an optional Run exists, completing it means only that its material continuity receipt was closed. Do not equate Run completion with playbook certification, QA, deployment, customer-facing readiness, authorization, capability availability, business outcome, or causal proof.

The intended experience is:

**identify → retrieve little → work normally → remember what matters → continue**

not:

**request → bureaucracy → permission calculation → work**
