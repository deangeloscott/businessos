---
id: content.opportunity.signal-to-content
type: playbook
owner_system: content-synthesis
reads:
- Observation
- Insight
- ProofRecord
- IndustryEvent
- Opportunity
- Asset
writes:
- Insight
- Opportunity
capabilities:
  required:
  - none
  optional:
  - none
context:
- AudienceSegment
- Brand
- Objective
- ProductService
- Offer
---
# Signal to Content Opportunity

## Purpose
Judge whether a real organizational signal creates a worthwhile communication opportunity for a specific audience, and if so what kind of content response is justified.

## Business Outcome
Turn useful customer, proof, industry, competitor, search, trend, or other evidence into timely audience value without producing content merely because a topic exists.

## Run When
Use when a current Observation, Insight, ProofRecord, IndustryEvent, measured pattern, or other durable signal may materially improve audience communication and the value of a content response is not already obvious.

## Process
1. [HYBRID] Reuse the originating signal/evidence, current business Objective, affected audience, Brand/Offer context, relevant existing Assets/Opportunities, freshness, and any rights/proof/claim constraints that could change the decision.
2. [AI] Identify the audience value the signal could create: answer a question, respond to a concern, demonstrate, teach, compare, show proof, explain a development, provide a use case, correct a misconception, or express a useful point of view.
3. [AI] Generate the smallest useful response options and distinguish a reactive one-off from evergreen content, a reusable series, demonstration, case story, infographic, carousel, video, audio, platform-native post, or no content at all.
4. [AI] Evaluate evidence quality, timeliness, audience relevance, differentiation, Brand fit, rights/permission constraints, expected business/audience value, opportunity cost, and whether doing nothing is better.
5. [HYBRID] Reuse or extend an existing Asset/Opportunity when it represents the same real communication need. Exact IDs/refs may be matched deterministically; semantic duplication is model judgment.
6. [AI] Create/update a scoped Content Insight only when a durable interpretation about communication value will help future work. Create a Content Opportunity only when content itself is a distinct valuable intervention worth remembering; neither object is required simply to continue producing content in the current task.
7. [AI] If content is warranted, continue directly with the useful brief/strategy/production method. The active model/user chooses format, sequencing, and method; no WorkRequest, foreign-domain return path, or routing event is required.

## Verification
- The source signal remains distinguishable from the content interpretation built from it.
- A timely topic is not treated as automatically valuable content.
- Proof/claims/rights are preserved at the scope supported by evidence.
- Opportunity creation reflects a genuinely distinct durable intervention, not an internal routing step.

## Completion Criteria
- The model/user can decide whether content is worth doing, why, for whom, and what response class is most useful, with any durable Insight/Opportunity preserved only when future work benefits.
