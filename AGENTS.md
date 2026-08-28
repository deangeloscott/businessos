# AURA Harness Entry Adapter

This file is a thin compatibility shim for agent harnesses that automatically read `AGENTS.md`. It does not define a second operating system or duplicate AURA policy. The authoritative entry contract is root `CONTEXT.md`.

Before performing ordinary business work in this repository:

1. Read and follow root `CONTEXT.md`, `INSTALLATION.json`, `core/policies/agent-execution.md`, and `core/policies/operating-scope.md` before the first business write or artifact build.
2. Resolve the active organization workspace and business. The AURA product root is read-only during normal business operation.
3. Route the user's natural-language request through AURA and create or resume the bounded root Run before invoking a host specialist Skill/plugin, renderer, generator, browser workflow, or other executor that will materially perform the business task.
4. Treat host Skills/plugins/tools as executors inside the AURA contract/Run lifecycle, not as alternate orchestration paths around it. They may improve how a step is executed but do not replace AURA routing, context, evidence, authorization, canonical state, required subcontracts, QA, completion, or Learning.
5. After Run creation, use `runtime/runs/<business-id>/<run-id>/work/` in the active workspace as the default scratch/build/cache/render location for that execution. Final governed business artifacts belong in the locations required by the resolved contract. Do not create hidden build directories, browser profiles, caches, generated media, helper scripts, or temporary outputs anywhere under the product root.
6. Finish through AURA's required completion-evidence and validation path before reporting the business task complete.

If any harness-specific instruction conflicts with AURA business governance, preserve AURA's business truth, scope, authorization, workspace, and completion boundaries while using the harness capability only as the executor for the allowed step.
