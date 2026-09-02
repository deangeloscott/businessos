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
- WorkflowEvolutionProposal
---
# Playbook Evolution and System Improvement

## Purpose
Turn sufficiently strong reusable Learning into the narrowest justified operating-knowledge improvement without converting one successful result into universal AURA behavior.

## Business Outcome
Let the organization improve how future AI/humans work while keeping AURA portable, model/harness-neutral, evidence-linked, and easy to revise.

## Run When
Use when evidence-supported Learning appears reusable, the user/model intentionally wants to preserve a successful method, or outside/community evidence suggests an improvement worth evaluating.

## Do Not Run When
Do not formalize a method because a result is merely interesting, stylistically preferred, weakly correlated, or unsupported outside its observed scope.

## Process
1. [AI] Load the candidate Learning, material OutcomeEvaluations/Insights, contradictory evidence, and overlapping ProcessExtensions.
2. [HYBRID] Choose the narrowest useful result: keep the existing Learning as sufficient guidance, augment an existing AURA playbook, create a local playbook, or create a domain/system `canonical_revision` candidate.
3. [AI] State the reusable mechanism conditionally with `applies_when`, `does_not_apply_when`, uncertainty, negative cases, and re-evaluation triggers.
4. [HYBRID] For a process change, keep only valuable operating knowledge: the tools or resources appropriate to the work, relevant reads/writes, instructions, quality/verification criteria, and useful discovery terms for a new local playbook.
5. [DETERMINISTIC] Persist a schema-valid WorkflowEvolutionProposal through `scripts/persist_workflow_evolution.py`; ordinary organization work does not edit AURA product source.
6. [HYBRID] If the organization intentionally chooses a business-scoped proposal, adopt it through `core.learning.adopt-process-extension`. The adoption action is the choice; no separate Approval/autonomy/risk/runtime gate exists.
7. [HYBRID] Keep `canonical_revision` proposals as product-development candidates. Canonical AURA changes require deliberate source changes plus registry/validation/quality work before release.

## Verification
- Proposal scope is no broader than its evidence.
- Supporting and contradictory evidence remain traceable.
- Capability needs are provider-neutral.
- The proposal does not encode host/provider/runtime state or generic authority semantics.
- No canonical AURA product file was silently mutated.

## Completion Criteria
A useful WorkflowEvolutionProposal exists, or the existing Learning remains the appropriate reusable guidance because formalizing another process artifact would not improve future organizational work.
