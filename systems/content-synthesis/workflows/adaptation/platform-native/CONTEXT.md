---
id: content.adaptation.platform-native
type: workflow
owner_system: content-synthesis
reads:
- Asset
- Insight
- Learning
- PlatformProfile
writes:
- Asset
context:
- AudienceSegment
- Brand
---
# Platform-Native Adaptation

## Purpose
Transform a validated core idea into genuinely native expressions for selected platforms rather than superficial reformatting.

## Business Outcome
Create or improve platform-native adaptation so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Use when platform-native adaptation would materially improve an existing idea/Asset and current Assets do not already satisfy the communication need.

## Process
1. [AI] Reconstruct the core Insight, audience, objective, nonnegotiable evidence, and what can change in expression. Audience-context operating knowledge may help when that context is not already clear; it is not a mandatory stage.
2. [HYBRID] Load the current PlatformProfile for each selected surface. If missing/stale and platform mechanics materially affect the decision, `content.strategy.platform-profile-refresh` may be useful before finalizing the adaptation.
3. [AI] For each target platform identify consumption context, native behavior, attention pattern, format grammar, interaction, typical depth, and desired action.
4. [AI] Re-conceive hook, structure, pacing, examples, visuals, language, and CTA independently for each platform.
5. [HYBRID] Preserve factual meaning and brand while allowing different emphasis/order/depth; reject simple truncation/resize when it produces weak native fit.
6. [AI] Identify platform-specific source/proof/creative needs and the smallest useful production approach.
7. [INTEGRATION] Produce/render each selected expression using the active harness's available tools or relevant format-specific operating knowledge. Do not create internal production contracts merely to hand work between AURA Workflows.
8. [HYBRID] QA each actual asset independently rather than assuming the source asset quality transfers. Platform QA knowledge may be useful for a final platform-specific Asset, but it is not a machine-required subworkflow.
