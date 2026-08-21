---
id: seo.execution.aeo.question-universe
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
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
# Question / Prompt Universe

## Purpose
Build and continuously refresh the high-value questions and conversational prompts through which buyers may discover or evaluate the brand/category.

## Business Outcome
Improve valuable organic discovery through question / prompt universe, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Question / Prompt Universe**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Start from Brand Context, awareness stages, customer objections, support/sales language, keyword/topic clusters, offers, and competitor observations.
2. [AI] Generate natural conversational forms including broad discovery, problem diagnosis, comparisons, recommendations, constraints, local needs, follow-ups, and brand-specific verification.
3. [HYBRID] Mine observed first-party queries, on-site search, sales/support questions, AI grounding/query data, and available third-party evidence.
4. [HYBRID] Cluster semantic duplicates while preserving materially different constraints, persona, geography, stage, and intent.
5. [AI] Map every prompt cluster to business value, expected answer type, target asset/entity, and relevant surfaces.
6. [HYBRID] Sample and rerank continuously as demand, products, competitors, and observed answers change.


