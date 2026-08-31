---
id: seo.execution.aeo.surface-configuration
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - ai_answer.observe
  optional:
  - research.web.read
  - cms.page.read
  - cms.page.update
  - analytics.read
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# Answer Surface Configuration

## Purpose
Define which AI/generative/answer surfaces matter for a brand and how each can be observed without assuming identical behavior.

## Business Outcome
Improve valuable organic discovery through answer surface configuration, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Answer Surface Configuration**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory relevant AI search, generative search, assistant, answer-engine, voice, and platform-native discovery surfaces by market/audience.
2. [AI] Document observable capabilities per surface: prompt input, citations/links, recommendations, answer text, location/personalization, referral data, and API/tool availability.
3. [HYBRID] Prioritize surfaces by audience relevance, conversion pathway, observability, and business importance—not novelty.
4. [HYBRID] Define compliant sampling methods, locales, signed-in/personalization controls where possible, and evidence limitations.
5. [HYBRID] Create surface-specific measurement fields while maintaining a shared canonical answer-observation schema.
6. [HYBRID] Review configuration when platforms, audiences, or access capabilities materially change.


