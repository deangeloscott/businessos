---
id: content.opportunity.signal-to-content
type: playbook
version: 1.2.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- Observation
- Insight
- ProofRecord
- IndustryEvent
- Opportunity
- WorkRequest
- Asset
writes:
- Insight
- Opportunity
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - customer.public-signal.observed
  - insight.activated
  - insight.updated
  - industry.audience-implication.updated
  emits:
  - content.opportunity.evaluated
context:
- AudienceSegment
- Brand
- Objective
- ProductService
- Offer
---
# Signal to Content Opportunity

## Purpose
Evaluate whether a customer comment, proof item, Industry Insight, competitor/search signal, trend, or other canonical intelligence should become useful content—and what kind of content response is justified.

## Business Outcome
Turn valuable organizational signals into timely, audience-relevant content without creating duplicate Opportunities or producing content merely because a topic exists.

## Run When
Run when new intelligence or proof has plausible communication value and no existing Content WorkRequest already defines the required production job.

## Process
1. [DETERMINISTIC] Resolve the originating signal, its semantic owner, source/proof restrictions, business Objective, affected audience, existing Opportunities/WorkRequests, and freshness/timeliness.
2. [DETERMINISTIC] If an existing WorkRequest or foreign-domain Opportunity already requires Content execution, attach the signal as evidence and route to the requested Content workflow; do not create a duplicate Content Opportunity.
3. [AI] Identify the audience value the signal could create: answer a question, respond to concern, demonstrate, teach, compare, show proof, explain news, provide a use case, correct a misconception, or develop a timely point of view.
4. [AI] Generate candidate content responses and distinguish reactive one-off response from reusable evergreen content, series, demonstration, case story, infographic, carousel, video, audio, or platform-native post.
5. [HYBRID] Evaluate evidence quality, timeliness, audience relevance, differentiation, brand fit, proof/permission constraints, expected value, and whether doing nothing is better.
6. [DETERMINISTIC] Search existing Assets/Content Opportunities for the same communication intervention and update/reuse when appropriate.
7. [HYBRID] Create a Content Insight and candidate Content Opportunity only when content itself is an independent valuable intervention; otherwise return the signal to the existing delegated work path.
8. [DETERMINISTIC] Route qualified work to angle/format/platform planning with the original signal and lineage intact.
