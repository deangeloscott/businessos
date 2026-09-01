---
id: content.intelligence.ecosystem-radar
type: playbook
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
---
# Content Ecosystem Radar

## Purpose
Discover emerging content formats, distribution behaviors, creator patterns, platform mechanics, and communication tactics, then determine what mechanisms are actually supported and transferable.

## Business Outcome
Help the business adapt content earlier and more intelligently without copying creators, chasing every trend, or treating engagement as business value.

## Run When
Use on demand for content intelligence or when platform/creator/content behavior may have materially changed.

## Process
1. [HYBRID] Reuse existing trend scans, creator monitoring, content-performance evidence, Domain Learning, and SourceProfiles before searching again.
2. [AI] Discover the formats, hooks, structures, pacing, visual/audio patterns, distribution mechanics, creator behaviors, topic packaging, or cross-niche mechanisms that could materially inform the current content decision.
3. [HYBRID] Preserve representative source evidence and use Core triangulation plus trend validation when useful to distinguish one viral item, repeated imitation, sustained multi-source adoption, platform change, and measured owned-content response.
4. [AI] Separate transferable mechanism from protected expression or creator identity. Creative-pattern extraction may help when the abstraction matters; do not turn imitation into a routed tactic.
5. [AI] Evaluate freshness and applicability by platform, audience, account state, Objective, format, production context, distribution conditions, and whether the observed outcome is attention, qualified action, or business value.
6. [AI] Decide what the evidence warrants next: ignore, watch, investigate, try a bounded owned-content hypothesis, use the mechanism in production, revise Learning, or do nothing. Relevant Content playbooks are optional methods, not automatic destinations.
7. [AI] Where owned outcomes exist, compare them against distribution, trend/timing, paid amplification, topic demand, account growth, and plausible alternatives before attributing effect to format/creative.
8. [DETERMINISTIC] Persist only material Observation/Insight evidence and exact references selected by the model/user. Content Learning changes only when semantic judgment and outcome evidence support reusable scoped guidance.

## Verification
- Popularity, novelty, mechanism plausibility, and business effectiveness remain separate dimensions.
- Pattern transfer never authorizes copying source expression.
- No Opportunity/WorkRequest or production route is created merely because a trend/mechanism was observed.

## Completion Criteria
- Material content discoveries have traceable evidence, a scoped mechanism/applicability interpretation, and any suggested next method remains model/user judgment rather than AURA routing state.
