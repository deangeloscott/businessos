# Adding an AURA Playbook

A playbook is reusable operating knowledge for a capable model or human. Add one only when the authored method materially improves future work enough to justify another thing to retrieve and maintain.

Create a separate playbook when it has a genuinely distinct purpose, applicability boundary, evidence/context need, reusable method, or quality/verification knowledge. Keep trivial substeps inside the parent method or ordinary prose instead of multiplying playbooks for structural symmetry.

Use a stable namespaced `id` because AURA needs an exact durable identifier for retrieval and references. The internal file is still called a contract, but that identifier is **not** execution authority.

Frontmatter should remain descriptive:
- `reads` — durable object types/selectors that may be useful to the method;
- `writes` — durable outputs the method may produce when they are actually worth remembering;
- `capabilities` — provider-neutral abilities the method may need or benefit from;
- `context` — durable context types that are especially relevant;
- `subcontracts` — supporting AURA playbooks that can deepen this method when useful.

None of those fields is a permission list, capability preflight, semantic router, execution graph, or requirement to manufacture objects that are not genuinely useful.

Write the body for an intelligent operator:
1. State the purpose and business outcome.
2. Explain when the method is useful and important cases where it is not.
3. Give the minimum process knowledge needed to produce excellent work. Distinguish essential quality/evidence invariants from incidental implementation details the model may adapt.
4. Preserve uncertainty, evidence, and business truth honestly.
5. Define substantive verification/quality criteria where they materially improve the result.

Do not add risk tiers, autonomy ceilings, approvals, generic fallbacks, routing decisions, scheduler behavior, provider selection, lifecycle stages, Runs, WorkRequests, or handoffs merely because an older playbook used them. Add a durable object or supporting method only when its organizational meaning is independently real.

After authoring, run `python3 scripts/generate_registry.py` and the relevant product-integrity and real-work qualification checks. Tests should protect the useful business behavior or AURA-owned invariant, not freeze wording or obsolete architecture.
