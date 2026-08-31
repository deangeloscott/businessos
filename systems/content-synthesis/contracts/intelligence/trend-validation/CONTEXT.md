---
id: content.intelligence.trend-validation
type: playbook
version: 1.2.0
owner_system: content-synthesis
reads:
- SourceRecord
- Observation
- Insight
- PlatformProfile
writes:
- Observation
- Insight
capabilities:
  required:
  - none
  optional:
  - creator_content.observe
  - social.observe
  - social.listen
  - analytics.read
context:
- AudienceSegment
- Market
---
# Content Trend Validation

## Purpose
Determine whether a suspected content trend is a real, relevant pattern or an isolated viral/outlier event before the business invests in it.

## Business Outcome
Capture useful trends early while reducing wasted content caused by imitation, survivorship bias, paid amplification, or temporary platform noise.

## Run When
Run when trending-content or creator monitoring produces a promising but uncertain topic, format, hook, or creative mechanism.

## Process
1. [DETERMINISTIC] Define the candidate trend precisely and specify what evidence would count as replication across creators, posts, platforms, time, or the business's own data.
2. [INTEGRATION] Gather additional examples and counterexamples across an appropriate window; capture visible account scale, publish timing, paid/boosted status when known, and source context.
3. [DETERMINISTIC] Remove duplicate/repost effects and compare against creator/category baselines where available so raw views do not substitute for relative performance.
4. [AI] Test whether the repeated element is the topic, format, hook, structure, visual mechanic, event timing, creator identity, or distribution condition.
5. [AI] Generate plausible alternative explanations and evidence that would falsify the trend hypothesis.
6. [HYBRID] Rate confidence, expected lifespan, audience relevance, originality risk, platform dependence, and whether immediate experimentation is justified despite uncertainty.
7. [HYBRID] Update/contradict the Content Insight and route only sufficiently relevant trends to pattern transfer or Content Opportunity evaluation.
