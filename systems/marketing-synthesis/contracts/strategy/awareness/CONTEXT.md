---
id: marketing.strategy.awareness
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
  - cms.page.publish
  - email.send
  - social.ad.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Audience Awareness and Sophistication

## Purpose
Determine what the audience already knows/believes about the problem, solutions, brand, alternatives, and Offer.

## Business Outcome
Match persuasion depth and sequence to the audience’s real decision state rather than over-explaining or prematurely selling.

## Run When
Use when audience awareness/sophistication is material to a marketing message or asset. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [HYBRID] Resolve relevant Customer evidence, acquisition/source context, prior touchpoints, Offer, search/content intent, and campaign performance when available.
2. [AI] Determine awareness of problem, desired outcome, solution category, specific product/brand, and Offer separately rather than one blanket stage.
3. [AI] Assess category/message sophistication: what promises/mechanisms/claims the audience has likely encountered and become skeptical of.
4. [AI] Identify prerequisite beliefs/information that must exist before the desired action can feel reasonable.
5. [HYBRID] Segment or branch when materially different awareness states cannot be served by one persuasion path.
6. [AI] Define what to explain, prove, contrast, or omit for the target state.
7. [AI] Preserve the useful awareness assumptions, evidence, and variant conditions as a Marketing-owned strategy Asset when future work benefits from them. Do not create a WorkRequest merely because downstream messaging/content methods may use the result.
