# Deployment

AURA is local-first organizational memory and operating knowledge. It does not compile provider bindings, discover host tools, or maintain an execution-capability profile. AURA Workflows describe the work that needs to happen in ordinary language; the active model/harness decides which actual tools, Skills, providers, and execution methods are available and best suited to the outcome.

## Workspace location

AURA product source and organization-owned state may live together for the simple local experience or use the supported external workspace configuration. Durable organization state stays under the selected workspace; product upgrades should not require copying business state into AURA source.

When the active AI usually starts somewhere else, attach AURA once through the harness's normal persistent mechanism. Prefer the included `skills/viraltrac-aura/SKILL.md` when the harness supports portable Agent Skills; otherwise use the small persistent instruction in `AURA-ATTACHMENT.md` or an equivalent agent profile/workspace configuration.

Attachment creates **awareness**, not filesystem permission. The harness must still be able to access the AURA product/workspace through its normal file, mount, connector, MCP, or other supported mechanism. AURA should not scan the user's device broadly to discover itself.

## Session/operator labels

A host may set `BUSINESSOS_OPERATOR_REF`, `BUSINESSOS_TEAM_REF`, and `BUSINESSOS_ROLE_REF` per shell/session when scoped preferences or attribution benefit from them. These labels grant no authority and are not required for ordinary use. If a bounded Run/work receipt is intentionally created, it may record the applicable labels and preference snapshot.

Different harness windows may work against the same organization workspace. Coordinate simultaneous writes according to `core/policies/shared-workspace-coordination.md`; AURA does not need to orchestrate the models themselves.
