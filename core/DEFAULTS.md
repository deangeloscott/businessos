# Core Defaults

These defaults apply across AURA unless a more specific Workflow or explicit organization instruction materially changes the job. AURA is organization-owned memory and reusable operating knowledge, not the model, harness, permission system, scheduler, or execution-control plane.

## Operating loop
1. Resolve the active organization and the user's actual outcome.
2. Retrieve the smallest useful set of durable context, evidence, prior decisions, results, preferences, Assets, unresolved work, and Learning.
3. Surface a relevant Playbook and/or Workflow when that operating knowledge can help. The model/user decides what applies.
4. Let the active model/harness reason and execute using its best appropriate tools, other Skills, resources, and orchestration.
5. Persist only material organizational meaning future work should retain.
6. Validate persisted truth, provenance, references, schemas, and organization isolation.
7. Preserve measurements, outcomes, and reusable Learning when evidence supports them.

## Organizational memory
Persist information when forgetting it would materially hurt future organizational work. Favor durable facts, evidence, decisions, instructions/preferences, useful Assets/results, meaningful work receipts, unresolved work, outcomes, and evidence-supported Learning.

Do not persist hidden reasoning, full conversations, routine tool calls, temporary calculations, subagent chatter, retries, transient tool availability, or execution mechanics merely because they occurred.

Use `DecisionRecord` for a real durable decision. Use `WorkRequest` only for a real handoff worth remembering. Use `AttentionItem` only for a material condition worth future awareness. Use `ChangeEvent` or `VerificationRecord` only when the change or verification itself has future organizational value; ordinary execution or QA does not require a durable lifecycle record.

## Truth and evidence
- Keep observation, inference, hypothesis, candidate strategy, established fact, and unknown distinct.
- Never invent missing evidence, business facts, tool actions, permissions, outcomes, or measurements.
- **Unknown/not-found is not absent.**
- External patterns and benchmarks may inform hypotheses but do not become active-organization facts or forecasts without appropriate organization-specific evidence.
- Preserve source/provenance and current-versus-superseded state where it materially affects future work.
- Customer-facing claims must remain supported by established organization truth and applicable evidence.

## Operating knowledge
AURA uses **Playbook → Workflow → Step**.

- A Playbook is an end-to-end business job.
- A Workflow is a reusable procedure that helps accomplish a Playbook and may be useful independently.
- A Step is the minimum procedural guidance needed inside a Workflow.

Use the **fewest instructions necessary** to repeatedly achieve the intended outcome at the required truth and quality standard. Preserve non-obvious expertise, evidence requirements, real scope constraints, and meaningful quality conditions. Do not prescribe implementation detail merely because it can be written down.

AURA does not define a universal capability vocabulary or tool allowlist. Describe what the work requires in natural language. The active model/harness may use native tools, external Skills, APIs, connectors, browsers, local programs, subagents, or other sound methods.

When an AURA Workflow is actually used, satisfy the requirements that materially define the job; do not turn incidental implementation detail into conformance paperwork. Work done through an external Skill, model-created method, or ad-hoc method remains legitimate organizational work and may be remembered truthfully.

### Module independence
Installed modules are bodies of AURA operating knowledge, not limits on what capable intelligence may do.

- Only claim AURA operating knowledge that is actually installed.
- A missing module means its AURA guidance is unavailable. It does **not** prohibit another sound method.
- An uninstalled optional module is never a hidden hard dependency.
- Missing optional modules may change the available AURA guidance or evidence path; they must not silently lower the requested outcome or quality bar.
- Do not fabricate an uninstalled module as the owner, executor, or source of durable AURA state.
- If a module is installed later, reuse compatible existing organizational state rather than duplicating it.

## Execution boundary
- Use the active model/harness's real tools, models, other Skills, subagents, concurrency, retries, scheduling, permissions, and runtime state. AURA should not duplicate or override them.
- Stay within the user's actual request and real business, legal, platform, account, contractual, or organizational constraints. AURA does not manufacture authority gates.
- Tool availability is an execution fact, not durable organizational truth unless there is a material reason to remember it.
- Protect AURA product files during ordinary organizational work. Product changes belong to explicit AURA development/repair work.
- Use minimum sufficient work: deepen research or execution complexity only when it can materially improve the outcome, reduce important uncertainty, or satisfy a real requirement.

## Coordination and continuity
- Reuse current organizational context before asking repeat questions or repeating research.
- Preserve real handoffs and unresolved work when future continuation benefits.
- Do not create coordination objects merely because a model used a tool, provider, subagent, or another internal execution mechanism.
- Monitoring intent may be durable organizational state; scheduler bindings, polling loops, retries, and notification delivery belong to the host/runtime.

## Validation
Universal AURA integrity means persisted records are schema-valid, truthful, provenance-aware, reference-valid, and isolated to the correct organization. When a Workflow is actually used, its material method/evidence/quality requirements should be satisfied; this does not create a separate conformance lifecycle.

A successful tool response is not automatically proof of a later business outcome. Verify when the task or consequence warrants it, not as universal ceremony.

## Completion
A job is complete when the user's requested outcome has been addressed as far as the available evidence and real constraints allow, material results and unresolved work are represented truthfully, and persisted AURA state passes applicable integrity checks. Completion does not imply publication, deployment, external authorization, or measured business impact unless those facts are actually established.
