---
id: customer.monitoring.public-signal-watch
type: detector
version: 1.2.0
owner_system: customer-intelligence
reads:
- Observation
- Insight
- SourceRecord
writes:
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - none
  optional:
  - social.listen
  - public_comment.read
  - community.read
  - review.read
  - rss.read
schedule:
  class: recurring
  default: daily
  configurable: true
events:
  consumes:
  - none
  emits:
  - customer.public-signal.observed
  - insight.updated
context:
- AudienceSegment
- ProductService
- Offer
- Market
---
# Public Customer Signal Watch

## Purpose
Continuously detect meaningful changes in public customer questions, praise, complaints, needs, and experience without treating every mention as important.

## Business Outcome
Surface emerging customer opportunities or risks early enough for the business to respond, learn, or create useful communication.

## Run When
Run on the configured monitoring cycle for approved public sources and active customer/product themes.

## Process
1. [DETERMINISTIC] Load the approved watch topics, products, markets, current Customer Insights, last checkpoint, and existing unresolved themes.
2. [INTEGRATION] Retrieve only new public comments/reviews/discussions since the checkpoint using allowed sources; do not monitor private spaces or individuals beyond an authorized customer relationship purpose.
3. [DETERMINISTIC] Deduplicate reposts/cross-posts and compare against prior captured signals so old conversation is not repeatedly treated as new evidence.
4. [AI] Extract meaningful new questions, pains, sentiment shifts, use cases, before/after evidence, objections, feature needs, and changing language.
5. [HYBRID] Evaluate whether the new evidence merely adds examples, materially strengthens/weakens an Insight, creates a new Customer Insight candidate, or warrants no action.
6. [HYBRID] Flag potential proof and content-response candidates and route foreign-domain signals to the canonical owner without creating duplicate Insights.
7. [DETERMINISTIC] Persist new SourceRecords/Observations, update monitoring checkpoint, update Customer Insights only when warranted, and emit events for downstream relevance evaluation.
