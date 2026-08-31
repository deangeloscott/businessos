---
id: content.intelligence.ecosystem-radar
type: playbook
version: 1.0.0
owner_system: content-synthesis
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
- Asset
writes:
- Observation
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - research.web.read
  optional:
  - creator_content.observe
  - social.observe
  - social.listen
  - community.read
  - analytics.read
  - marketing.performance.read
context:
- Business
- Brand
- AudienceSegment
- Market
- Objective
subcontracts:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  conditional:
  - id: content.intelligence.trending-content-discovery
    when: Current unusually strong/trending content needs discovery.
  - id: content.intelligence.creator-monitoring
    when: Creator behavior over time is decision-relevant.
  - id: content.intelligence.trend-validation
    when: A suspected content trend needs validation beyond attention.
  - id: content.intelligence.creative-pattern-extraction
    when: A reusable mechanism should be abstracted without copying protected expression.
  - id: content.learning.domain-learning
    when: Owned-content outcomes justify reusable content guidance.
---
# Content Ecosystem Radar

## Purpose
Discover emerging content formats, distribution behaviors, creator patterns, platform mechanics, and communication tactics, then distinguish fleeting attention from reusable content mechanisms.

## Business Outcome
Help the business adapt content earlier and more intelligently without copying creators, chasing every trend, or treating engagement as business value.

## Run When
Run from the Core ecosystem radar, on demand for content intelligence, or when platform/creator/content behavior may have materially changed.

## Process
1. [HYBRID] Reuse existing trend scans, creator monitoring, content-performance Insights, domain Learnings, and SourceProfiles before searching again.
2. [AI] Discover emerging formats, hooks, structures, pacing, visual/audio patterns, distribution mechanics, creator behaviors, topic packaging, and cross-niche mechanisms through known and open semantic discovery.
3. [HYBRID] Preserve representative source evidence and use Core triangulation plus existing trend validation to distinguish one viral item, repeated imitation, sustained multi-source adoption, platform change, and measured owned-content response.
4. [AI] Separate the transferable mechanism from protected expression or creator identity; use creative-pattern extraction and never route copying as a tactic.
5. [HYBRID] Evaluate freshness and applicability by platform, audience, account state, objective, format, production capability, distribution context, and whether the observed outcome is engagement, qualified action, or business value.
6. [HYBRID] Route low-confidence novelty to watch, promising communication mechanisms to a bounded owned-content test/Opportunity, and verified platform mechanics to relevant content strategy/production contracts.
7. [AI] Compare owned outcomes against distribution, trend/timing, paid amplification, topic demand, and account growth before attributing effect to format or creative.
8. [DETERMINISTIC] Update Content Learning only after outcome evidence supports repeatable context-specific guidance and retain negative/null tests.

## Verification
- Popularity, novelty, and business effectiveness are separate dimensions.
- Pattern transfer never authorizes copying source expression.

## Completion Criteria
- Material content discoveries have a mechanism, freshness/applicability assessment, evidence status, and owned next route.
