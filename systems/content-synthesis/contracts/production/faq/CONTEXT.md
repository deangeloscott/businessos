---
id: content.production.faq
type: playbook
owner_system: content-synthesis
artifact_role: customer_facing_production_root
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
# FAQ Content Production

## Purpose
Create evidence-backed answers to recurring audience questions in a form that is easy to find and understand.

## Business Outcome
Resolve real customer/audience uncertainty accurately without manufacturing questions or over-answering beyond evidence.

## Run When
Run when Customer/SEO/Support/Industry/Marketing intelligence identifies recurring questions suitable for reusable content.

## Process
1. [DETERMINISTIC] Resolve the actual question evidence, audience/context, relevant canonical facts/Insights, and any search/marketing requirements.
2. [AI] Normalize duplicate phrasings into distinct underlying questions while preserving the language people use.
3. [AI] Prioritize by frequency, decision impact, risk, confusion, and fit for the target Asset—not frequency alone.
4. [AI] Write the direct answer first, then necessary explanation, conditions, example, and next step.
5. [HYBRID] Identify questions requiring expert/legal/medical/financial or other high-stakes review and constrain unsupported advice.
6. [DETERMINISTIC] Fact-check each answer and link sources/proof where appropriate.
7. [AI] Produce FAQ Asset/sections and route search/persuasion/journey-specific requirements back to their owner.
