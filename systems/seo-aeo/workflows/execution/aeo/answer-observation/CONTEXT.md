---
id: seo.execution.aeo.answer-observation
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# AI Answer Observation

## Purpose
Capture reproducible evidence of how relevant answer systems respond to priority questions so later analysis is based on observed behavior rather than model memory.

## Business Outcome
Provide trustworthy surface-specific evidence for AEO decisions while preserving the non-deterministic and contextual nature of generated answers.

## Run When
Use when a current AEO question requires direct observation of one or more answer surfaces, or when previously useful observations are materially stale for the decision.

## Process
1. Select the smallest useful sample of priority prompts/questions and answer surfaces based on business value, uncertainty, coverage gaps, or a material change being investigated.
2. Record the observable surface/model/product, prompt, locale/context controls, timestamp, and other sampling conditions needed to interpret or reproduce the observation.
3. Capture the answer content or material structured facts, citations/links, recommended entities, meaningful ordering/grouping, and refusal/no-answer states within the real tooling and access available.
4. Resolve important brand, competitor, source, URL, or entity identities accurately enough that later comparison does not merge unrelated evidence.
5. Mark personalization, sampling, product-version, and non-determinism limitations. Repeat or broaden samples when one answer would be materially misleading, not by default.
6. Preserve the resulting Answer Observations. Use citation, factual-accuracy, competitive-share, source-gap, or another relevant analysis method directly when the current task benefits from it; do not create an internal trigger chain.

## Proportionate Scope
Sample enough prompts, surfaces, contexts, and repetitions to support the decision at hand. Expand when answers are unstable, contradictory, high-stakes, or materially different across surfaces; do not maximize sampling merely because more observations are possible.

## Verification
- Material observations retain the prompt/question, surface, timestamp, answer evidence, and citation/mention state needed for interpretation.
- One generated answer is not generalized into a stable surface-wide fact without supporting evidence.
- AURA may remember when re-observation would be useful, but the host/runtime owns any recurring execution.
