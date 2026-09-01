---
id: core.intelligence.community-evidence-review
type: playbook
owner_system: core
reads:
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
Evaluate community-contributed process ideas and local replications as evidence, not popularity, then decide whether an innovation should be ignored, watched, investigated, tested, adopted locally, or proposed for broader playbook evolution.

## Business Outcome
Convert useful community experimentation into faster learning without creating an echo chamber or allowing private cross-business state to leak.

## Run When
Run when imported community evidence becomes decision-relevant, receives new local OutcomeEvaluation evidence, accumulates meaningful support or contradiction, or may justify adoption/evolution beyond simple discovery.

## Process
1. [DETERMINISTIC] Load the canonical SourceRecords and linked candidate Insight for the contribution plus relevant local OutcomeEvaluations, existing Learning, and overlapping evidence. Exchange/index entries may be consulted as noncanonical import support when available, but they are not organizational truth.
2. [AI] Separate reported community counts from independently inspectable evidence and from the active business's own measured outcomes.
3. [HYBRID] Trace duplicate/reposted packages and do not count identical contribution material as independent replication.
4. [AI] Apply Core triangulation: independent support/contradiction, methodology, applicability, novelty/repackaging, mechanism-specific freshness, and alternative explanations.
5. [HYBRID] Use Core route-learning to choose ignore/watch/investigate/test/adopt. Stronger evidence thresholds apply as cost, harm, or irreversibility rise.
6. [HYBRID] If local or independently corroborated evidence supports a durable reusable process, route to `core.learning.playbook-evolution` with the narrowest justified scope.
7. [HYBRID] If broader evidence might justify a canonical AURA improvement, create a `canonical_revision` proposal only; do not mutate the product automatically.

## Verification
- Exchange popularity/repetition is never substituted for independent evidence.
- Canonical conclusions remain traceable through SourceRecord, Insight, OutcomeEvaluation, and Learning objects.
- Private business state from another installation is never required.
- Contradictions and neutral outcomes remain visible.
- Any resulting process change has explicit applicability and can be revised or retired.

## Completion Criteria
- The innovation has an evidence-grounded disposition and, when justified, a Learning/evolution route rather than an unreviewed community recommendation.
