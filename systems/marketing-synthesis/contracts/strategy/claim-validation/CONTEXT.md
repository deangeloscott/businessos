---
id: marketing.strategy.claim-validation
type: playbook
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
# Marketing Claim Validation

## Purpose
Verify that consequential marketing claims are true, appropriately scoped, current, and supported before publication.

## Business Outcome
Prevent unsupported persuasion from creating customer, compliance, or reputational risk.

## Run When
Run before publishing material commercial claims or when evidence/Offer/product facts change.

## Process
1. [AI] Extract every consequential factual, comparative, quantitative, outcome, scarcity, guarantee, certification, or customer-result claim from the final asset.
2. [DETERMINISTIC] Resolve canonical Business/Product/Offer facts, ProofRecords, SourceRecords, permissions, dates, and applicable policy constraints.
3. [AI] Match each claim to evidence and classify what the evidence supports, including population, timeframe, conditions, and attribution limits.
4. [AI] Narrow, qualify, replace, or remove claims that exceed evidence rather than seeking convenient weak support.
5. [HYBRID] Route high-stakes regulated/legal interpretations to the appropriate human/expert approval path.
6. [DETERMINISTIC] Verify the rendered/published wording—not only source copy—against the claim map.
7. [DETERMINISTIC] Store claim-check result and evidence refs with the Asset/verification record.
