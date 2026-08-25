---
id: content.production.linkedin
type: playbook
version: 1.1.0
owner_system: content-synthesis
artifact_role: customer_facing_production_root
risk: low
autonomy_ceiling: 4
reads:
- WorkRequest
- Opportunity
- Insight
- SourceRecord
- Asset
writes:
- Asset
- Observation
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - creative.image.generate
  - creative.image.edit
  - creative.audio.generate
  - creative.video.generate
  - creative.animation.generate
  - video.render
  - presentation.render
  - document.render
context:
- AudienceSegment
- Brand
---
# LinkedIn Native Content

## Purpose
Create professional-network content that is native to feed behavior rather than an article pasted into a post.

## Business Outcome
Create or improve linkedin native content so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires linkedin native content and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define professional audience, conversational context, credible point of view, and whether the objective is teach, provoke useful discussion, demonstrate expertise, or distribute an asset.
2. [AI] Select native expression such as concise text, story/lesson, document carousel, image/data post, or short native video based on idea mechanics.
3. [AI] Write a first-screen opening that creates legitimate relevance/tension without clickbait withholding.
4. [AI] Structure for mobile feed scanning, progressive value, specific examples, and a natural closing action/question where appropriate.
5. [HYBRID] Remove corporate filler, fake vulnerability, engagement bait, and claims unsupported by evidence.
6. [DETERMINISTIC] Package platform-ready copy/media specs and Asset metadata.
