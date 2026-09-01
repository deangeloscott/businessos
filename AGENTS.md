# AURA Harness Entry Adapter

This file is a thin adapter for harnesses that automatically read `AGENTS.md`. Root `CONTEXT.md` defines AURA's operating philosophy. `AURA-ATTACHMENT.md` defines the same small contract for harnesses that should know AURA exists even when work starts outside this folder.

AURA provides organization-owned memory and reusable operating knowledge. It does not replace or constrain the active model/harness/user's intelligence, tools, semantic judgment, orchestration, delegation, concurrency, planning, permissions, scheduling, or execution.

For substantive work performed on behalf of an AURA-managed organization:

1. Identify the organization. `python3 scripts/list_businesses.py --json` exposes stable IDs and human-readable names without attempting semantic matching. If exactly one organization exists, AURA may resolve it automatically; if several are genuinely plausible, resolve from conversation context or ask the user rather than guessing.
2. If the organization does not exist yet, `scripts/init_business.py <business-id> --name "<name>"` creates the smallest truthful canonical identity. Do not invent industry, service, market, objective, or other facts merely to complete setup.
3. Retrieve only memory that can materially improve the current work. `python3 scripts/enter.py "<complete request>" --business-id <id>` is a bounded helper; equivalent direct retrieval is valid when the harness already has the needed context.
4. AURA operating knowledge is optional. The model/user may select an AURA playbook, adapt one within its real invariants, use an external Skill, create a better method, or work ad hoc. AURA does not semantically own the user's request.
5. Use the host's actual capabilities normally. AURA capability IDs describe possible playbook needs; AURA does not inventory, bind, rank, install, authorize, or select providers/tools.
6. Create a Run/work receipt only when durable continuity or provenance is useful. A Run is not required before reasoning begins or before durable memory can be saved.
7. Persist only material organization-owned meaning that a capable future model would benefit from. `python3 scripts/remember.py <business-id> --input <json>` is the generic Run-independent create/update path for canonical meaning; use specialized helpers when a type has real lifecycle/evidence semantics. Research evidence may use `persist_research_bundle.py` with truthful AURA-playbook, external-Skill, model-created, ad-hoc, or no method provenance. Do not fabricate a Run or contract merely to make memory writable.
8. If an AURA playbook was explicitly selected and completion of that playbook is claimed, satisfy its essential quality/evidence invariants. Other methods do not need to masquerade as AURA contracts.
9. Validate AURA-owned state when it is changed. Organization isolation, provenance/reference integrity, and schema validity are deterministic AURA responsibilities.

Remember evidence, current facts/inferences with provenance, durable decisions/instructions, useful results/assets, unresolved work, outcomes, or Learning when they pass the persistence test. Do not persist private reasoning, every tool call, caches, or runtime chatter.

Unrelated personal/general work should continue through the host normally. During ordinary organizational work, do not modify AURA product source to work around an execution problem. Product-source changes are appropriate when the request itself is to develop, repair, configure, or upgrade AURA.

The invariant is: **identify → retrieve little → work normally → remember what matters → continue.**
