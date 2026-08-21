---
id: marketing.strategy.awareness
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 2
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- ActionPacket
- WorkRequest
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
Run when the audience awareness/sophistication level is material to a marketing message or asset.

## Process
1. [DETERMINISTIC] Resolve Customer Insights, acquisition/source context, prior touchpoints, Offer, search/content intent, and relevant campaign performance.
2. [AI] Determine awareness of problem, desired outcome, solution category, specific product/brand, and Offer separately rather than one blanket stage.
3. [AI] Assess category/message sophistication: what promises/mechanisms/claims the audience has likely encountered and become skeptical of.
4. [AI] Identify prerequisite beliefs/information that must exist before the desired action can feel reasonable.
5. [HYBRID] Segment or branch when materially different awareness states cannot be served by one persuasion path.
6. [AI] Define what to explain, prove, contrast, or omit for the target state.
7. [DETERMINISTIC] Record awareness assumptions/evidence and conditions that would require a different variant.
