---
id: industry.monitoring.social-discussion
type: detector
version: 1.2.0
owner_system: industry-intelligence
reads:
- IndustryEvent
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- IndustryEvent
capabilities:
  required:
  - none
  optional:
  - social.listen
  - social.observe
  - public_comment.read
  - community.read
  - rss.read
  - news.read
schedule:
  class: recurring
  default: daily
  configurable: true
context:
- Market
- ProductService
---
# Industry Social Discussion Monitoring

## Purpose
Detect meaningful category/industry discussion emerging across public social, communities, and feeds while filtering memes, isolated virality, and repeated copies of the same story.

## Business Outcome
Surface changing narratives, questions, risks, and opportunities early enough for Industry Intelligence to verify them and determine whether they matter to the business.

## Run When
Run on the configured monitoring cycle for priority industry topics, markets, technologies, regulations, and category narratives.

## Process
1. [DETERMINISTIC] Load approved watch topics, markets, prior IndustryEvents, known narratives, last checkpoint, and priority public sources.
2. [INTEGRATION] Retrieve new public discussions/feed items since the checkpoint with source, timestamp, thread/context, and visible spread/engagement indicators where available.
3. [DETERMINISTIC] Cluster reposts, copied headlines, syndication, and repeated discussion of the same development so apparent volume is not mistaken for independent evidence.
4. [AI] Identify candidate developments, changing narratives, questions, concerns, claims, and emerging terminology while separating observed discussion from factual truth.
5. [HYBRID] Cross-check material factual claims against stronger/primary sources before updating an IndustryEvent; unresolved social claims remain Observations/hypotheses.
6. [AI] Determine whether the signal belongs to an existing Event, indicates a new Event candidate, or is merely conversation without a material external development.
7. [DETERMINISTIC] Persist SourceRecords/Observations/Event updates and route potentially material Events to verification/materiality rather than directly creating content.
