---
id: marketing.offer.diagnosis
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
- PreferenceProfile
---
# Offer Diagnosis

## Purpose
Determine whether weak commercial response is caused by the actual Offer structure rather than only its presentation, and identify the smallest evidence-backed structural improvement worth testing.

## Business Outcome
Improve customer-perceived value and decision confidence without trying to solve structural value/risk issues with better copy or manufacturing artificial offer enhancers.

## Run When
Run when qualified prospects understand the offer but repeatedly reject price, terms, scope, risk, packaging, commitment, effort, or time-to-value.

## Process
1. [DETERMINISTIC] Resolve canonical Offer, ProductService, economics, Customer Insights, win/loss evidence, competitor offers, conversion/sales performance, refunds/churn, delivery constraints, approved claims, and applicable Brand/operator marketing doctrine.
2. [AI] Diagnose the value exchange across distinct dimensions: desired customer outcome, perceived confidence/likelihood given available proof, time-to-value/delay, customer effort/sacrifice, included scope, price/payment, commitment, risk, qualification, complexity, and switching/implementation friction. A named value equation may be a useful lens but is not a literal scoring formula or universal doctrine.
3. [AI] Distinguish presentation misunderstanding from a real structural Offer weakness and from a product/service/fit problem owned elsewhere.
4. [AI] Compare rejection patterns across qualified/unqualified segments, awareness/journey context, and successful/unsuccessful customers to avoid optimizing for poor fit.
5. [AI] Consider legitimate enhancers only when they solve a supported barrier: risk reversal/guarantee, bonus, payment terms, naming, urgency, scarcity, onboarding/implementation support, or another real value component. Never invent capacity, deadlines, savings, outcomes, refund terms, proof, or arbitrary value stacks.
6. [HYBRID] Identify operational/economic/legal/customer-success constraints that make certain changes infeasible or harmful. A preferred marketing framework is a preference, not authorization to alter Offer terms.
7. [AI] Create prioritized Offer hypotheses with the expected mechanism and evidence needed for each; avoid changing many dimensions simultaneously without reason.
8. [DETERMINISTIC] Route structural Offer changes through ContextUpdateProposal/business approval and define experiment/guardrails before treating the proposed Offer as active truth.
