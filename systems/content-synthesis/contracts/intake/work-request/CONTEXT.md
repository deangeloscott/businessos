---
id: content.intake.work-request
type: playbook
version: 1.1.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- WorkRequest
- Opportunity
- Insight
- Asset
writes:
- WorkRequest
- ActionPacket
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - creative.image.generate
  - creative.video.generate
  - video.render
context:
- AudienceSegment
- Brand
---
# Content Work Request Intake

## Purpose
Accept delegated content production while preserving the originating Opportunity and exact success criteria.

## Business Outcome
Create or improve content work request intake so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires content work request intake and existing Assets do not already satisfy the communication need.

## Process
1. [DETERMINISTIC] Validate WorkRequest origin, requesting/executing systems, Opportunity/Action references, business ID, return contract, and required output.
2. [AI] Restate the communication job: audience, objective, context of consumption, required action/outcome, constraints, proof, and upstream intelligence.
3. [HYBRID] Identify missing inputs that genuinely block production versus details the Content OS can infer/research safely.
4. [AI] Determine whether the request constrains platform/format or Content should choose them.
5. [DETERMINISTIC] Resolve production/rendering/publishing capabilities and approval constraints.
6. [HYBRID] Build content production Actions under the originating WorkRequest; do not create a duplicate Opportunity.
7. [DETERMINISTIC] Return explicit accepted/blocked state and next contract route.
