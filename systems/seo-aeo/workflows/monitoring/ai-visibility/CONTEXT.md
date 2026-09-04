---
id: seo.monitoring.ai-visibility
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- MetricObservation
- Opportunity
- Incident
- SEOAssetState
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
updates:
  SEOAssetState:
  - organic_performance
---
# AI / Answer Visibility Monitoring

## Purpose
Refresh high-value prompt observations and detect material changes in brand representation, recommendations, citations, competitors, and factual accuracy without turning AURA into the answer-surface monitoring runtime.

## Business Outcome
Keep AI/answer visibility understanding current enough to recognize gains or losses in valuable exposure and the resulting opportunity for consideration, referral traffic, leads, and other business outcomes while preserving exact evidence and uncertainty.

## Run When
Use for a bounded AI/answer visibility check when the user requests it, saved monitoring intent indicates another check would be useful, or a material business/platform change warrants re-observation. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Sample the decision-relevant prompt/question universe across relevant answer surfaces with the strongest observation capabilities available to the active harness, using stable sampling controls where comparison matters.
2. [AI] Extract mentions, recommendations, citations/links, cited assets/domains, competitors, factual claims, and observable referral evidence.
3. [HYBRID] Compare value-weighted coverage/share with previous samples while accounting for nondeterminism, prompt-universe changes, market/context differences, and evidence limitations.
4. [AI] Judge whether new/lost citations, recommendation shifts, competitor displacement, or inaccurate claims are materially relevant to the active business. Repeated presence for valuable prompts can be meaningful because it increases the organization's opportunity to be seen, considered, or used as a source; it is not by itself proof of downstream traffic or revenue.
5. [AI] Preserve the smallest useful MetricObservation/SEOAssetState/Observation update. If the evidence genuinely warrants deeper diagnosis, an Opportunity, an Incident, verification, or Learning review, the model may select that method separately; monitoring does not route or create those states automatically.
6. [HYBRID] Keep surface-specific measurements separate; do not invent a universal AI ranking or collapse citation, mention, recommendation, referral, and business-outcome evidence into one score.

## Verification
- Preserve the exact prompt/question, surface, timestamp, answer evidence, and citation/mention status needed to interpret material observations.
- AI visibility and downstream outcomes remain distinct while their credible business pathway may inform prioritization and judgment.
- Saved cadence/checkpoint intent never proves a recurring task exists; only the external runtime can establish that execution state.
