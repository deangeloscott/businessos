---
id: content.intelligence.trending-content-discovery
type: playbook
version: 1.3.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
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
capabilities:
  required:
  - none
  optional:
  - creator_content.observe
  - social.observe
  - social.listen
  - rss.read
  - research.web.read
  - analytics.read
context:
- AudienceSegment
- Brand
- Market
- Objective
subcontracts:
  required:
  - content.intelligence.trend-scan-plan
  - content.intelligence.performance-normalization
  conditional:
  - id: content.intelligence.creative-pattern-extraction
    when: a candidate piece materially outperforms its contextual baseline
---
# Trending Content Discovery

## Purpose
Identify genuinely emerging topics, formats, creative structures, and audience conversations worth studying without mistaking one viral post for a durable trend.

## Business Outcome
Give Content Synthesis current, evidence-backed creative opportunities and ideas before they become stale while avoiding copycat content and vanity-driven trend chasing.

## Run When
Run when the business needs current content opportunities, a platform/topic watch is due, or existing Content Insights are stale.

## Process
1. [HYBRID] Define the target audience, niche/adjacent niches, platforms, time window, desired outcome, and what “trending” must mean for this decision.
2. [INTEGRATION] Retrieve rising/top content and creator/category signals with publish time, format, visible performance/context, account baseline where available, and source references.
3. [DETERMINISTIC] Normalize obvious age/account-size/repost effects where data supports it; separate repeated copies of the same trend from independent evidence.
4. [AI] Separate topic trend, format trend, hook pattern, narrative structure, visual device, creator-specific advantage, and distribution effect rather than collapsing them into “this content works.”
5. [AI] Identify candidate mechanisms explaining attention/engagement and record alternative explanations such as paid amplification, controversy, novelty, celebrity, or existing audience scale.
6. [HYBRID] Compare across multiple examples, adjacent niches, PlatformProfiles, and the business's own Content Learning to estimate relevance and transferability.
7. [AI] Publish scoped Content Insights for patterns/topics worth acting on; preserve source examples but abstract the mechanism so downstream work remains original.
8. [DETERMINISTIC] Route weak/uncertain trends to `content.intelligence.trend-validation` before creating a Content Opportunity.
