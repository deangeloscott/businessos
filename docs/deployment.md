# Deployment

AURA is local-first organizational memory and operating knowledge. It does not compile provider bindings, discover host tools, or maintain an execution-capability profile. AURA playbooks may name provider-neutral capabilities that would help a method; the active model/harness decides which actual tools/providers are available and how to use them.

## Workspace location

AURA product source and organization-owned state may live together for the simple local experience or use the supported external workspace configuration. Durable organization state stays under the selected workspace; product upgrades should not require copying business state into AURA source.

When the active AI usually starts somewhere else, attach AURA once through the harness's normal persistent mechanism using `AURA-ATTACHMENT.md`. Attachment is a pointer/usage contract, not a background service or runtime.

## Session/operator labels

A host may set `BUSINESSOS_OPERATOR_REF`, `BUSINESSOS_TEAM_REF`, and `BUSINESSOS_ROLE_REF` per shell/session when scoped preferences or attribution benefit from them. These labels grant no authority and are not required for ordinary use. If a bounded Run/work receipt is intentionally created, it may record the applicable labels and preference snapshot.

Different harness windows may work against the same organization workspace. Coordinate simultaneous writes according to `core/policies/shared-workspace-coordination.md`; AURA does not need to orchestrate the models themselves.
