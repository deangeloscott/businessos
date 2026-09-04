---
id: seo.execution.aeo.surface-configuration
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
# Answer Surface Selection & Observation Design

## Purpose
Determine which AI, generative-search, assistant, answer-engine, voice, or platform-native discovery surfaces materially matter for the business and how observations from each should be interpreted.

## Business Outcome
Focus AEO attention on relevant answer surfaces and preserve surface-specific evidence without assuming they behave identically or that novelty equals business importance.

## Run When
Use when the organization needs to decide which answer surfaces are relevant to a market/audience or when material platform, audience, or access changes make an earlier observation design stale.

## Process
1. Identify the answer/discovery surfaces plausibly used by the relevant audience, market, need, or purchase decision rather than inventorying every available AI product.
2. For important surfaces, document the observable evidence that matters for the current work: prompt/question input, answer text, citations/links, recommendations, location/personalization context, referrals, and other meaningful output or measurement behavior.
3. Prioritize surfaces by audience relevance, business pathway, decision importance, and practical observability—not novelty, popularity, or tool availability alone.
4. Define sampling/context controls useful for interpretation, such as locale, signed-in state, personalization, device, or repeated observations where the surface makes them material. Record limitations rather than pretending they can always be controlled.
5. Preserve surface-specific observation details while keeping shared concepts such as prompt, answer, citation, mention, recommendation, timestamp, and context comparable enough for cross-surface analysis when appropriate.
6. Revisit the selection/design when platform behavior, audience use, market relevance, or available evidence changes enough that the old design could mislead the current decision. Any recurring check belongs to the host/runtime.

## Proportionate Scope
Start with the few surfaces most likely to matter to the actual audience and business outcome. Broaden only when additional surfaces may materially change the conclusion or represent a distinct customer discovery path.

## Verification
- Surface relevance is grounded in audience/business context rather than novelty.
- Differences in personalization, citation behavior, observability, and measurement remain visible.
- Lack of API/tool access does not make a surface irrelevant, and tool availability does not make it important.
- AURA records useful observation design; it does not own provider configuration or recurring execution.
