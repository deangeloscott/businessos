# ViralTrac AURA — Agent Contract

AURA provides **durable organization-owned memory and reusable operating knowledge** to a capable model/harness. AURA is not the model, semantic intent engine, universal orchestrator, permission system, provider/tool selector, scheduler, or business decision-maker.

## Operating loop

For substantive organizational work:

1. **Identify exactly one organization.** Use stable `business_id` only after resolving which organization the user means. Never guess across organizations.
2. **Retrieve little.** Load only durable context/evidence/decisions/results/preferences/Learning that can materially improve the current job. Reuse current organizational knowledge before repeating questions or research.
3. **Choose the method with model judgment.** AURA may expose candidate playbooks, but candidates are retrieval hints rather than semantic authority. The model/user may select an AURA playbook, adapt useful knowledge, use an external Skill, create another method, or work ad hoc.
4. **Work normally.** Use the active harness's real tools, models, subagents, concurrency, permissions, retries, scheduling, and connected systems. AURA must not replace or downgrade capabilities the host already provides.
5. **Remember only what matters.** Persist durable organizational meaning when forgetting it would materially hurt future quality, truth, continuity, or efficiency. Do not save hidden reasoning, complete chats, routine tool calls, temporary calculations, retries, subagent chatter, caches, or transient host capability state.
6. **Preserve truth.** Keep explicit/verified business facts, external evidence, inference, candidate strategy, and unknown distinct. Unknown/not-found is not absent. Never fabricate business facts, claims, evidence, tool actions, permissions, or outcomes.
7. **Validate AURA-owned state.** Canonical state must be schema-valid, provenance/reference-aware, and isolated to the correct organization. Deterministic validation protects these mechanics; it should not replace model semantic judgment.
8. **Measure and learn when evidence supports it.** Preserve meaningful outcomes and promote reusable Learning only at the scope justified by evidence.

## Persistence test

Before saving anything, ask:

> Would a capable future model working for this organization materially benefit from knowing this after the current session/runtime is gone?

If no, do not persist it merely because a schema/helper exists.

A Run is an **optional bounded work receipt** for continuity/provenance. It is not required before reasoning begins and should not be required merely to remember durable truth. If a Run exists, record the method actually used: `aura_playbook`, `external_skill`, `model_created`, or `ad_hoc`.

## Operating knowledge

AURA playbooks/contracts describe reusable methods. They are not executable programs or authority over the active intelligence/runtime.

- Deterministic indexes may find bounded candidate playbooks.
- The model/user decides semantic applicability.
- Only claim AURA-playbook conformance when that playbook was actually selected and its essential evidence/quality invariants were satisfied.
- External Skill, model-created, and ad-hoc work remain legitimate and may produce the same useful organizational results without fabricated AURA contract provenance.

Installed modules are packages of AURA operating knowledge, not limits on what a capable model/harness may do. If a module is absent, its AURA playbooks are unavailable; that does **not** prohibit another sound method when the host has sufficient capabilities/evidence.

Provider-neutral capability IDs describe possible method needs only. The host owns live capability discovery, provider selection, permissions, fallbacks, and execution.

## Organization truth and isolation

Every canonical object belongs to one organization. Cross-organization canonical references are invalid unless an explicit product-level learning mechanism is designed for that purpose.

Use provenance appropriate to the meaning being saved. AURA should deterministically verify that referenced sources/objects exist and belong to the organization; the capable model determines semantic interpretation. Stronger literal support may still be required for outward claims or other cases where exact evidence is materially important.

Current context should represent the best supported organizational truth. When reality changes, update/retire incorrect current state and preserve historical change only when the history itself has future organizational value.

## External systems

Connected systems such as Gmail, CRM, accounting, analytics, banking, ViralTrac, or web tools remain owned by the active harness/runtime. Query the strongest appropriate source and persist only bounded durable meaning or authoritative pointers/results that future work benefits from. Do not bulk-copy operational histories into AURA merely because they are accessible.

A successful tool call is not automatically proof of a later business outcome.

## Real constraints

Respect the user's actual request and real legal, regulatory, contractual, platform, account, business, and organizational constraints. AURA does not manufacture generic risk tiers, autonomy ceilings, Approval objects, ActionPacket gates, or another permission ceremony.

A request to analyze does not silently become a request to publish. An explicit request to execute should not be blocked by invented AURA authority when the harness can perform it and no real constraint prevents it.

## Customer-facing work

Do not convert hypotheses, competitor patterns, placeholders, or inferred business details into established company claims. Load the specific claim/evidence policies when outward-facing work requires them. Artifact quality, deployment, and measured business outcome are separate facts.

## Product boundary

During ordinary organizational work, do not modify AURA product source to work around an execution problem. Product changes belong to explicit AURA development/repair work. Organization-specific context, preferences, Learning, and operating knowledge belong in organization state rather than product source.

## Practical entry

- `scripts/list_businesses.py --json` — list managed organizations by human-readable name and stable ID.
- `scripts/init_business.py <business-id> --name "<name>"` — establish the smallest truthful organization identity; no extra facts are required.
- `scripts/enter.py "<request>" --business-id <id>` — retrieve bounded baseline context and playbook candidates without semantic routing.
- Re-run `enter.py` with `--selected-contract <id>` only after the active model/user chooses an AURA playbook.
- Use supported persistence helpers for durable state and `scripts/validate_business.py <business-id>` after material changes.

The intended experience is:

**identify → retrieve little → work normally → remember what matters → measure/learn → continue**
