---
id: seo.execution.aeo.competitive-answer-share
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
# Competitive Answer Share

## Purpose
Measure relative brand and competitor representation across a defined, decision-relevant prompt universe.

## Business Outcome
Understand where the business is or is not represented in valuable answer contexts without turning unlike answer signals into one vanity score.

## Run When
Use when the organization needs a comparative view of brand versus competitor representation across current Answer Observations.

## Process
1. Define the measurement universe and any weighting by prompt business value so low-value questions do not dominate the result.
2. Classify observations separately for owned-brand mention, recommendation, citation/link, meaningful order/grouping, and competitor equivalents.
3. Calculate separate interpretable measures for mention share, recommendation share, citation share, prompt coverage, and high-value prompt coverage only where the sample supports them.
4. Segment by intent, awareness stage, topic, market, or surface when those dimensions materially change interpretation.
5. Inspect material changes for prompt-universe drift, sampling changes, answer-system variability, or other confounders before attributing movement to business interventions.
6. Identify the important competitive gaps or strengths and use the relevant diagnosis/source/content/authority method directly. Preserve an Opportunity only when durable coordination is useful.

## Proportionate Scope
Use the smallest stable prompt and surface sample that can answer the competitive question. Expand when representation differs materially across segments or sampling uncertainty could change the conclusion.

## Verification
- Mention, recommendation, citation, order, and business value remain distinct.
- Sample and prompt-universe changes remain visible when comparing periods.
- Competitive answer share is not presented as causal evidence of an intervention or as a universal composite score.
