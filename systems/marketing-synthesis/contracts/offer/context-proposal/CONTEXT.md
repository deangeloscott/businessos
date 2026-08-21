---
id: marketing.offer.context-proposal
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
# Offer Context Change Proposal

## Purpose
Package a Marketing-supported Offer change for controlled business review and canonical context update.

## Business Outcome
Allow Offer optimization without giving Marketing authority to silently change price, terms, guarantees, or deliverables.

## Run When
Run whenever Marketing recommends a structural change to canonical Offer truth.

## Process
1. [DETERMINISTIC] Resolve current Offer version and all supporting diagnosis, Customer/Competitor Insights, economics, operational constraints, and experiment evidence.
2. [AI] State the exact fields/terms proposed to change and the customer/business mechanism expected.
3. [AI] Identify what remains unchanged so the proposal is testable and implementation scope is clear.
4. [HYBRID] Document financial, delivery, legal/compliance, customer-quality, and migration implications.
5. [DETERMINISTIC] Define approval authority, effective date, rollback/reversion, instrumentation, and success/guardrail metrics.
6. [AI] Create ContextUpdateProposal linked to the originating Opportunity/Insight; do not alter Offer before approval.
7. [DETERMINISTIC] After approval, ensure downstream Marketing/Content/Sales-facing Assets are identified for update.
