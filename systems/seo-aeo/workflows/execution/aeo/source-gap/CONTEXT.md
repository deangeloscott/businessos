---
id: seo.execution.aeo.source-gap
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
# AI Source Gap Analysis

## Purpose
Identify what information sources answer systems repeatedly rely on and what useful owned or earned information is missing or uncompetitive.

## Business Outcome
Improve valuable answer-engine discovery by identifying the real information/evidence gap behind citation or recommendation patterns, not by chasing citations as an end in themselves.

## Run When
Use when current answer observations for a valuable prompt/question set show meaningful source patterns or brand/source gaps that could affect the business decision.

## Process
1. For the relevant prompt/question cluster, aggregate cited domains/pages and important non-cited entities only to the depth needed to reveal stable source patterns.
2. Classify source roles where useful: primary evidence, product/vendor page, editorial authority, community/user-generated, directory/database, news, local/review, or another meaningful role.
3. Compare the source information, evidence, freshness, structure, accessibility, authority, and unique value against owned or already-earned assets.
4. Identify the actual gap: missing answer, weak evidence, inaccessible content, poor entity consistency, weak reputation/authority, absent third-party coverage, or no legitimate owned fit.
5. Use the most relevant content, on-page, technical, reputation, local, digital-PR, authority, or other operating knowledge directly when a legitimate intervention exists. Do not create an internal routing step merely to continue the work.
6. Reject attempts to mimic a cited source purely for inclusion when the business cannot provide equivalent or better user/information value.

## Proportionate Scope
Start with the sources and prompts most likely to change the business conclusion. Broaden the sample when citation patterns are unstable, contradictory, high-stakes, or materially different across answer surfaces.

## Verification
- Preserve enough prompt/question, surface, timestamp, answer, and citation evidence to support material conclusions.
- Citation prevalence is evidence about observed source use, not proof of causality, authority, or guaranteed future inclusion.
- The recommended response adds genuine information value rather than cargo-culting a source format.
