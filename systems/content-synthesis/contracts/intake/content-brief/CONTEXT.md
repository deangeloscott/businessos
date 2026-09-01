---
id: content.intake.content-brief
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
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Brief

## Purpose
Define the communication job precisely enough that a capable model can produce strong content without rediscovering the audience, evidence, platform context, and material requirements.

## Business Outcome
Improve content quality and continuity by carrying forward the organizational context that materially shapes the asset while leaving creative execution flexible.

## Run When
Use before material content production when the current task lacks a sufficiently clear, current communication brief. An Opportunity or a real durable WorkRequest may provide context, but neither is required merely to create content.

## Process
1. [HYBRID] Reuse the relevant audience, objective, Brand/Offer context, platform context, current Insights, ProofRecords, upstream requirements Assets, existing content, and any real WorkRequest that happens to exist. Load only what can materially improve the current asset.
2. [AI] State the communication job: what the audience should understand, feel, remember, or do after consuming the content and why that matters to the business/user request.
3. [AI] Define the audience starting state, consumption context, core message, supporting points, evidence/proof, desired action, required facts, and material exclusions at the confidence the evidence supports.
4. [AI] Separate fixed constraints/requirements from creative choices and identify outward claims that need business-truth/evidence support.
5. [HYBRID] Resolve real conflicts among Brand, audience needs, platform behavior, upstream requirements, evidence, user instructions, and legal/contractual constraints. Do not manufacture a generic approval gate.
6. [AI] Define only the deliverables/variants, format requirements, quality checks, publication destination, and measurement intent that materially improve the job. The active model/harness chooses real production/rendering tools.
7. [AI] Produce a concise brief that references durable organizational evidence/requirements instead of copying large source material. Persist it as an internal Content-owned `Asset` only when future sessions/actors materially benefit; otherwise use it directly in the current work.
8. [AI] If a real cross-person/model/session handoff must survive the current runtime, `core.continuity.manage-handoff` may preserve that separately. Content does not require an internal WorkRequest merely because another AURA domain supplied useful context.

## Verification
- The brief preserves material upstream evidence and business/brand truth without treating another domain's recommendation as execution authority.
- Creative choices remain flexible unless a real requirement constrains them.
- Claims/evidence requirements are visible enough to protect customer-facing truth.
- No return contract, accepted/blocked state, Action lifecycle, capability preflight, or internal routing step is required.

## Completion Criteria
- A capable model can produce the intended content without rebuilding the communication problem, and any persisted brief is useful durable organizational knowledge rather than internal orchestration state.
