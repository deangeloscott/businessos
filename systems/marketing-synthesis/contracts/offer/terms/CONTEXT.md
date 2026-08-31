---
id: marketing.offer.terms
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
# Offer Terms Optimization

## Purpose
Evaluate whether commitment, payment, cancellation, trial, eligibility, or contractual terms are blocking otherwise-qualified customers.

## Business Outcome
Reduce unnecessary commercial friction without shifting unacceptable risk to the business or customer.

## Run When
Run when customer/win-loss evidence indicates Offer terms materially affect purchase decisions.

## Process
1. [AI] Identify the exact term creating friction and which qualified segment/decision it affects.
2. [DETERMINISTIC] Resolve current contract/payment/cancellation/trial/eligibility terms, economics, operational constraints, legal/compliance, and failure/abuse history.
3. [AI] Generate alternative terms that target the friction while holding unrelated Offer dimensions constant where practical.
4. [AI] Evaluate customer value, business risk, cash flow, delivery, churn/refund, and adverse-selection implications.
5. [HYBRID] Do not recommend terms that obscure obligations, trap customers, or create commitments the business cannot honor.
6. [AI] Define testable change, eligibility/guardrails, and expected mechanism.
7. [DETERMINISTIC] Create ContextUpdateProposal/approval path and measurement plan.
