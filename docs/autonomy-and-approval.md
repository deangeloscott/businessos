# Autonomy & Approval

Autonomy is per Action, not per agent or whole workflow.

- Tier 0: Observe.
- Tier 1: Recommend.
- Tier 2: Prepare executable work.
- Tier 3: Execute within bounded write authority/approval policy.
- Tier 4: Autonomous only inside explicit permissions and risk limits.

Effective authorization is the most restrictive combination of business policy, domain policy, Action risk, scale/blast radius, reversibility, confidence/evidence, compliance, capability permissions, approval requirements, rollback quality, **and the scope of the user's request**. Tool availability never implies authorization. A request to determine/recommend the next action does not automatically authorize performing it.

Silence, clarification timeout, tool/provider timeout, or absence of a response is never approval. Preserve the pending choice/blocker instead of converting timeout into permission.
