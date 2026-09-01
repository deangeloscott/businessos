---
id: marketing.strategy.guarantee-risk-reversal
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
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
Use when Customer/Marketing evidence shows risk is a meaningful barrier and the actual Offer could potentially be changed.

## Process
1. [AI] Identify the exact perceived risk: outcome, implementation, time, quality, fit, switching, financial, contractual, or effort.
2. [HYBRID] Resolve current Offer terms, economics, delivery variability, refund/cancellation policy, applicable legal/compliance constraints, and ProofRecords.
3. [AI] Generate risk-reversal options that target the actual risk: trial, milestone, guarantee, conditional assurance, implementation commitment, cancellation flexibility, or another legitimate mechanism.
4. [AI] Evaluate customer behavior/incentive effects, abuse risk, operational burden, financial downside, and qualification needs for each option using actual evidence where available.
5. [HYBRID] Reject guarantees that promise outcomes outside business control or conceal material conditions.
6. [AI] Recommend the narrowest credible option with exact proposed terms, evidence/rationale, material uncertainty, and useful measurement/guardrails when warranted. Keep it explicitly proposed rather than current Offer truth.
7. [AI] Preserve the recommendation as a Marketing-owned strategy Asset when useful. If the organization actually adopts the new guarantee/risk-reversal terms, update canonical Offer truth through the normal current-context path with provenance. If not adopted, keep the idea clearly candidate; do not manufacture a ContextUpdateProposal, approval object, WorkRequest, or Experiment merely because the option was evaluated.
