---
id: marketing.offer.packaging
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
# Offer Packaging Design

## Purpose
Design candidate ways to bundle, tier, scope, or sequence established products/services/outcomes without treating a proposed package as current Offer truth.

## Business Outcome
Improve customer choice and perceived value while protecting delivery quality, customer success, and supported economics.

## Run When
Use when Offer evidence suggests packaging, tiering, or scope is a material barrier/opportunity or the organization explicitly wants to explore packaging alternatives.

## Process
1. [AI] Map the customer jobs/outcomes, natural usage/service bundles, real capability dependencies, decision evidence, and supported delivery/economic constraints that matter to packaging.
2. [AI] Define the smallest useful package/tier hypotheses with clear target customer, included/excluded scope, outcome, access/support, limits, and upgrade path. Do not invent capabilities or terms.
3. [AI] Reduce unnecessary choice complexity and avoid artificial feature withholding that damages customer success.
4. [AI] Assess economic/operational implications only from supported inputs and compare with current Offer/competitive context when useful. Keep unknown economics/capacity unknown rather than filling them with conventional assumptions.
5. [HYBRID] Check whether each candidate can actually be delivered consistently and whether names/differences are understandable from the customer's perspective.
6. [AI] Select the smallest package change or bounded comparison/test capable of informing the underlying hypothesis; do not redesign every dimension at once without a reason.
7. [AI] Keep candidate packaging distinct from current Offer truth. A real organization decision can update the Offer directly through supported context persistence. If an unresolved candidate is materially useful to retain, preserve it as Insight, Opportunity, Experiment, or Core ContextUpdateProposal according to its actual meaning rather than requiring a proposal/approval lifecycle.

## Verification
- Candidate packages do not invent unavailable scope, capabilities, economics, or customer outcomes.
- Current and proposed Offer structures are clearly distinguishable.
- No ContextUpdateProposal, Approval, WorkRequest, or experiment is created merely because packaging alternatives were designed.

## Completion Criteria
- The organization has a clear, evidence-aware packaging recommendation/hypothesis it can decide or test without AURA silently changing Offer truth or creating commercial approval machinery.
