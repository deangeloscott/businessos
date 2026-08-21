---
id: content.intelligence.creator-monitoring
type: detector
version: 1.2.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- SourceRecord
- Observation
- Insight
- Learning
- PlatformProfile
writes:
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - none
  optional:
  - creator_content.observe
  - social.observe
  - rss.read
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
Monitor selected creators in similar and dissimilar niches for new content mechanisms, topics, and format shifts that can inform original business content.

## Business Outcome
Continuously learn from strong public creative execution without copying creator-specific expression or confusing popularity with transferable effectiveness.

## Run When
Run on the configured creator-watch cycle or when a creator/category is added because it is strategically useful to study.

## Process
1. [DETERMINISTIC] Load the approved creator/watch set, last checkpoint, target platforms, and the reason each creator is relevant.
2. [INTEGRATION] Retrieve new public content since the checkpoint with source, format, date, visible context/performance signals, and relevant surrounding posts when comparison is needed.
3. [DETERMINISTIC] Identify unusually strong or novel items relative to each creator's own recent baseline where enough data exists.
4. [AI] Decompose candidate content into topic, hook, structure, pacing, proof, visual device, interaction, payoff, CTA, and distribution context.
5. [AI] Separate creator-specific advantages from patterns that could plausibly transfer to another brand/audience.
6. [HYBRID] Compare patterns across creators and against existing Content Insights/Learnings before calling something new.
7. [DETERMINISTIC] Publish source-backed Observations/Content Insights and update the checkpoint; route mechanisms needing stronger evidence to trend validation or pattern extraction.
