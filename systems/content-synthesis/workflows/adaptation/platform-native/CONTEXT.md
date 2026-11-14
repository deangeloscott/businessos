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
Adapt or localize video, audio, and other content for selected platforms, languages, or markets while preserving meaning and creating a suitable audience experience.

## Business Outcome
Create or improve platform-native adaptation so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Use to localize or adapt an existing video, audio, or other asset for another platform, language, or market, including translated subtitles, dubbed speech, and on-screen graphics.

## Process
1. [AI] Reconstruct the core Insight, audience, objective, nonnegotiable evidence, and what can change in expression. Audience-context operating knowledge may help when that context is not already clear; it is not a mandatory stage.
2. [HYBRID] Load the current PlatformProfile for each selected surface. If missing/stale and platform mechanics materially affect the decision, `content.strategy.platform-profile-refresh` may be useful before finalizing the adaptation.
3. [AI] For each target audience and surface identify relevant consumption context, language/locale, native behavior, format, interaction, depth, and intended effect or action.
4. [AI] Adapt hook, structure, pacing, examples, visuals, language, and any CTA to that context. For localization, preserve factual meaning and established terminology while adapting idioms, delivery, text layout, and timing where needed; use the optional craft reference for more detail.
5. [HYBRID] Preserve factual meaning and brand while allowing different emphasis/order/depth; reject simple truncation/resize when it produces weak native fit.
6. [AI] Identify platform-specific source/proof/creative needs and the smallest useful production approach.
7. [INTEGRATION] Produce/render each selected expression using the active harness's available tools or relevant format-specific operating knowledge. Do not create internal production contracts merely to hand work between AURA Workflows.
8. [HYBRID] QA each actual asset independently rather than assuming the source asset quality transfers. Platform QA knowledge may be useful for a final platform-specific Asset, but it is not a machine-required subworkflow.

## Optional craft references

The [creative localization reference](../../../../../recipes/creative/creative-localization.md) covers meaning, cultural context, spoken performance, subtitles, on-screen graphics, and review of the actual target-language artifact. Use only the concerns that matter to the adaptation.
