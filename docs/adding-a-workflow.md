# Adding an AURA Workflow

Add a Workflow only when a reusable procedure materially improves future work enough to justify another thing to retrieve and maintain.

A Workflow is smaller than a Playbook. A **Playbook** represents a meaningful end-to-end business job; a **Workflow** is a reusable procedure that helps accomplish part of that job and may also be useful independently.

Create a separate Workflow when it has a genuinely distinct purpose, applicability boundary, evidence/context need, reusable method, or quality/verification knowledge. Keep trivial substeps inside the parent Workflow instead of multiplying files for structural symmetry.

Use a stable namespaced `id` because AURA needs an exact durable identifier for retrieval and references. Historical internal paths may still use the word `contract`; that is only storage compatibility and does not create execution authority.

## Write for a capable model or human

1. State the purpose and business outcome in ordinary language.
2. Explain when the Workflow is useful and important cases where it is not.
3. Give the minimum process knowledge needed to produce excellent work repeatedly.
4. Preserve uncertainty, evidence, and business truth honestly.
5. Define substantive verification/quality criteria only where they materially improve the result.

Prefer statements such as:

> Examine current competitor websites, public customer feedback, relevant advertising, social/public conversations, news, and other evidence that materially answers the competitive question.

rather than invented capability labels or instructions tied to one current tool.

The model/harness should choose the best tools, external Skills, APIs, browsers, subagents, files, renderers, and orchestration it actually has. If a better method exists, use it unless the Workflow expresses a real requirement that must be preserved.

## Frontmatter

Keep metadata small and descriptive:

- `reads` — durable organization object types/selectors that may help the procedure;
- `writes` — durable outputs the procedure may materially produce;
- `context` — especially relevant durable context types;
- `workflows` — supporting AURA Workflows that contain useful knowledge;
- `evidence_inputs` / `artifact_role` / `completion_evidence` — only when they add real value.

Do not add a generic capability catalog, provider/tool bindings, permission lists, capability preflight, semantic routing, execution graphs, lifecycle stages, Runs, WorkRequests, or handoffs merely because another Workflow once contained them.

## Composition

A Workflow may reference other Workflows as normally useful or conditional knowledge. This does not force execution order. The model may sequence them, parallelize independent work, use only the relevant portions, combine them with outside Skills, or choose another sound method.

## After authoring

Regenerate AURA's derived navigation and registries, validate the workspace, and run the relevant product-integrity and real-work qualification checks.

Tests should protect the useful business behavior or an AURA-owned invariant, not freeze wording, tool choices, or obsolete architecture.
