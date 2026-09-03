---
id: customer.analysis.segmentation
type: workflow
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
- AudienceSegment
- ContextUpdateProposal
context:
- Business
- Market
- Objective
- ProductService
- AudienceSegment
---
# Customer Segmentation Intelligence

## Purpose
Identify evidence-backed customer differences that warrant distinct treatment rather than inventing personas.

## Business Outcome
Improve decisions by preserving only customer distinctions that materially change needs, buying behavior, experience, economics, or the action the business should take.

## Run When
Use when a decision may benefit from more precise customer segmentation and the current AudienceSegment definitions or supporting evidence are too broad, stale, weakly supported, or no longer decision-useful.

## Process
1. [AI] Start from the business decision segmentation must improve and the current canonical AudienceSegments; do not assume new segments are needed.
2. [HYBRID] Assemble current customer evidence that can reveal meaningful differences in needs, jobs/outcomes, criteria, language, objections, triggers, behavior, value, success, churn, or journey patterns. Draw on evidence-coverage or segment-brief methods when they materially improve the work; neither is a mandatory prerequisite.
3. [AI] Propose boundaries only where the differences are durable enough to matter and can plausibly change a business decision, experience, message, offer, product choice, or measurement.
4. [HYBRID] Test candidate segments for evidence strength, stability, interpretability, reachability/actionability, overlap, and sufficient business relevance. Avoid prohibited or inappropriate use of sensitive characteristics.
5. [AI] Reject distinctions that are merely channel behavior, a one-off preference, sparse anecdotes, convenient demographic labels, or clustering with no decision consequence.
6. [HYBRID] Compare plausible alternative segmentations and state what decision would change under each, what evidence is missing, and what would falsify the proposed boundary.
7. [HYBRID] If evidence and an authoritative organization decision establish a corrected AudienceSegment definition, update canonical context through the normal memory path. Preserve a ContextUpdateProposal only when the possible correction remains unresolved and remembering that unresolved candidate will materially help future work.

## Completion Criteria
- Each segment distinction is traceable to evidence and a meaningful decision consequence.
- Established evidence, inference, uncertainty, and unresolved gaps remain distinct.
- Supporting Workflows are optional expert methods, not a composition graph.
- Canonical context is updated directly when truth is established; unresolved proposals are preserved only when they are useful memory.
