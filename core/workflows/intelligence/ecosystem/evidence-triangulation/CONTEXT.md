---
id: core.intelligence.ecosystem.evidence-triangulation
type: workflow
owner_system: core
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- OutcomeEvaluation
- Experiment
writes:
- Observation
- Insight
---
# External Evidence Triangulation

## Purpose
Determine what a material external claim or signal is actually supported by after tracing provenance, independent corroboration, contradiction, freshness, novelty, methodology, and alternative explanations.

## Business Outcome
Reduce false confidence from viral repetition, stale evidence, selective success stories, and duplicated reporting before BusinessOS spends money or changes operations.

## Run When
Run when a discovered claim/event is material enough to influence a business decision, an existing Insight receives meaningful new evidence, or evidence appears contradictory.

## Process
1. [AI] State one atomic claim or event proposition, its proposed mechanism, expected effect, scope, and what evidence would discriminate it from plausible alternatives.
2. [HYBRID] Trace the earliest available originating evidence and build lineage among original material, direct replications, derived analyses, commentary, syndication, and simple repetition; do not count echoes as independent corroboration.
3. [AI] Deliberately search for independent support and independent contradiction, including failed replications, counterexamples, methodological criticism, alternative explanations, and current authoritative guidance when that source class can answer the question.
4. [HYBRID] Assess source authority for the specific fact type, directness, method/sample/control quality, reproducibility, platform/market specificity, commercial context, and whether the measured outcome is causal, correlational, proxy, or actual business value.
5. [HYBRID] Assess freshness relative to mechanism volatility and record original publication/event time, retrieval time, latest material corroboration/contradiction, and relevant market/platform/version context when available.
6. [AI] Compare the proposition semantically with current Insights/Learnings to classify novelty as new mechanism, material extension, changed applicability, fresh replication, contradiction, or mostly renamed/repackaged prior knowledge.
7. [HYBRID] Create/update the narrowest Insight status and confidence justified by the evidence; preserve supporting, contradicting, contextualizing, and derived evidence separately and keep unresolved causal ambiguity explicit.
8. [DETERMINISTIC] Store structured triangulation details in `Insight.extensions.external_learning`, including original source refs, independent support refs, independent contradiction refs, echo/derived refs, freshness context, novelty classification, unresolved confounds, and relevant SourceProfile refs.

## Verification
- Independent evidence and echo volume are never conflated.
- Source history may guide attention but is not itself support for the current claim.
- Mixed or insufficient evidence stays mixed/uncertain instead of being forced into a positive conclusion.

## Completion Criteria
- A downstream domain can see the claim, provenance graph, independent support/contradiction, freshness, novelty, method limits, confidence, and unresolved questions without redoing the research.
