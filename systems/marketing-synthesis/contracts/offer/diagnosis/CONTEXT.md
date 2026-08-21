---
id: marketing.offer.diagnosis
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
# Offer Diagnosis

## Purpose
Determine whether weak commercial response is caused by the actual Offer structure rather than only its presentation.

## Business Outcome
Identify evidence-backed Offer problems before trying to solve structural value/risk issues with better copy.

## Run When
Run when qualified prospects understand the offer but repeatedly reject price, terms, scope, risk, packaging, or commitment.

## Process
1. [DETERMINISTIC] Resolve canonical Offer, ProductService, economics, Customer Insights, win/loss evidence, competitor offers, conversion/sales performance, refunds/churn, and delivery constraints.
2. [AI] Diagnose perceived value, outcome specificity, included scope, price/payment, commitment, risk, time-to-value, guarantees, bonuses, qualification, and complexity separately.
3. [AI] Distinguish presentation misunderstanding from a real structural Offer weakness.
4. [AI] Compare rejection patterns across qualified/unqualified segments and successful/unsuccessful customers to avoid optimizing for poor fit.
5. [HYBRID] Identify operational/economic/legal constraints that make certain changes infeasible or harmful.
6. [AI] Create prioritized Offer hypotheses and expected mechanism for each; avoid changing many dimensions simultaneously without reason.
7. [DETERMINISTIC] Route structural changes through ContextUpdateProposal/business approval and define experiment/guardrails.
