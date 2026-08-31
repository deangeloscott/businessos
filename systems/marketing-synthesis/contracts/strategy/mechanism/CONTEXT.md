---
id: marketing.strategy.mechanism
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
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
# Persuasion Mechanism Explanation

## Purpose
Develop the credible explanation for how the product/service/approach creates the promised outcome and why alternatives may fail.

## Business Outcome
Increase belief by connecting the Offer to an understandable, supportable mechanism rather than relying on unsupported benefit claims.

## Run When
Run when prospects need to understand why the solution works, is different, or is likely to produce the desired result.

## Process
1. [AI] Resolve ProductService facts, Customer desired outcomes/problems, current mechanism claims, proof, and competitive alternatives.
2. [AI] Describe the actual causal/functional process from input/action to intermediate effect to customer outcome at the level the audience needs.
3. [AI] Separate established facts, business interpretation, and hypothesis; do not invent proprietary science or causal certainty.
4. [AI] Identify why common alternatives/status quo fail or trade off under the same customer conditions, using evidence rather than strawmen.
5. [HYBRID] Simplify technical detail without changing meaning and flag regulated/scientific/financial/medical claims for appropriate review.
6. [AI] Connect proof/examples/demonstration to each critical belief in the mechanism.
7. [DETERMINISTIC] Produce reusable mechanism language/diagram brief with claim→evidence links.
