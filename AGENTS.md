# AURA Harness Entry Adapter

For substantive work for an AURA-managed organization, read root `CONTEXT.md` once, unless its current contents are already in context. It is the shared operating guidance for every entry path. Use the user's selected workspace and business; unrelated work continues through the harness normally.

AURA adds organization-owned memory and reusable operating knowledge. The active model, user and harness retain semantic judgment, tools, native memory, delegation, permissions, scheduling and execution. User instructions take priority over contextual guidance.

Start with `scripts/list_businesses.py --json` when the organization is unclear. `scripts/enter.py "<request>" --business-id <id>` retrieves bounded context; direct retrieval is valid when you already have what you need. A simple conversation needs no helper calls. Use the available Python interpreter; do not assume `python3` exists on every OS.

For first-time setup or genuinely unknown readiness, use `scripts/setup.py --organization "<name>" --json` and `scripts/doctor.py --business-id <id> --json`. Before initializing an apparently empty download, inspect `scripts/workspace_catalog.py --current --json` or a user-selected `--path <folder> --json`. Native Skill attachment belongs to the host; the bundled Skill is `skills/viraltrac-aura/`.

During ordinary organizational work, do not modify AURA product source to solve an execution problem. Source changes belong to an explicit request to develop, repair, configure, migrate or upgrade AURA.
