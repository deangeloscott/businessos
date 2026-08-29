# Core Defaults

These rules apply to every contract unless a stricter business, system, family, or contract rule applies. `core/policies/portable-first.md` is a hard architectural invariant; optional infrastructure may enhance execution but may not become mandatory Business OS infrastructure.

## Operating Loop
- Business outcome → evidence → Opportunity → Action → verification → measurement → Learning.
- Keep observation, inference, hypothesis, and validated Learning distinct.
- Derived objects reference upstream lineage instead of copying another system's canonical meaning.
- Every Opportunity has one semantic owner. Delegated execution does not create another Opportunity.

## Execution
- Use deterministic software for exact calculation, parsing, validation, comparison, state transition, scheduling, and other mechanical work.
- Resolve durable customization through `core/policies/preferences-and-adaptation.md`: mandatory BusinessOS/business/Brand/contract/task requirements outrank preferences; preferences guide valid choices but do not authorize claims/actions.
- Prefer better/faster/easier implementation methods when they satisfy the same required outputs, evidence, authorization, capability, and validation boundaries; do not freeze incidental technique into BusinessOS.
- Shared-state use across sessions/workers follows `core/policies/shared-workspace-coordination.md`: sequential resume is supported, while arbitrary simultaneous writes to the same state are not assumed conflict-safe.
- Use AI for ambiguity, interpretation, diagnosis, synthesis, planning, and creative reasoning.
- Tool availability is not permission. Apply business policy, action risk, reversibility, autonomy ceiling, and required approval before execution.
- Before executing an atomic job, preflight its required capabilities. Missing automation changes the executor, not the required business process. Create human-executable work when a required capability is unavailable, and preserve a blocker when no safe fallback exists.
- Preserve validated canonical business state and resumable run state according to `core/policies/local-state-and-recovery.md`; an agent restart is not a reason to discard valid work.
- Use minimum sufficient work: conserve user waiting, tokens/context, tool/API spend, compute, agent cycles, and human attention while doing all work needed for a reliable outcome. Deepen or fan out only when it is likely to materially improve the decision, reduce important uncertainty, mitigate risk, or satisfy required verification.
- Do not invent implementation time, staffing, cost, or resource availability. When those are unknown, keep them unknown and do not overweight presumed manual-development effort where automation may execute the work.
- Truth rules apply to every artifact/answer that represents the active business, not only canonical state. Unknown/not-found is not the same as absent; external patterns and hypotheses must not become unsupported business claims.
- Stay within the user's requested scope. A request to analyze/diagnose/prioritize authorizes decision work, not implementation of the recommended intervention; silence or timeout never grants approval.
- Protect BusinessOS product files during normal business operation. Use supported helpers and business/runtime paths; do not patch `scripts/`, `core/`, `systems/`, `tests/`, schemas, or manifests to work around a failed operation. Product changes are appropriate only when the user's request itself concerns BusinessOS development/repair/configuration.

## External Research
- Public/third-party research may use browser/crawl/email tools only within legitimate access and a truthful authorized research identity. Never fabricate identity, company facts, purchase intent, or authority to obtain restricted information.
- Research source examples are non-exhaustive: use them to ensure coverage, not to prevent the agent from finding better sources.

## Shared Intelligence
- Follow `core/policies/intelligence-foundation.md` for multimodal evidence, subject/source tracking, contextual comparison, decision context, and human/machine legibility.
- Treat text, webpages, documents, images, audio, video, transcripts, comments, and structured records as evidence modalities. Use the best available provider-neutral method and preserve acquisition limitations.
- Reuse a resolved SourceProfile/subject watch instead of restarting from zero. Monitoring state belongs to the organization; no workflow may create a mandatory proprietary scheduler/daemon to make that state useful.
- Choose comparison cohorts for the decision. Geography, scale, audience/offer overlap, market position, business model, and channel/surface may make different peers relevant to different questions.
- Shared evidence mechanics do not transfer semantic ownership. Route customer, competitor, industry, search, content, persuasion, and journey interpretations to their existing owners.
- Canonical JSON remains machine-authoritative. Human summaries/views should be traceable derivatives and should not become competing canonical state.

## Evidence and Uncertainty
- Reuse current canonical intelligence before repeating research.
- Never invent missing evidence. When evidence is insufficient, stale, biased, or contradictory, preserve the uncertainty and create or maintain the knowledge gap.
- Use ranges when value, cost, impact, or causal effect cannot be estimated precisely. External benchmarks may support hypotheses or scenarios but do not become active-business forecasts without business-specific inputs.

## Verification
- Validate written objects, business isolation, references, schema, semantic ownership, and applicable lifecycle transitions before persistence.
- External state mutation requires a ChangeEvent plus independent VerificationRecord unless an explicit policy exception applies. A successful tool response is not independent verification.

## Completion
A job is complete only when required outputs validate, upstream lineage remains inspectable, unresolved uncertainty is explicit, and required cross-system next work is represented canonically through a WorkRequest, refresh request, object reference, event, or Incident.

## Context Integrity
- Canonical Business Context changes through controlled updates or proposals; downstream systems do not silently overwrite it.
- Cross-business references are prohibited by default.
