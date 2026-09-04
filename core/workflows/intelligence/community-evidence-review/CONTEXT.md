---
id: core.intelligence.community-evidence-review
type: workflow
owner_system: core
reads:
- SourceRecord
- Insight
- OutcomeEvaluation
- Learning
writes:
- Insight
---
# Community Innovation Evidence Review

## Purpose
Evaluate community-contributed process ideas and local replications as evidence rather than popularity, then determine what the evidence actually justifies.

## Business Outcome
Learn faster from community experimentation without creating an echo chamber, leaking private cross-business state, or turning community attention into automatic adoption/routing.

## Run When
Use when imported community evidence becomes decision-relevant, receives new local OutcomeEvaluation evidence, accumulates meaningful support/contradiction, or may justify changing organization-local operating knowledge or explicit AURA product-development work.

## Process
1. [HYBRID] Reuse the canonical SourceRecords and linked candidate Insight for the contribution plus relevant local OutcomeEvaluations, existing Learning, and overlapping evidence. Exchange/index entries may be consulted as noncanonical import support but are not organizational truth.
2. [AI] Separate reported community counts/repetition from independently inspectable evidence and from the active organization's own measured outcomes.
3. [HYBRID] Trace duplicate/reposted packages and do not count identical contribution material as independent replication. Exact package/hash deduplication may be deterministic; semantic equivalence remains model judgment.
4. [HYBRID] Draw on Core evidence-triangulation knowledge when it materially improves assessment of independent support/contradiction, methodology, applicability, novelty/repackaging, mechanism-specific freshness, or alternative explanations. Do not require a separate triangulation ceremony when the evidence is already sufficient for the actual decision.
5. [AI] Decide the narrowest justified disposition: ignore, remember, watch, investigate, test, preserve useful local operating knowledge, revise an existing Learning, or do nothing. This is a reasoning decision, not a Core routing lifecycle.
6. [AI] If evidence supports a reusable process improvement, `core.learning.workflow-evolution` may be relevant operating knowledge. The active model/user chooses whether preserving a ProcessExtension would actually help and at what scope; ordinary review does not mutate AURA product source.
7. [DETERMINISTIC] Persist only material Insight/evidence meaning selected by the model/user. Any later ProcessExtension is persisted through its own evidence-linked path. If the improvement belongs in canonical AURA, handle that as explicit product-development work rather than manufacturing an organizational proposal object.

## Verification
- Exchange popularity/repetition is never substituted for independent evidence.
- Material conclusions remain traceable through SourceRecord, Insight, OutcomeEvaluation, and Learning evidence where applicable.
- Private business state from another installation is never required.
- Contradictions and neutral outcomes remain visible when material.
- No WorkRequest, Opportunity, permission object, or next-route state is created merely because community evidence was reviewed.

## Completion Criteria
- The contribution has an evidence-grounded interpretation and, when useful, a clearly suggested next method without an automatic routing/adoption decision encoded by AURA.
