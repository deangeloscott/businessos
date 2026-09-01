---
id: content.intelligence.creator-monitoring
type: detector
owner_system: content-synthesis
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
  - media.video.acquire
  - media.transcript.acquire
  - media.metadata.inspect
  - media.video.process
  - media.audio.extract
  - media.frame.extract
context:
- AudienceSegment
- Brand
---
# Creator Content Monitoring

## Purpose
Build or refresh a durable, cross-source understanding of selected creators/channels for content mechanisms, topics, teachings, messaging/style, offers, and meaningful shifts that can inform original business content.

## Business Outcome
Learn from strong public creative execution without copying creator-specific expression, losing useful cross-channel history, or confusing popularity with transferable effectiveness.

## Run When
Use when the user or current content decision needs a current/deeper understanding of a creator or channel, when a selected creator/category becomes strategically useful to study, or when saved SourceProfile/watch context indicates that a bounded refresh would materially help. Any recurring execution is owned by the active harness/runtime.

## Process
1. [HYBRID] Resolve the creator/channel identity, relevant SourceProfiles, prior evidence/checkpoints, target surfaces, and the actual business/content question that makes the subject worth studying. Do not create a duplicate identity system when existing organizational evidence already resolves the subject.
2. [AI] Expand identity across other public profiles, websites, newsletters, podcasts, or channels only when evidence supports that they belong to the same subject. Preserve ambiguity instead of merging uncertain identities.
3. [INTEGRATION] Retrieve the minimum sufficient new or historical corpus for the current question using the host's available capabilities. Capture source, format, date, visible context/performance signals, and surrounding items/comments only where they materially improve interpretation.
4. [HYBRID] Inspect the modalities that actually carry the mechanism: spoken/transcript content, visual composition, thumbnails/key frames, demonstrations/screens, editing/pacing, captions, descriptions, posts, comments, or linked pages. Prefer native multimodal inspection when available; use legitimate transcript/frame/document fallbacks and record material limitations.
5. [HYBRID] Identify unusually strong, novel, or changing items relative to the creator's own prior work and appropriate peer/context when enough evidence exists. Treat visible engagement/volume as a proxy, not proof of business outcome.
6. [AI] Decompose useful examples into topics/teachings, hooks, structure, pacing, proof, storytelling, visual/audio devices, interaction, payoff, CTA, distribution context, offers, and recurring audience response.
7. [AI] Separate creator-specific advantages/expression from mechanisms that could plausibly transfer to another brand/audience. Do not copy protected expression or imitate style so specifically that it substitutes for the creator.
8. [AI] Compare patterns across channels, over time, and against existing Content Insights/Learnings before treating something as stable, novel, or materially changed.
9. [HYBRID] Persist only source-backed Observations/Content Insights and SourceProfile/checkpoint updates that future work would materially benefit from. Preserve semantic next-check/watch intent when useful, but do not represent it as an active schedule. If the research reveals a materially relevant non-content fact, use the appropriate organizational context or domain method directly rather than emitting or routing an AURA event.

## Verification
- Creator identity and cross-channel linkage are evidence-backed.
- Visible engagement/performance signals are labeled as proxies rather than proven business outcomes.
- Transferable mechanisms remain distinct from creator-specific expression.
- Saved watch/checkpoint state does not claim a recurring job exists unless an external runtime actually provides one.

## Completion Criteria
- The organization has the smallest useful current understanding of the creator/channel for the active content decision, with reusable evidence and patterns preserved only where future work benefits.
