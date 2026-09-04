---
id: seo.diagnosis.ai-citation-gap
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
- Observation
writes:
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# AI Citation & Recommendation Gap

## Purpose
Understand high-value prompts where relevant competitors or sources appear but the organization is absent, inaccurately represented, or poorly cited, and determine whether a legitimate AEO response exists.

## Business Outcome
Explain material AI citation/recommendation gaps without promising inclusion, optimizing vanity coverage, or turning AURA into an opportunity scanner.

## Run When
Use when sufficiently current answer observations exist for decision-relevant prompts and the user/model needs to understand an AI citation, mention, recommendation, or representation gap.

## Process
1. [HYBRID] Select prompt/question clusters that matter to the audience and business and use observations stable enough for the decision. Preserve surface, timestamp, answer context, citation/mention state, and other evidence needed to reproduce material observations.
2. [AI] Classify the actual gap separately: no mention, no recommendation, no citation, wrong cited URL, inaccurate facts, competitor/source dominance, missing source type, or another observed condition.
3. [HYBRID] Relate the gap to demand/business value, owned-asset suitability, factual/evidence coverage, authority/reputation, entity/local consistency, and the source patterns actually cited by the surface. Exact joins may be mechanical; suitability and business meaning are model judgments.
4. [AI] Determine whether a legitimate response could involve improving owned content/evidence, technical/indexability, entity consistency, local/reputation work, earned third-party coverage, or no SEO/AEO action. Do not assume every absence is controllable.
5. [AI] Preserve an Opportunity only when the gap is materially valuable, plausibly addressable, and supported by surface-specific evidence. Never claim or imply guaranteed inclusion, citation, recommendation, or answer behavior.
6. [HYBRID] When later evaluation would materially help, preserve the re-observation scope, evidence needed, and success/guardrail measures. The harness owns any future recheck schedule.

## Verification
- Material claims preserve enough prompt/question, surface, timestamp, answer, citation, and mention evidence to be reproducible.
- The intervention hypothesis stays within the observed evidence and current organization truth.
- Absence from one answer/sample is not generalized beyond the evidence.
- AI-answer inclusion is not treated as guaranteed or directly controllable.

## Deterministic local-site evidence
When scoped evidence is a local/first-party website export, use `scripts/inspect_site_evidence.py` and persist material direct Observations through `scripts/persist_site_observation.py` using captured fact IDs when those helpers apply. Keep consequences and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.
