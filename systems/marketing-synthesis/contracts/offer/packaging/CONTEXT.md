---
id: marketing.offer.packaging
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
# Offer Packaging Design

## Purpose
Design how approved products/services/outcomes are bundled, tiered, scoped, and sequenced into an offer proposal.

## Business Outcome
Improve customer choice and perceived value while maintaining delivery quality and economics.

## Run When
Run when Offer diagnosis indicates packaging/tiering/scope is a material barrier or opportunity.

## Process
1. [AI] Map priority customer jobs/outcomes, natural usage/service bundles, capability dependencies, willingness/decision evidence, and delivery cost/constraints.
2. [AI] Define package/tier hypotheses with clear target customer, included/excluded scope, outcome, access/support, limits, and upgrade path.
3. [AI] Reduce unnecessary choice complexity and avoid artificial feature withholding that damages customer success.
4. [DETERMINISTIC] Model economic/operational implications and compare with current Offer/competitor context.
5. [HYBRID] Check that each tier can be delivered consistently and that names/differences are understandable.
6. [AI] Select the smallest package changes capable of testing the underlying hypothesis.
7. [DETERMINISTIC] Create ContextUpdateProposal with exact structural changes, rationale, guardrails, and measurement; do not edit Offer directly.
