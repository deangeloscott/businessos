# Context Reuse and Question Minimization

The BusinessOS should not repeatedly ask a user for information it already has. Reuse validated durable context before interrupting the user, while preserving business isolation and truthful scope.

## Before asking a question
1. Inspect the active business's canonical context, configuration, relevant prior validated outputs, and the current Run for an already-known answer.
2. When the question concerns external research identity, resolve the effective profile from the active business's `config/external-research-profile.json` plus `deployment/operator-profile.json` when inheritance is enabled.
3. Reuse a known answer when it is current, relevant, sufficiently authoritative, and permitted for the present action. Do not ask merely because a new contract or module is running.
4. Ask only when the unresolved information materially changes execution, authorization, compliance, economics, brand meaning, or output quality enough to justify interruption.

## Persist reusable answers
When the user supplies information that is likely to remain useful, persist it at the narrowest correct durable scope unless the user says it is temporary/one-time or storage would be inappropriate.

- **Business scope:** company/brand facts, organization identity, website, offers, audiences, pricing, constraints, brand preferences, business-specific research contact details, and other facts that must not silently cross `business_id` boundaries.
- **Operator/workspace scope:** the human/operator's reusable external-research identity may be stored in `deployment/operator-profile.json`. Only fields explicitly listed in `reuse_across_businesses` may be inherited by another business.
- **Run/one-time scope:** temporary answers, task-specific choices, and values the user says not to remember stay in the active Run and are not promoted automatically.

When an answer changes an existing durable value, update/supersede the old value according to the owning object's policy rather than keeping contradictory active truths.

## Cross-business reuse
Remember aggressively but reuse conservatively.

- Never copy or infer brand-specific facts from one business into another.
- `organization` and `website` are always business-scoped in the external research profile.
- Operator fields (`name`, `email`, `phone`, `location`) may cross businesses only when they are stored at operator scope and explicitly marked reusable.
- A business-level value overrides an inherited operator value for that business.
- If scope is ambiguous, persist to the active business rather than asking an extra meta-question solely about storage. Promote to operator scope later when the user clearly indicates the value is reusable across brands.
- Cross-business reuse of identity does not authorize actions, signups, purchases, submissions, or data sharing; normal approval and risk policies still apply.

## Privacy and portability
These profiles are local workspace state. Do not place secrets, credentials, payment data, authentication tokens, or unnecessary sensitive data in them. Distribution packaging must reset shared operator identity so one user's profile is never shipped to another.
