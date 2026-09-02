---
id: marketing.offer.bonuses
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Insight
- Opportunity
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Offer Bonus Design

## Purpose
Evaluate whether a complementary addition could remove a supported implementation/value barrier or accelerate value without cluttering the Offer.

## Business Outcome
Use additions only when they plausibly improve customer success or perceived value for the relevant buyer, without fake value stacking or silently changing the active Offer.

## Run When
Use when Offer diagnosis/evidence suggests an additional resource, service, access item, or support element may solve a specific customer barrier.

## Process
1. [AI] Identify the customer barrier/outcome the addition must improve and why the current core Offer leaves that gap.
2. [AI] Generate only complementary, low-confusion candidates aligned with actual value realization rather than arbitrary “value stack” inflation.
3. [AI] Assess supported delivery cost/capacity, usage dependency, eligibility, operational ownership, and customer-success implications. Keep unsupported cost/capacity assumptions unknown.
4. [AI] Decide whether the candidate really belongs as core scope, optional add-on, onboarding/implementation support, content/resource, or a bonus; do not force the “bonus” label.
5. [AI] Reject fake inflated monetary values, artificial scarcity, or additions that reduce focus/customer fit.
6. [AI] Define the exact candidate inclusion, target segment, rationale, expected mechanism, material uncertainty, and useful measurement/test approach when warranted.
7. [AI] Keep the candidate distinct from current Offer truth. If the organization actually adopts the addition, update the Offer through the supported current-context path. If the unresolved candidate is worth retaining, persist it as Insight, Opportunity, Experiment, or Core ContextUpdateProposal according to its meaning; no proposal/approval lifecycle is required.

## Verification
- The addition addresses a supported barrier rather than manufacturing perceived value.
- Current and proposed Offer scope remain distinct.
- No ContextUpdateProposal, Approval, WorkRequest, or experiment is created merely because a candidate addition was evaluated.

## Completion Criteria
- The organization has an evidence-aware addition/bonus recommendation or hypothesis it can decide/test without AURA manufacturing commercial approval machinery.
