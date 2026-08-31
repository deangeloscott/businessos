---
id: content.research.research-plan
type: playbook
version: 1.3.0
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - creative.image.generate
  - creative.audio.generate
  - creative.video.generate
  - creative.animation.generate
  - creative.avatar_video.generate
  - video.render
  - presentation.render
  - document.render
  - social.content.publish
  - social.content.schedule
  - cms.page.publish
  - email.content.publish
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Research Plan

## Purpose
Determine what additional factual/contextual research is required to create an accurate, useful asset after reusing existing intelligence.

## Business Outcome
Fill only the evidence gaps necessary for content without recreating Customer, Competitor, Industry, or SEO research.

## Run When
Run when the brief identifies unanswered factual/contextual questions that materially affect the asset.

## Process
1. [DETERMINISTIC] Inventory current canonical Insights, SourceRecords, ProofRecords, business context, and existing relevant Assets.
2. [AI] List only the unanswered questions necessary for accuracy, usefulness, examples, or audience understanding.
3. [AI] Classify each question by canonical owner and request refresh when another OS already owns the intelligence.
4. [AI] Identify bounded source research that Content can legitimately perform itself, such as fact checking or source support.
5. [HYBRID] Define freshness/authority requirements for high-consequence claims.
6. [DETERMINISTIC] Set a stopping rule once sufficient evidence exists; avoid open-ended browsing for more interesting facts.
7. [AI] Produce research tasks/WorkRequests and feed resolved evidence back into the content brief.
