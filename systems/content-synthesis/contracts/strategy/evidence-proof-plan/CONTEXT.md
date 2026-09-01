---
id: content.strategy.evidence-proof-plan
type: playbook
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
# Content Evidence and Proof Plan

## Purpose
Match material factual claims and illustrative examples to appropriate sources and ProofRecords before production.

## Business Outcome
Make content credible, traceable, and resistant to unsupported or misleading claims.

## Run When
Run when content includes factual claims, customer outcomes, comparisons, demonstrations, statistics, or consequential advice.

## Process
1. [AI] List material claims the asset intends to make and classify each as fact, interpretation, opinion, example, estimate, or recommendation.
2. [DETERMINISTIC] Resolve supporting SourceRecords, Observations, ProofRecords, canonical context, and usage permissions/restrictions.
3. [AI] Match the strength/scope of each claim to the evidence; narrow or remove claims that exceed support.
4. [AI] Select proof/examples that are representative and relevant to the audience rather than only the most dramatic case.
5. [HYBRID] Check confidentiality, testimonial permission, attribution, sensitive information, and comparison fairness.
6. [AI] Decide where evidence should appear in the content to improve understanding/trust without turning the asset into a citation dump.
7. [DETERMINISTIC] Produce a claim→evidence map for fact-check and final QA.
