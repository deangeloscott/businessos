---
id: marketing.offer.guarantee
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
# Offer Guarantee Design

## Purpose
Design precise candidate risk-reversal/guarantee terms that the organization could actually administer without presenting a proposed promise as current business truth.

## Business Outcome
Evaluate a clear customer assurance with understandable conditions and bounded business exposure while avoiding unsupported guarantees or hidden complexity.

## Run When
Use when evidence indicates customer risk is a material barrier and a guarantee/risk-reversal approach may be a viable Offer change.

## Process
1. [AI] State the customer risk being addressed, the business-controlled promise under consideration, and the evidence that makes risk reversal relevant.
2. [AI] Define candidate eligibility, customer obligations, covered outcome/milestone, evidence required, timeframe, remedy, exclusions, request process, and operational owner only to the detail needed to evaluate the concept.
3. [HYBRID] Test ambiguity, abuse potential, applicable legal/compliance constraints, delivery variability, operational ability to adjudicate consistently, and customer-fairness implications.
4. [AI] Express the candidate terms in plain language that does not negate the headline promise through hidden complexity.
5. [AI] Estimate economic exposure only from supported inputs; distinguish known limits/scenarios from assumptions and keep unsupported expected/worst-case economics explicitly unknown.
6. [AI] Define how the guarantee could be presented without implying broader certainty, outcomes, or rights than the candidate terms actually support.
7. [AI] Keep the candidate guarantee distinct from current Offer/BusinessClaim truth. If the organization actually adopts it, persist the established terms/claim through the supported context/claim path. If the unresolved candidate itself is worth remembering, preserve it with the semantic object that actually fits (for example Insight, Opportunity, Experiment, or Core ContextUpdateProposal); no AURA approval lifecycle is required.

## Verification
- Candidate guarantee wording is not treated as an approved outward claim before the organization establishes it.
- Economic/operational/legal implications are supported or explicitly uncertain.
- No ContextUpdateProposal, Approval, WorkRequest, or experiment is created merely because guarantee design occurred.

## Completion Criteria
- The organization has a precise, evidence-aware candidate guarantee it can evaluate or test without AURA manufacturing approval authority or silently changing current Offer truth.
