---
id: content.intelligence.trending-content-discovery
type: workflow
owner_system: content-synthesis
reads:
- PlatformProfile
- Insight
- Learning
- SourceRecord
- Observation
writes:
- SourceRecord
- Observation
- Insight
context:
- AudienceSegment
- Brand
- Market
- Objective
---
# Trending Content Discovery

## Purpose
Identify genuinely emerging topics, formats, creative structures, and audience conversations worth studying without mistaking one viral post for a durable trend.

## Business Outcome
Give Content Synthesis current, evidence-backed creative opportunities and ideas before they become stale while avoiding copycat content and vanity-driven trend chasing.

## Run When
Use when the business needs current content opportunities, a platform/topic watch is due, or existing Content Insights are stale.

## Process
1. [HYBRID] Define the target audience, niche/adjacent niches, platforms, time window, desired outcome, and what “trending” must mean for this decision. Trend-scan planning knowledge may help when the discovery envelope is not already obvious.
2. [INTEGRATION] Retrieve rising/top content and creator/category signals with publish time, format, visible performance/context, account baseline where available, and source references.
3. [DETERMINISTIC] Normalize obvious age/account-size/repost effects where data supports it; draw on performance-normalization knowledge when useful, but do not require a separate stage. Separate repeated copies of the same trend from independent evidence.
4. [AI] Separate topic trend, format trend, hook pattern, narrative structure, visual device, creator-specific advantage, and distribution effect rather than collapsing them into “this content works.”
5. [AI] Identify candidate mechanisms explaining attention/engagement and record alternative explanations such as paid amplification, controversy, novelty, celebrity, or existing audience scale.
6. [HYBRID] Compare across multiple examples, adjacent niches, PlatformProfiles, and the business's own Content Learning to estimate relevance and transferability. Creative-pattern extraction may help when a candidate materially outperforms its contextual baseline.
7. [AI] Preserve scoped Content Insights for patterns/topics worth acting on; keep source examples but abstract the mechanism so future work remains original.
8. [AI] When a trend is weak or uncertain, use trend-validation operating knowledge if more evidence could materially change the decision. Do not create an internal route merely because another Workflow exists.
