# AURA Harness Entry Adapter

This file is a thin adapter for harnesses that automatically read `AGENTS.md`. Root `CONTEXT.md` defines AURA's operating philosophy.

AURA supports the active model/harness/user; it does not replace or constrain their intelligence, tools, orchestration, delegation, concurrency, planning, or judgment.

For work performed on behalf of an AURA-managed organization:

1. Resolve or initialize the organization when needed.
2. Use `python3 scripts/enter.py "<complete request>"` to retrieve bounded organizational context and an optional AURA playbook recommendation.
3. Treat the recommendation as operational knowledge, **not authority**. The model/harness/user may use it, adapt it, use an external Skill, create a better method, or work ad hoc.
4. Use the host's actual capabilities normally. AURA capability IDs describe what an AURA playbook may need; AURA does not inventory, bind, rank, install, or select providers/tools.
5. Create a Run/work receipt only when durable continuity or persistence is useful, and record the method actually used.
6. Persist only material organization-owned meaning that a capable future model would benefit from: evidence, facts/inferences with provenance, decisions, useful results/assets, unresolved work, outcomes, or Learning. Do not persist private reasoning, every tool call, caches, or runtime chatter.
7. If an AURA playbook was explicitly selected and completion of that playbook is claimed, satisfy its essential quality/evidence invariants. Other methods do not need to masquerade as AURA contracts.

Unrelated personal/general work should continue through the host normally. During ordinary business operation, do not modify AURA product source to work around an execution problem. Product-source changes are appropriate when the request itself is to develop, repair, configure, or upgrade AURA; see `core/policies/agent-execution.md` and `core/DEFAULTS.md` for that boundary.

The invariant is: **AURA provides organizational intelligence and operational knowledge; the active intelligence/runtime determines how best to work.**
