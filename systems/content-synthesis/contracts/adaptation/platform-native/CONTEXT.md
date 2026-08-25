---
id: content.adaptation.platform-native
type: playbook
version: 1.3.0
owner_system: content-synthesis
artifact_role: customer_facing_production_root
risk: low
autonomy_ceiling: 4
reads:
- Asset
- Insight
- Learning
- PlatformProfile
writes:
- Asset
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
subcontracts:
  required:
  - content.strategy.audience-context
  conditional:
  - id: content.qa.platform
    when: a final platform-specific Asset is produced
---
# Platform-Native Adaptation

## Purpose
Transform a validated core idea into genuinely native expressions for selected platforms rather than superficial reformatting.

## Business Outcome
Create or improve platform-native adaptation so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires platform-native adaptation and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Reconstruct the core Insight, audience, objective, nonnegotiable evidence, and what can change in expression.
2. [HYBRID] Load the current PlatformProfile for each selected surface; if missing/stale and platform mechanics materially affect the decision, route `content.strategy.platform-profile-refresh` before finalizing the plan.
3. [AI] For each target platform identify consumption context, native behavior, attention pattern, format grammar, interaction, typical depth, and desired action.
4. [AI] Re-conceive hook, structure, pacing, examples, visuals, language, and CTA independently for each platform.
5. [HYBRID] Preserve factual meaning and brand while allowing different emphasis/order/depth; reject simple truncation/resize when it produces weak native fit.
6. [AI] Identify platform-specific source/proof/creative needs and production plan.
7. [INTEGRATION] Produce/render each selected expression or delegate format-specific production contracts.
8. [HYBRID] QA each asset independently rather than assuming the source asset quality transfers.
