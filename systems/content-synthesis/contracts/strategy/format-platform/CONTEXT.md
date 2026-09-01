---
id: content.strategy.format-platform
type: playbook
owner_system: content-synthesis
reads:
- Opportunity
- WorkRequest
- Insight
- Learning
- Asset
- PlatformProfile
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - social.observe
context:
- AudienceSegment
- Brand
---
# Platform & Format Selection

## Purpose
Choose how the idea should be expressed based on audience behavior and consumption context rather than default repurposing.

## Business Outcome
Create or improve platform & format selection so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires platform & format selection and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define audience, objective, awareness, expected attention, desired action, idea complexity, required proof/visuals, and production constraints.
2. [HYBRID] Load the current PlatformProfile for each selected surface; if missing/stale and platform mechanics materially affect the decision, route `content.strategy.platform-profile-refresh` before finalizing the plan.
3. [HYBRID] Evaluate candidate platforms by audience presence/context and existing Business/Content Learnings rather than generic popularity.
4. [AI] Evaluate formats by communication mechanism: text, visual sequence, demonstration, narrative video, talking head, data graphic, audio, interactive, presentation, etc.
5. [AI] Determine whether one core idea warrants multiple genuinely different native expressions or one primary asset.
6. [HYBRID] Reject format/platform choices that merely repackage content with poor native fit.
7. [DETERMINISTIC] Record selected platform/format, rationale, success metric, and required production capabilities.
