---
id: content.production.newsletter
type: workflow
owner_system: content-synthesis
reads:
- WorkRequest
- Opportunity
- Insight
- SourceRecord
- Asset
writes:
- Asset
- Observation
context:
- AudienceSegment
- Brand
---
# Newsletter Production

## Purpose
Create a relationship-oriented email/newsletter suited to inbox context and the audience expectation.

## Business Outcome
Create or improve newsletter production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires newsletter production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define the subscriber context, expected relationship, single primary idea, value promise, and desired action. Draw on current audience, message, hook, narrative, or other operating knowledge only when it materially improves the result.
2. [AI] Choose structure appropriate to newsletter type: insight note, curated analysis, story/lesson, update, digest, or educational sequence.
3. [AI] Draft subject/preheader/body with a compelling but truthful opening and early value delivery.
4. [HYBRID] Use links/CTAs proportionately; avoid turning every educational newsletter into a sales letter unless the actual business objective is persuasion/conversion.
5. [AI] Optimize scannability, paragraph length, hierarchy, and mobile inbox reading.
6. [HYBRID] Verify claims, links, personalization tokens, brand/compliance, and deliverable formatting. Draw on pre-publish QA operating knowledge when an additional integrated review is useful.
7. [DETERMINISTIC] Save the useful versioned Asset. If external publishing is actually requested, the active model/harness uses the available authorized publishing capability; AURA does not create a routing or permission workflow.
