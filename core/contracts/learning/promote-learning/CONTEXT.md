---
id: core.learning.promote-learning
type: service
version: 1.1.0
owner_system: core
risk: low
autonomy_ceiling: 4
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
events:
  consumes:
  - none
  emits:
  - core.object.updated
---
# Promote Learning

## Purpose
Turn repeated or sufficiently strong outcome evidence into scoped future decision guidance.

## Business Outcome
Improve future decisions without converting anecdotes into universal best practices.

## Run When
When OutcomeEvaluations or repeated evidence suggest a tactic, threshold, preference, or mechanism is reusable.

## Do Not Run When
Do not promote mere observations, one-off stylistic edits, or weak correlations beyond their evidence-supported scope.

## Process
1. [AI] State the candidate Learning as a conditional proposition rather than a slogan.
2. [HYBRID] Determine the narrowest appropriate scope: domain, business, or system.
3. [HYBRID] Aggregate supporting/contradictory evidence and assess replication, causal confidence, and applicability.
4. [HYBRID] Set maturity/status and explicit applies_when/does_not_apply_when.
5. [DETERMINISTIC] For system learning, confirm evidence eligibility and isolation requirements.
6. [DETERMINISTIC] Persist Learning and emit learning.promoted/updated.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Required outputs exist and validate.
- Material uncertainty, contradictions, and unresolved dependencies are explicit.
- Any required next route is represented by a canonical reference or event rather than an informal note.
