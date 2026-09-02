---
id: seo.execution.aeo.aeo-content-optimization
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
- OrganicDemandUnit
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
- records topic intent evidence
---
# Answer-Oriented Content Optimization

## Purpose
Improve owned information so it is clear, useful, evidence-rich, retrievable, and appropriate for both human search and answer systems.

## Business Outcome
Better satisfy valuable customer questions and strengthen the quality of information answer/search systems can retrieve without creating machine-targeted “AI pages” that reduce human usefulness.

## Run When
Use when a diagnosed question, answer, source, factual, or information gap indicates an existing or justified owned Asset can materially serve the audience better.

## Process
1. Start from the actual question/intent, observed gap, and the most appropriate existing or justified target Asset. Do not create a separate “AI page” when an existing page can serve the user well.
2. Make the answer or information need clear and directly accessible, with terminology, scope, supporting explanation, and next actions appropriate to the audience rather than optimizing for a guessed model pattern.
3. Add or improve original evidence, authoritative sourcing, verified product/service facts, definitions, comparisons, tables/lists, examples, and entity relationships only when they materially improve understanding or trust.
4. Remove unsupported claims, filler, hidden/machine-targeted text, redundant passages, or formatting that harms human usefulness merely to appear more “answer optimized.”
5. Verify relevant crawl/index eligibility, internal discovery, canonical consistency, visible-content/structured-data consistency, and conversion alignment when those factors could prevent the improved information from serving its intended purpose.
6. Define later evaluation using the outcomes actually relevant to the job—such as useful search visibility, answer mentions/citations/recommendations, referral traffic, qualified actions, or business outcomes—while keeping them separate and avoiding causal claims the evidence cannot support.

## Proportionate Scope
Improve the smallest Asset or information set capable of resolving the material gap. Expand content depth, evidence, technical work, or supporting assets only when additional work has a reasonable chance of improving user usefulness or changing the discovery outcome.

## Verification
- Human usefulness and factual quality lead; answer-system visibility is not pursued through deceptive or low-value machine-targeted content.
- Material organizational facts and outward claims remain supported by current truth/evidence.
- Structured data, citations, and formatting accurately represent visible content rather than manufacturing eligibility.
- Search, answer visibility, referral, and business outcomes remain separate measurements.
