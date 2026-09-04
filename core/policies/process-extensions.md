# Process Extensions and Organization-Local Workflows

AURA may retain organization-scoped reusable operating knowledge without mutating the installed AURA product. A `ProcessExtension` is optional durable organizational memory, not a permission system, runtime wrapper, execution plan, or automatic self-modification mechanism.

## Purpose

Use a ProcessExtension when organization-authored procedure or evidence-supported Learning would materially improve future work. Do not create one merely to preserve one-off implementation detail, routine execution state, or a temporary draft.

A ProcessExtension can do one of two things:
- augment an installed AURA Workflow by using that Workflow's existing `workflow_id`;
- define an organization-local Workflow by using a `custom.*` `workflow_id`.

The identifier already tells AURA which relationship applies; no separate execution or compatibility mode is needed.

## Invariants

1. ProcessExtensions are operating knowledge. They do not own reasoning, tool/provider choice, orchestration, permissions, scheduling, concurrency, or runtime execution.
2. The active model/harness/user may use an extension, adapt it, combine it with another method, or choose a better method. AURA supplies relevant knowledge; it does not make that knowledge semantic authority.
3. Store only the procedure knowledge that helps future work: purpose, applicability, instructions, optional verification guidance, useful discovery terms, scope, and evidence/provenance.
4. Do not add capability declarations, provider bindings, reads/writes contracts, product-version compatibility, approval state, risk tiers, routing state, or other retired control-plane metadata.
5. Organization-authored procedure needs no fabricated Learning. When reusable knowledge genuinely evolved from Learning, preserve the relevant `source_learning_refs`; other supporting evidence may be preserved through source/evidence refs.
6. Scope is organizational relevance, not deterministic precedence. `business`, `team`, `role`, and `operator` scope may help retrieval; when several applicable extensions conflict, the active model/user resolves the conflict from actual context.
7. Deactivating or retiring an extension preserves useful history while removing it from normal active retrieval.
8. An imported or shared Workflow never becomes organization truth automatically. Adoption remains an explicit local decision and persistence act.
9. Product-level AURA Workflow changes remain explicit product-development work. A ProcessExtension does not mutate canonical product files.

## Applicability

Use `applies_when` and `does_not_apply_when` when they materially help future intelligence know when the procedure is useful. They are semantic context, not executable predicates or a routing engine.

Do not manufacture exhaustive conditions. The capable model may recognize relevant circumstances not literally enumerated in these fields.

## Verification guidance

`verification` is optional reusable guidance for checking work performed with the procedure. It is not a completion gate, conformance certificate, or mandatory receipt. Preserve it only when it makes future use meaningfully better.

## Resolution

`scripts/process_extensions.py` may list/filter applicable organization knowledge and provide bounded lexical discovery candidates. It may render an effective view of an installed or organization-local Workflow. Deterministic code does not decide semantic applicability, method quality, or whether the Workflow should be used.

## Sharing

The Innovation Exchange may package reusable Workflow knowledge only through an explicit sharing action with privacy/integrity boundaries. Imported packages remain support material until the receiving organization explicitly chooses to preserve them as local operating knowledge.
