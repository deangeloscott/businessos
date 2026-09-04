---
id: marketing.strategy.claim-validation
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Marketing Claim Validation

## Purpose
Verify that consequential marketing claims are true, appropriately scoped, current, and supported before outward use.

## Business Outcome
Prevent unsupported persuasion from creating customer, compliance, or reputational risk.

## Run When
Use before publishing material commercial claims or when evidence, Offer, product, or business facts change enough to make prior claims uncertain.

## Process
1. [AI] Extract every consequential factual, comparative, quantitative, outcome, scarcity, guarantee, certification, or customer-result claim from the final asset.
2. [HYBRID] Resolve canonical Business/Product/Offer facts, ProofRecords, SourceRecords, permissions, dates, and applicable policy constraints.
3. [AI] Match each claim to evidence and classify what the evidence supports, including population, timeframe, conditions, and attribution limits.
4. [AI] Narrow, qualify, replace, or remove claims that exceed evidence rather than seeking convenient weak support.
5. [HYBRID] Obtain real human/expert/legal review only when the claim or external rule actually requires it. AURA does not create a generic approval object or internal approval path.
6. [HYBRID] Verify the rendered/published wording—not only source copy—against the claim map when the final surface is available.
7. [HYBRID] Preserve the claim-check result and evidence refs in the relevant Asset or a VerificationRecord only when future work materially benefits from remembering them. Do not create a WorkRequest merely to move the result to another AURA method.
