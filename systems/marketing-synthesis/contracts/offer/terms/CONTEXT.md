---
id: marketing.offer.terms
type: playbook
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
capabilities:
  required:
  - none
  optional:
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Offer Terms Optimization

## Purpose
Evaluate whether commitment, payment, cancellation, trial, eligibility, or contractual terms are blocking otherwise-qualified customers and design the narrowest credible alternative.

## Business Outcome
Reduce unnecessary commercial friction without shifting unacceptable risk to the business or customer or pretending proposed terms are already active.

## Run When
Use when customer/win-loss evidence indicates Offer terms materially affect purchase decisions or the organization explicitly wants to evaluate those terms.

## Process
1. [AI] Identify the exact term creating friction and which qualified segment/decision it affects.
2. [HYBRID] Reuse the current contract/payment/cancellation/trial/eligibility terms, economics, operational constraints, applicable legal/compliance requirements, and relevant failure/abuse history. Exact retrieval is mechanical; relevance and implications require model/human judgment.
3. [AI] Generate the smallest alternative terms that address the supported friction while holding unrelated Offer dimensions constant where practical.
4. [AI] Evaluate customer value, business risk, cash flow, delivery, churn/refund, adverse-selection, and clarity implications using actual evidence where available. Keep unknown economics unknown.
5. [AI] Reject terms that obscure obligations, trap customers, create unsupported promises, or impose commitments the business cannot honor.
6. [AI] State the proposed change, affected segment/eligibility, rationale, expected mechanism, material uncertainty, and useful measurement/test approach when one is warranted.
7. [AI] Keep proposed terms distinct from current Offer truth. If the organization actually decides to adopt them, update the Offer through the supported current-context path. If they remain an unresolved candidate and remembering that candidate materially helps future work, a Core `ContextUpdateProposal`, Insight, Opportunity, or Experiment may be appropriate according to its real meaning; none is a mandatory approval step.

## Verification
- Current terms and proposed terms are clearly distinguished.
- Economic/legal/operational implications are evidence-based or explicitly unknown.
- No ContextUpdateProposal, approval object, WorkRequest, or experiment is created merely because terms were evaluated.

## Completion Criteria
- The organization has a defensible terms recommendation/hypothesis and enough context to decide or test it without AURA manufacturing a commercial approval lifecycle.
