---
id: core.learning.playbook-evolution
type: playbook
version: 1.0.0
owner_system: core
reads:
- Learning
- OutcomeEvaluation
- Insight
- ProcessExtension
writes:
- PlaybookEvolutionProposal
capabilities:
  required:
  - none
  optional:
  - none
subcontracts:
  conditional:
  - id: core.learning.adopt-process-extension
    when: user explicitly approves a business-scoped extension/local playbook
events:
  consumes:
  - none
  emits:
  - core.object.created
---
# Playbook Evolution and System Improvement

## Purpose
Turn sufficiently strong reusable Learning into the narrowest justified operating-process improvement without converting one successful result into universal BusinessOS behavior.

## Business Outcome
Let every installed domain improve how the active business operates while keeping canonical BusinessOS portable, upgradeable, provider-neutral, evidence-governed, and reversible.

## Run When
Run when validated/emerging Learning appears reusable, the user asks to make a successful method part of BusinessOS, or community/external evidence suggests a process improvement worth formalizing.

## Do Not Run When
Do not rewrite BusinessOS because a result is merely interesting, stylistically preferred, weakly correlated, or unsupported outside its observed scope.

## Process
1. [AI] Load the candidate Learning, material OutcomeEvaluations/Insights, contradictory evidence, and any existing ProcessExtensions that overlap the same mechanism.
2. [HYBRID] Decide the narrowest justified level: keep as Learning/business rule, augment an existing contract, create a new local playbook, or create a domain/system `canonical_revision` proposal.
3. [AI] State the reusable mechanism conditionally, with explicit `applies_when`, `does_not_apply_when`, causal uncertainty, negative cases, and what would cause re-evaluation.
4. [HYBRID] For process change, define provider-neutral required/optional capabilities, declared reads/writes, operating instructions, verification, route terms when a new local playbook is needed, and rollback/deactivation behavior.
5. [HYBRID] Preserve canonical safety/approval/evidence/autonomy boundaries. An extension may add requirements but may not silently lower the base contract's controls.
6. [DETERMINISTIC] Persist a schema-valid PlaybookEvolutionProposal through `scripts/persist_playbook_evolution.py`; do not edit `core/` or `systems/` during ordinary business work.
7. [HUMAN] Require explicit user approval before business-scoped adoption. If approved, route to `core.learning.adopt-process-extension`.
8. [HYBRID] For `canonical_revision`, keep the proposal as a system-development candidate. Canonical product changes require an explicit BusinessOS-development request, repository change review, registry regeneration, and regression validation.

## Decisions / Routing
- Evidence not strong/reusable enough -> keep/narrow the Learning.
- Existing process should be adapted only for this business -> `augment_existing`.
- Reusable business workflow has no suitable base contract -> `new_local_playbook`.
- Evidence may justify changing standard BusinessOS guidance -> `canonical_revision`, then explicit product-development workflow.
- User approves business-scoped adoption -> `core.learning.adopt-process-extension`.

## Verification
- Proposal scope is no broader than its evidence.
- Supporting and contradictory evidence remain traceable.
- Capabilities are provider-neutral.
- No canonical BusinessOS product file was silently mutated.
- Adoption has an explicit rollback/deactivation path.

## Completion Criteria
- A validated PlaybookEvolutionProposal exists or the Learning remains intentionally unpromoted with an inspectable reason.
