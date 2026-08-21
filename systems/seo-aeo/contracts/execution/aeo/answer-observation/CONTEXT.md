---
id: seo.execution.aeo.answer-observation
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
# AI Answer Observation

## Purpose
Record reproducible observations of how relevant answer systems respond to priority questions.

## Business Outcome
Improve valuable organic discovery through ai answer observation, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **AI Answer Observation**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Select prompts from the configured universe using business priority, coverage gaps, refresh cadence, and change events.
2. [DETERMINISTIC] Record surface/model/product if observable, prompt, locale/context controls, timestamp, and sampling conditions.
3. [AI] Capture answer content/structured facts within permitted tooling, citations/links, recommended entities, ordering/grouping where meaningful, and refusal/no-answer states.
4. [DETERMINISTIC] Normalize brand/competitor/entity mentions and map cited URLs/domains to canonical assets/competitors.
5. [HYBRID] Mark personalization/non-determinism limitations and repeat samples where one observation would be misleading.
6. [AI] Write Answer Observations and trigger citation, accuracy, competitive-share, and source-gap analysis.


