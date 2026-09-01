---
id: core.learning.promote-learning
type: service
owner_system: core
reads:
- OutcomeEvaluation
- Learning
- Insight
writes:
- Learning
capabilities:
  required:
  - none
  optional:
  - none
---
# Promote Learning

## Purpose
Turn repeated or sufficiently strong outcome evidence into scoped future decision guidance without turning Learning maturity into an automatic routing lifecycle or leaking one organization's private evidence into another.

## Business Outcome
Improve future decisions while keeping Learning evidence-backed, organization-owned, and no broader than the evidence supports.

## Run When
When OutcomeEvaluations or repeated evidence suggest a tactic, threshold, preference, or mechanism may be reusable beyond the immediate result inside the active organization.

## Do Not Run When
Do not promote mere observations, one-off stylistic edits, weak correlations, unsupported generalizations, or private evidence from another organization.

## Process
1. [AI] State the candidate Learning as a conditional proposition rather than a slogan.
2. [AI] Choose the narrowest useful organization-owned scope: `domain` when the guidance belongs to one specialized domain, or `business` when it genuinely applies across the active organization.
3. [HYBRID] Aggregate supporting and contradictory evidence from the active organization and assess replication, causal confidence, freshness, and applicability.
4. [AI] Choose maturity/status and explicit applies_when/does_not_apply_when from the evidence rather than from a fixed promotion pipeline.
5. [DETERMINISTIC] Persist and validate the Learning chosen by the model/user. Do not emit an AURA runtime event merely because maturity or interpretation changed.
6. [AI] If the Learning suggests a reusable organization-specific method, `core.learning.playbook-evolution` may encode it as a local process extension/playbook. If broader reuse outside this organization is desired, use an explicit sharing/adoption path such as the Innovation Exchange or deliberate AURA product-development work rather than creating cross-business Learning state.

## Verification
- The Learning belongs to the active organization and is scoped no broader than its supporting evidence.
- Supporting and contradictory evidence remain inspectable.
- Learning maturity does not create execution authority or mandatory next work.
- No other organization's private state is read or incorporated implicitly.

## Failure / Fallback
- If evidence remains insufficient or contradictory, keep the Learning at the narrowest justified maturity/scope or leave it unpromoted.
- If broader reuse seems valuable, preserve the organization-local evidence and use an explicit export/product-development path rather than weakening organization isolation.

## Completion Criteria
- Durable guidance exists only when it improves future work for the active organization, with applicability, uncertainty, and evidence clear enough for later models/humans to use responsibly.
