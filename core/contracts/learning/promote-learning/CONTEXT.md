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
Turn repeated or sufficiently strong outcome evidence into scoped future decision guidance without turning Learning maturity into an automatic routing lifecycle.

## Business Outcome
Improve future decisions without converting anecdotes into universal best practices or silently changing reusable AURA product behavior.

## Run When
When OutcomeEvaluations or repeated evidence suggest a tactic, threshold, preference, or mechanism may be reusable beyond the immediate result.

## Do Not Run When
Do not promote mere observations, one-off stylistic edits, weak correlations, or unsupported generalizations beyond their evidence-supported scope.

## Process
1. [AI] State the candidate Learning as a conditional proposition rather than a slogan.
2. [HYBRID] Determine the narrowest justified scope: organization/domain or broader system-level reuse only when evidence supports it.
3. [HYBRID] Aggregate supporting and contradictory evidence and assess replication, causal confidence, freshness, and applicability.
4. [AI] Choose maturity/status and explicit applies_when/does_not_apply_when from the evidence rather than from a fixed promotion pipeline.
5. [DETERMINISTIC] For any broader-scope Learning, verify the actual evidence/reference/isolation requirements that make such reuse legitimate.
6. [DETERMINISTIC] Persist the Learning. Do not emit an AURA runtime event merely because its maturity or current interpretation changed.
7. [AI] If formal reusable operating knowledge would materially improve future work, `core.learning.playbook-evolution` is an available method the model/user may choose. Promotion does not automatically route there or edit product files.

## Verification
- The Learning is schema-valid and its scope is no broader than its supporting evidence.
- Supporting and contradictory evidence remain inspectable.
- Learning maturity does not create execution authority or mandatory next work.

## Failure / Fallback
- If evidence remains insufficient or contradictory, keep the Learning at the narrowest justified maturity/scope or leave it unpromoted.

## Completion Criteria
- Durable guidance exists only when it improves future work, with applicability, uncertainty, and evidence clear enough for later models/humans to use it responsibly.
