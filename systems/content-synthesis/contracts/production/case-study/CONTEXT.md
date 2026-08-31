---
id: content.production.case-study
type: playbook
version: 1.3.0
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
# Customer Case Study

## Purpose
Turn verified customer evidence and ProofRecords into a useful, accurate account of context, intervention, mechanism, and outcome.

## Business Outcome
Create credible proof and education without exaggerating attribution or exposing customer information beyond permission.

## Run When
Run when sufficient verified customer proof exists for a case study or success story.

## Process
1. [DETERMINISTIC] Resolve ProofRecords, permission/usage restrictions, customer/account context, relevant product/service, and primary SourceRecords.
2. [AI] Define audience question and select the case only if it is relevant/representative enough for that communication job.
3. [AI] Structure starting situation → constraints/problem → decision/process → what was actually done → observed outcome → mechanism/lesson → limitations.
4. [AI] Separate measured results from customer attribution and business interpretation; preserve timeframe/baseline/conditions.
5. [HYBRID] Remove confidential/sensitive identifiers and obtain any required approval for naming, logos, quotes, screenshots, or results.
6. [AI] Include concrete evidence/examples and avoid unsupported “because of us” causal language.
7. [DETERMINISTIC] Create the Asset, linked ProofRecord references, claim map, and applicable derivatives/QA.
