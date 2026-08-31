---
id: seo.execution.aeo.source-gap
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
# AI Source Gap Analysis

## Purpose
Identify what information sources answer systems repeatedly rely on and what owned/earned information is missing or uncompetitive.

## Business Outcome
Improve valuable organic discovery through ai source gap analysis, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **AI Source Gap Analysis**, or when an authorized incident response requires it.

## Process
1. [HYBRID] For a high-value prompt cluster, aggregate cited domains/pages and non-cited prominent entities across observations.
2. [AI] Classify source roles: primary evidence, product/vendor page, editorial authority, community/user-generated, directory/database, news, local/review, etc.
3. [HYBRID] Compare source content, evidence, freshness, structure, authority, and unique information against owned assets.
4. [AI] Identify the actual gap: missing answer, weak evidence, inaccessible content, poor entity consistency, weak reputation/authority, absent third-party coverage, or no legitimate owned fit.
5. [HYBRID] Route to content, on-page, technical, reputation, local, digital PR, or authority playbooks as appropriate.
6. [HYBRID] Reject attempts to mimic a source purely for citation if it would not add equivalent user/information value.


