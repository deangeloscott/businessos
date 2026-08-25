---
id: core.intelligence.community-evidence-review
type: playbook
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- InnovationExchangeEntry
- SourceRecord
- Insight
- OutcomeEvaluation
- Learning
writes:
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - research.web.read
subcontracts:
  required:
  - id: core.intelligence.ecosystem.evidence-triangulation
  - id: core.intelligence.ecosystem.route-learning
  conditional:
  - id: core.learning.playbook-evolution
    when: evidence supports a reusable process improvement
---
# Community Innovation Evidence Review

## Purpose
Evaluate accumulated BusinessOS community contributions and local replications as evidence, not popularity, then decide whether an innovation should be ignored, watched, investigated, tested, adopted locally, or proposed for broader playbook evolution.

## Business Outcome
Convert useful community experimentation into safer faster learning without creating an echo chamber or allowing private cross-business state to leak.

## Process
1. [DETERMINISTIC] Load the InnovationExchangeEntry, its package/source records, linked candidate Insight, local OutcomeEvaluations, existing Learning, and overlapping innovations.
2. [AI] Separate reported community counts from independently inspectable evidence and from the active business's own measured outcomes.
3. [HYBRID] Trace duplicate/reposted packages and do not count identical contribution material as independent replication.
4. [AI] Apply Core triangulation: independent support/contradiction, methodology, applicability, novelty/repackaging, mechanism-specific freshness, and alternative explanations.
5. [HYBRID] Use Core route-learning to choose ignore/watch/investigate/test/adopt. Stronger evidence thresholds apply as cost, harm, or irreversibility rise.
6. [HYBRID] If local or independently corroborated evidence supports a durable reusable process, route to `core.learning.playbook-evolution` with the narrowest justified scope.
7. [HYBRID] If broader evidence might justify a canonical BusinessOS improvement, create a `canonical_revision` proposal only; do not mutate the product automatically.

## Verification
- Exchange popularity/repetition is never substituted for independent evidence.
- Private business state from another installation is never required.
- Contradictions and neutral outcomes remain visible.
- Any resulting process change has explicit applicability and rollback.

## Completion Criteria
- The innovation has an evidence-grounded disposition and, when justified, a Learning/evolution route rather than an unreviewed community recommendation.
