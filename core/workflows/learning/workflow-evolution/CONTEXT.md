---
id: core.learning.workflow-evolution
type: workflow
owner_system: core
reads:
- Learning
- OutcomeEvaluation
- Insight
- ProcessExtension
writes:
- ProcessExtension
---
# Workflow Evolution and Local Operating Knowledge

## Purpose
Turn sufficiently strong reusable Learning into the narrowest useful organization-owned operating knowledge without converting one successful result into universal AURA behavior.

## Business Outcome
Let future AI/humans benefit from what the organization has learned while keeping that knowledge optional, evidence-linked, portable, model/harness-neutral, and easy to revise.

## Run When
Use when evidence-supported Learning appears reusable and preserving a method would materially improve future organizational work.

## Do Not Run When
Do not formalize a method because a result is merely interesting, stylistically preferred, weakly correlated, or unsupported outside its observed scope. Do not create another process object when the existing Learning is already sufficient guidance.

## Process
1. [AI] Load the relevant Learning, material OutcomeEvaluations/Insights, contradictory evidence, and overlapping ProcessExtensions.
2. [AI] Decide whether reusable procedural knowledge would actually help future work. The valid result may simply be to keep the Learning as-is.
3. [AI] If useful, choose the narrowest organization-local form: augment an installed Workflow or create a local Workflow. State `applies_when`, `does_not_apply_when`, uncertainty/negative cases, useful instructions, and meaningful verification criteria without prescribing tools or orchestration unnecessarily.
4. [AI] Keep scope no broader than the evidence. Reads/writes describe organization-owned information the method may use or produce; they are not permissions, routing rules, or execution gates.
5. [DETERMINISTIC] Persist the local knowledge directly as a schema-valid `ProcessExtension` through `scripts/persist_process_extension.py` with `source_kind: learning_evolved`, the supporting `source_learning_refs`, and relevant evidence/provenance. No proposal/adoption lifecycle is required.
6. [HYBRID] If the improvement belongs in canonical AURA rather than organization-local knowledge, treat it as explicit AURA product-development work. Ordinary organizational work must not silently mutate canonical product source.
7. [AI] Future models may use, adapt, ignore, deactivate, or supersede the ProcessExtension according to the actual request, evidence, organization instructions, and better available methods. Stored local knowledge is context, not semantic authority.

## Verification
- The preserved knowledge materially improves future work beyond the existing Learning alone.
- Scope is no broader than the supporting evidence.
- Supporting and contradictory evidence remain traceable.
- Instructions preserve useful expertise without encoding provider/runtime state or unnecessary implementation detail.
- Reads/writes remain descriptive organizational semantics, not permissions or routing authority.
- No canonical AURA product file was silently mutated.

## Completion Criteria
Either the existing Learning remains sufficient, or a useful evidence-linked ProcessExtension exists as optional organization-owned operating knowledge. No intermediate proposal, approval, or adoption object is required.
