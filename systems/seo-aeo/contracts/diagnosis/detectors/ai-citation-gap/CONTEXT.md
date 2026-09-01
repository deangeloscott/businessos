---
id: seo.diagnosis.detectors.ai-citation-gap
type: detector
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
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.serp.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# AI Citation / Recommendation Gap Detector

## Purpose
Find high-value prompts where relevant competitors/sources appear but the brand is absent or poorly represented.

## Business Outcome
Explain material AI citation/recommendation gaps well enough to decide whether a useful SEO/AEO response exists without promising inclusion or turning AURA into an opportunity scanner.

## Run When
Use when fresh relevant answer observations exist and the user/model needs to diagnose an **AI citation / recommendation gap**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Select decision-relevant prompt clusters and Answer Observations with sufficiently stable evidence for the question.
2. [AI] Classify the gap separately: no mention, no recommendation, no citation, wrong cited URL, inaccurate facts, competitor dominance, or missing source type.
3. [HYBRID] Relate the gap to demand/business value, owned-asset suitability, factual/evidence coverage, authority/reputation, and cited-source patterns. Exact joins may be mechanical; suitability and business meaning are model judgment.
4. [AI] Determine whether a legitimate intervention could involve content, evidence, technical/indexing, entity consistency, local/reputation, earned third-party coverage, or no SEO action at all.
5. [AI] Create or update an AEO Opportunity only when the gap is materially valuable, plausibly addressable, and supported by surface-specific evidence; never claim guaranteed inclusion.
6. [HYBRID] When future evaluation would help, preserve the re-observation sample, evaluation window, and success/guardrail measures as method/evaluation context. AURA does not schedule the recheck itself.

## Verification
- Preserve the exact prompt/question, surface, timestamp, answer evidence, and citation/mention status needed to reproduce material observations.
- Opportunity scope and intervention hypothesis stay within the observed evidence.

## Deterministic local-site evidence
When the scoped evidence is a local/first-party website export, do not hand-author material direct site facts from model memory or prose inspection. Run `scripts/inspect_site_evidence.py`, then persist material direct Observations through `scripts/persist_site_observation.py` using the captured fact IDs. Keep consequences, severity, and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.
