---
id: customer.evidence-collection.public-conversation
type: playbook
version: 1.2.0
owner_system: customer-intelligence
risk: medium
autonomy_ceiling: 3
reads:
- SourceRecord
- Observation
- Insight
- ProofRecord
writes:
- SourceRecord
- Observation
- Asset
capabilities:
  required:
  - none
  optional:
  - social.listen
  - social.observe
  - public_comment.read
  - community.read
  - review.read
  - rss.read
  - webpage.snapshot
  - webpage.screenshot
events:
  consumes:
  - none
  emits:
  - customer.public-signal.observed
context:
- AudienceSegment
- Market
- ProductService
- Offer
---
# Public Conversation Collection

## Purpose
Collect public comments, discussions, reviews, and posts that reveal real customer or market experiences while preserving context, source, and privacy boundaries.

## Business Outcome
Expand customer understanding beyond formal surveys and interviews by capturing current public questions, praise, complaints, comparisons, use cases, and changing concerns.

## Run When
Run when public conversation can materially improve a current customer knowledge need, theme watch, proof search, or content/customer-response decision.

## Process
1. [HYBRID] Define the products, topics, brands, customer problems, markets, time window, and public surfaces to monitor; exclude private/restricted spaces and collection that violates policy or access terms.
2. [INTEGRATION] Retrieve allowed public posts/comments/reviews with permalink/source, timestamp, thread/context, public author label only when needed, and engagement/context signals that are actually available.
3. [INTEGRATION] Capture an original snapshot or screenshot when preservation matters and the surface permits it; store it as an Asset linked to the SourceRecord rather than treating the image as separate evidence.
4. [DETERMINISTIC] Remove exact duplicates, syndicated copies, obvious reposts, and repeated captures while preserving distinct people and materially different follow-up statements.
5. [AI] Extract direct questions, pains, desired outcomes, praise, complaints, objections, comparisons, use cases, before/after statements, feature requests, and exact language; keep direct statements separate from interpretation.
6. [AI] Classify aspect-level sentiment and intensity about the product/experience/topic, not personality or sensitive characteristics of the person posting.
7. [HYBRID] Mark potential ProofRecord candidates and foreign-domain signals such as competitor claims, industry events, journey friction, or content-response opportunities without creating foreign-domain Insights.
8. [DETERMINISTIC] Publish traceable SourceRecords/Observations and emit the public-signal event; route proof candidates to `customer.analysis.before-after-proof` or `core.intelligence.register-proof`.
