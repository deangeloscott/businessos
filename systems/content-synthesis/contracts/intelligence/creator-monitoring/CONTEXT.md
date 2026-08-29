---
id: content.intelligence.creator-monitoring
type: detector
version: 1.3.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- PlatformProfile
writes:
- SourceProfile
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - none
  optional:
  - creator_content.observe
  - social.observe
  - public_comment.read
  - rss.read
  - research.web.read
  - document.read
  - webpage.snapshot
  - webpage.screenshot
  - crawler.run
schedule:
  class: recurring
  default: weekly
  configurable: true
context:
- AudienceSegment
- Brand
---
# Creator Content Monitoring

## Purpose
Build and maintain a durable, cross-source understanding of selected creators/channels for content mechanisms, topics, teachings, messaging/style, offers, and meaningful shifts that can inform original business content.

## Business Outcome
Continuously learn from strong public creative execution without copying creator-specific expression, losing cross-channel history, or confusing popularity with transferable effectiveness.

## Run When
Run on the configured creator-watch cycle, when a creator/category is added because it is strategically useful to study, or when the user asks for a deep/current understanding of a specific creator or channel.

## Process
1. [DETERMINISTIC] Load/reuse the shared creator subject key, resolved SourceProfiles, last checkpoints, target platforms/surfaces, and the reason/questions each creator is relevant. Do not create a content-owned duplicate identity system.
2. [HYBRID] Expand identity across other public profiles/website/newsletter/podcast only when evidence supports that they belong to the same subject. Preserve ambiguous accounts separately.
3. [INTEGRATION] Retrieve the minimum sufficient new or historical corpus for the request with source, format, date, visible context/performance signals, and relevant surrounding items/comments when comparison is needed.
4. [HYBRID] Inspect the modalities that materially carry the mechanism: spoken/transcript content, visual composition, thumbnails/key frames, demonstrations/screens, editing/pacing, captions, descriptions, posts, comments, or linked pages. Prefer native multimodal inspection when available; use legitimate transcript/frame/document fallbacks and record limitations.
5. [DETERMINISTIC] Identify unusually strong, novel, or changing items relative to the creator's own baseline and appropriate peer/context where enough data exists. Treat visible engagement/volume as a proxy, not proof of business outcome.
6. [AI] Decompose candidate content into topics/teachings, hooks, structure, pacing, proof, storytelling, visual/audio devices, interaction, payoff, CTA, distribution context, offers, and recurring audience response.
7. [AI] Separate creator-specific advantages/expression from patterns that could plausibly transfer to another brand/audience; do not copy protected expression or style so specifically that it substitutes for the creator.
8. [HYBRID] Compare patterns across the creator's channels, over time, and against existing Content Insights/Learnings before calling something a stable pattern or meaningful shift.
9. [DETERMINISTIC] Publish source-backed Observations/Content Insights, update shared SourceProfile checkpoints, and route non-content signals (for example company funding/strategy or broad industry events) to their semantic owner.
