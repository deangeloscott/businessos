---
id: marketing.offer.bonuses
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
# Offer Bonus Design

## Purpose
Evaluate whether complementary additions can remove implementation barriers or accelerate value without cluttering the Offer.

## Business Outcome
Use bonuses only when they increase customer success or perceived value for the target buyer.

## Run When
Run when Offer diagnosis suggests an additional resource/service/access item could resolve a specific barrier.

## Process
1. [AI] Identify the customer barrier/outcome the bonus must improve and why the core Offer alone currently leaves the gap.
2. [AI] Generate additions that are complementary, low-confusion, and aligned with actual value realization rather than arbitrary “value stack” inflation.
3. [DETERMINISTIC] Estimate delivery cost/capacity, usage dependency, eligibility, and operational ownership.
4. [AI] Evaluate whether the bonus should instead be core scope, optional add-on, onboarding support, or content—not a bonus.
5. [HYBRID] Reject fake inflated monetary values or additions that reduce focus/customer fit.
6. [AI] Define exact proposed inclusion, target segment, rationale, and expected mechanism.
7. [DETERMINISTIC] Route Offer changes through ContextUpdateProposal/approval and measure adoption/conversion/customer outcome.
