# AURA Harness Entry Adapter

This file is a thin adapter for harnesses that automatically read `AGENTS.md`. Root `CONTEXT.md` defines AURA's operating philosophy. `AURA-ATTACHMENT.md` defines the same small attachment guidance for harnesses that should know AURA exists even when work starts outside this folder.

AURA provides organization-owned memory and reusable operating knowledge. It does not replace or constrain the active model/harness/user's intelligence, tools, semantic judgment, orchestration, delegation, concurrency, planning, permissions, scheduling, or execution.

For substantive work performed on behalf of an AURA-managed organization:

1. **Identify the organization.** `python3 scripts/list_businesses.py --json` exposes stable IDs and human-readable names without attempting semantic matching. If exactly one organization exists, AURA may resolve it automatically; if several are genuinely plausible, resolve from conversation context or ask rather than guessing.
2. **Initialize only what is known.** If the organization does not exist yet, `scripts/init_business.py <business-id> --name "<name>"` creates the smallest truthful canonical identity. Do not invent industry, service, market, objective, or other facts merely to complete setup.
3. **Retrieve little.** `python3 scripts/enter.py "<complete request>" --business-id <id>` is a bounded helper. Load only organizational memory and operating knowledge that can materially improve the current job. Equivalent direct retrieval is valid when the harness already has what it needs.
4. **Use operating knowledge when helpful.** AURA may surface a high-level Playbook and relevant Workflows. A Playbook is an end-to-end business job; a Workflow is a reusable procedure; a Step is the minimum guidance needed inside a Workflow. Candidates are navigation help, not semantic authority.
5. **Aim at the outcome, not AURA conformance.** Use the smallest useful set of AURA Workflows, combine them with other installed Skills, adapt them, replace them with a better sound method, or work ad hoc when appropriate. Sequence or parallelize work according to real dependencies.
6. **Use the host normally.** Use any appropriate tools, connectors, Skills, APIs, browsers, files, subagents, renderers, models, providers, retries, permissions, and scheduling mechanisms the harness actually exposes. AURA has no universal capability ontology or provider/tool allowlist.
7. **Remember durable value.** Persist only organization-owned meaning that a capable future model would materially benefit from. `python3 scripts/remember.py <business-id> --input <json>` is the generic Run-independent create/update path. Use specialized helpers only when their semantics genuinely matter. Do not fabricate a Run, Playbook, or Workflow provenance merely to make memory writable.
8. **Keep truth current.** Update established current truth when it changes, explicitly remove obsolete fields when appropriate, and use `scripts/forget.py` when an entire unreferenced object no longer deserves durable memory. Unknown/not-found is not absence.
9. **Preserve useful artifacts intentionally.** Keep the real artifact in a durable location and remember the useful `Asset` identity/reference/provenance/status when future work should reuse it. Do not ingest every temporary file.
10. **Use monitoring correctly.** AURA may remember what should be monitored, why, material signals, cadence intent, prior state, and findings. The host/OS/automation system owns actual wakeups, recurrence, retries, and notification delivery.
11. **Use Runs sparingly.** Create an optional bounded work receipt only when continuity or provenance materially benefits. A Run is not required before reasoning, persistence, Asset creation, publication, or validation.
12. **Validate AURA-owned state after material changes.** Organization isolation, provenance/reference integrity, schema validity, and structural workspace integrity are deterministic AURA responsibilities. Semantic strategy and evidence interpretation remain with the model/user.

Before saving anything, ask:

> Would a capable future model working for this organization materially benefit from knowing or reusing this after the current session is gone?

Remember established facts/evidence, durable decisions/preferences, useful findings, important Assets, unresolved work, measurements/outcomes, and evidence-supported Learning when they pass that test. Do not persist private reasoning, full chats, routine tool calls, retries, caches, or runtime chatter.

Unrelated personal/general work should continue through the host normally. During ordinary organizational work, do not modify AURA product source to work around an execution problem. Product-source changes are appropriate only when the request itself is to develop, repair, configure, migrate, or upgrade AURA.

The invariant is: **identify → retrieve little → work normally → remember what matters → measure/learn → continue.**
