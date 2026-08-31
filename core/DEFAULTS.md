# Core Defaults

These defaults apply across AURA unless a selected SOP or explicit business instruction needs something more specific. AURA is organizational memory and operational knowledge, not the model, harness, permission system, scheduler, or execution-control plane.

## Operating Loop
1. Resolve the active organization and the user's actual outcome.
2. Retrieve the smallest relevant set of durable organizational context, evidence, prior decisions, results, and Learning.
3. Surface an AURA SOP when it is useful. The model/user may select it, adapt it within its essential invariants, or use another method.
4. Let the active model/harness reason and execute with the capabilities it actually has.
5. Persist only material organizational meaning that future work should retain.
6. Validate persisted truth, provenance, references, schema, and business isolation.
7. Measure outcomes and promote Learning when evidence supports it.

## Organizational Memory
Persist information when forgetting it would materially hurt future organizational work. Favor durable facts, evidence, decisions, instructions/preferences, assets/results, meaningful work receipts, unresolved work, outcomes, and evidence-supported Learning.

Do not persist hidden reasoning, full conversations, routine tool calls, transient calculations, subagent chatter, retries, temporary capability state, or execution mechanics merely because they occurred.

Use `DecisionRecord` for a real durable organizational decision. Use `WorkRequest` only for a real handoff worth remembering. Use `AttentionItem` only for a material condition worth future awareness. Use `ChangeEvent` or `VerificationRecord` only when the change or verification itself has future organizational value or the selected SOP requires it.

## Truth and Evidence
- Keep observation, inference, hypothesis, candidate strategy, established fact, and unknown distinct.
- Never invent missing evidence, business facts, tool actions, permissions, outcomes, or measurements.
- Unknown/not-found is not the same as absent.
- External patterns and benchmarks may inform hypotheses but do not become active-business facts or forecasts without appropriate business-specific evidence.
- Preserve source/provenance and current-versus-superseded state where it materially affects future work.
- Customer-facing claims must remain supported by established business truth and applicable evidence.

## Operational Knowledge
AURA SOPs describe reusable high-quality business methods. Provider-neutral capability declarations may describe what a method needs or benefits from; the current harness/runtime determines how those capabilities are actually satisfied.

If an AURA SOP is selected and its completion is claimed, satisfy its essential process, evidence, and QA requirements. Do not turn incidental implementation details into universal requirements. Work done through an external Skill, model-created method, or ad-hoc method remains legitimate organizational work and may still be remembered truthfully without fabricated contract execution.

## Execution Boundary
- Use the active model/harness's real tools, models, subagents, concurrency, retries, scheduling, permissions, and runtime state. AURA should not duplicate or override those mechanisms.
- Stay within the user's actual request and any real business, legal, platform, account, or organizational constraints. AURA does not manufacture additional authority gates.
- Tool availability is an execution fact, not durable organizational truth unless the organization has a material reason to remember it.
- Protect AURA product files during ordinary business work. Product changes belong to explicit AURA development/repair work, not business-operation fallbacks.
- Use minimum sufficient work: deepen research or orchestration only when it can materially improve the outcome, reduce important uncertainty, or satisfy a selected method's real requirements.

## Coordination and Continuity
- Reuse current organizational context before asking repeat questions or repeating research.
- Preserve real handoffs and unresolved work when future continuation benefits from them.
- Do not create coordination objects merely because a model used a tool, provider, subagent, or another internal execution mechanism.
- Monitoring intent may be durable organizational state; scheduler bindings, polling loops, retries, and notification delivery are runtime concerns.

## Validation
Universal AURA integrity means persisted records are schema-valid, truthful, provenance-aware, reference-valid, and isolated to the correct business. Selected-SOP conformance is additional and applies only when that SOP is actually used or claimed.

A successful tool response is not automatically proof of a later business outcome. Independent verification should be performed when the task/SOP or consequence warrants it, not as universal ceremony.

## Completion
A job is complete when the user's requested outcome has been addressed as far as the available evidence and real constraints allow, material results and unresolved work are represented truthfully, and any persisted AURA state passes applicable integrity checks. Completion does not imply deployment, authorization by an external party, or measured business impact unless those facts are actually established.
