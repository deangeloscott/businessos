# Context Reuse and Question Minimization

AURA should not repeatedly ask for information the organization already owns. Reuse relevant durable context before interrupting the user while preserving business isolation, truth, and scope.

## Before asking a question

1. Inspect the active business's relevant canonical context, evidence, prior decisions/results, preferences/instructions, and current work continuity for an already-known answer.
2. Reuse a known answer when it is current, relevant, sufficiently authoritative, and actually applies to the present request.
3. Ask only when the unresolved information could materially change the requested result, factual correctness, external constraint, economics, Brand meaning, or output quality enough to justify interruption.
4. Do not ask merely because a new contract/module/session is running.

## Persist reusable answers

When the user supplies information likely to remain useful, persist it at the narrowest correct durable scope unless they say it is temporary/one-time or storage would be inappropriate.

- **Business context:** company/Brand facts, offers, audiences, markets, pricing, objectives, durable constraints, and other organization-owned facts.
- **Preferences/instructions:** reusable style/work-method choices belong in `PreferenceProfile` or another appropriate durable organizational record when clearly intended for reuse.
- **DecisionRecord:** use when a material organizational choice itself should be remembered, including who/what decided, when, scope, and basis.
- **Run/one-time context:** temporary answers and task-specific choices should remain work-local unless their future organizational value is clear.

When an answer changes an existing durable value, update/supersede the old value according to the owning object's truth/lifecycle policy rather than keeping contradictory active truths.

## Cross-business reuse

Remember aggressively; reuse conservatively.

- Never copy or infer Brand-specific facts, customer data, private operational state, or preferences from one business into another.
- Reuse across businesses only through an explicit broader-scope mechanism designed for it, such as eligible system-level Learning or canonical product operational knowledge.
- If scope is ambiguous, default durable business facts/preferences to the active business rather than creating a shared cross-business personal profile.

## Private/session context

The active model/harness may have its own session/private memory, credentials, contacts, or account state. AURA does not need to duplicate those merely to make them available during execution. Persist only organization-owned meaning that future organizational work materially needs.

## Privacy

Do not persist secrets, authentication tokens, payment credentials, or unnecessary sensitive personal data in AURA context. Keep external systems of record external when a durable reference or bounded evidence snapshot is sufficient.
