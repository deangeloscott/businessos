# AURA Harness Entry Adapter

This file is a thin compatibility shim for agent harnesses that automatically read `AGENTS.md`. It does not define a second operating system or duplicate AURA policy. The authoritative entry contract remains root `CONTEXT.md`.

AURA governs **organization/business work**, not the user's entire AI/harness experience. If the request is unrelated personal/general work, continue with the host normally. If the request explicitly concerns developing, repairing, testing, packaging, or upgrading the AURA product itself, follow the product-development scope in `core/policies/operating-scope.md` rather than entering an ordinary business Run.

When the request is being performed on behalf of an AURA-managed organization/business:

1. Before business research, artifact creation, canonical writes, or invoking a specialist Skill/plugin as the primary execution path, run `python3 scripts/enter.py "<the user's complete original request>"`. Add `--business-id <id>` only when the active business is already known and `--workspace <path>` only when the organization workspace is not already configured. Preserve the user's request verbatim/substantively complete.
2. Follow the returned AURA execution envelope. Read the returned context, use its resolved root contract/process, Run, capability state, authorization/truth boundaries, required subcontracts, and completion path.
3. Host specialist Skills/plugins/tools are **executors inside the AURA contract/Run lifecycle**, not alternate operating systems around it. They may determine how to perform an allowed step but do not replace AURA routing, context, evidence, authorization, canonical state, QA, completion, history, or Learning.
4. Use the returned Run `work_dir` as the default build/cache/render/browser-profile/temp location. The AURA product root is read-only during ordinary business operation. Final governed business artifacts belong in the active organization workspace at locations appropriate to the resolved contract.
5. Persist material organizational evidence, findings, decisions, governed Assets/state, completion evidence, and evidence-supported Learning at the narrowest justified scope. Do not turn every model thought, tool call, cache, failed render, or scratch artifact into permanent organizational knowledge.
6. Finish through AURA's required completion-evidence and validation path before reporting the organizational task complete.

The operating principle is: **AURA establishes the organizational job; the model/harness/Skills perform it. AURA does not take over unrelated harness use or dictate incidental execution technique.**
