---
id: marketing.strategy.guarantee-risk-reversal
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
# Guarantee and Risk-Reversal Design

## Purpose
Evaluate how legitimate risk reversal can reduce a real purchase barrier without creating unsustainable or deceptive commitments.

## Business Outcome
Improve qualified conversion where perceived risk is material while preserving economics, operational feasibility, and customer fit.

## Run When
Run when Customer/Marketing evidence shows risk is a meaningful barrier and the actual Offer can potentially be changed.

## Process
1. [AI] Identify the exact perceived risk: outcome, implementation, time, quality, fit, switching, financial, contractual, or effort.
2. [DETERMINISTIC] Resolve current Offer terms, economics, delivery variability, refund/cancellation policy, legal/compliance constraints, and ProofRecords.
3. [AI] Generate risk-reversal options that target the actual risk: trial, milestone, guarantee, conditional assurance, implementation commitment, cancellation flexibility, or other legitimate mechanism.
4. [AI] Model customer behavior/incentive effects, abuse risk, operational burden, financial downside, and qualification needs for each option.
5. [HYBRID] Reject guarantees that promise outcomes outside business control or conceal material conditions.
6. [AI] Recommend testable Offer changes with exact terms and evidence/rationale; do not mutate canonical Offer directly.
7. [DETERMINISTIC] Create ContextUpdateProposal for approved-business review and define post-change measurement/guardrails.
