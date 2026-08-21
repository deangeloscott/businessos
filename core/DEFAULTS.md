# Core Defaults

These rules apply to every contract unless a stricter business, system, family, or contract rule applies. `core/policies/portable-first.md` is a hard architectural invariant; optional infrastructure may enhance execution but may not become mandatory Business OS infrastructure.

## Operating Loop
- Business outcome → evidence → Opportunity → Action → verification → measurement → Learning.
- Keep observation, inference, hypothesis, and validated Learning distinct.
- Derived objects reference upstream lineage instead of copying another system's canonical meaning.
- Every Opportunity has one semantic owner. Delegated execution does not create another Opportunity.

## Execution
- Use deterministic software for exact calculation, parsing, validation, comparison, state transition, scheduling, and other mechanical work.
- Use AI for ambiguity, interpretation, diagnosis, synthesis, planning, and creative reasoning.
- Tool availability is not permission. Apply business policy, action risk, reversibility, autonomy ceiling, and required approval before execution.
- Before executing an atomic job, preflight its required capabilities. Missing automation changes the executor, not the required business process. Create human-executable work when a required capability is unavailable, and preserve a blocker when no safe fallback exists.
- Preserve validated canonical business state and resumable run state according to `core/policies/local-state-and-recovery.md`; an agent restart is not a reason to discard valid work.

## External Research
- Public/third-party research may use browser/crawl/email tools only within legitimate access and a truthful authorized research identity. Never fabricate identity, company facts, purchase intent, or authority to obtain restricted information.
- Research source examples are non-exhaustive: use them to ensure coverage, not to prevent the agent from finding better sources.

## Evidence and Uncertainty
- Reuse current canonical intelligence before repeating research.
- Never invent missing evidence. When evidence is insufficient, stale, biased, or contradictory, preserve the uncertainty and create or maintain the knowledge gap.
- Use ranges when value, cost, impact, or causal effect cannot be estimated precisely.

## Verification
- Validate written objects, business isolation, references, schema, semantic ownership, and applicable lifecycle transitions before persistence.
- External state mutation requires a ChangeEvent plus independent VerificationRecord unless an explicit policy exception applies. A successful tool response is not independent verification.

## Completion
A job is complete only when required outputs validate, upstream lineage remains inspectable, unresolved uncertainty is explicit, and required cross-system next work is represented canonically through a WorkRequest, refresh request, object reference, event, or Incident.

## Context Integrity
- Canonical Business Context changes through controlled updates or proposals; downstream systems do not silently overwrite it.
- Cross-business references are prohibited by default.
