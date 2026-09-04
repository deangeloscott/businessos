---
id: content.production.faq
type: workflow
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
Use when recurring questions are evidenced strongly enough to justify reusable FAQ content.

## Process
1. [DETERMINISTIC] Resolve the actual question evidence, audience/context, relevant canonical facts/Insights, and any material search/marketing requirements.
2. [AI] Normalize duplicate phrasings into distinct underlying questions while preserving the language people use.
3. [AI] Prioritize by frequency, decision impact, risk, confusion, and fit for the target Asset—not frequency alone.
4. [AI] Write the direct answer first, then necessary explanation, conditions, example, and next step.
5. [HYBRID] Identify questions requiring expert/legal/medical/financial or other high-stakes review and constrain unsupported advice.
6. [DETERMINISTIC] Fact-check each answer and link sources/proof where appropriate.
7. [AI] Preserve the useful FAQ Asset/sections. Reuse relevant SEO, persuasion, support, or journey operating knowledge directly when those considerations materially affect the output; do not create internal ownership handoffs or routine WorkRequests.
