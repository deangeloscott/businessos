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
- Insight
- Opportunity
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
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
- PreferenceProfile
---
# Offer Diagnosis

## Purpose
Determine whether weak commercial response is caused by the actual Offer structure rather than only its presentation, and identify the smallest evidence-backed structural improvement worth considering or testing.

## Business Outcome
Improve customer-perceived value and decision confidence without trying to solve structural value/risk issues with better copy or manufacturing artificial offer enhancers.

## Run When
Use when qualified prospects understand the Offer but repeatedly reject price, terms, scope, risk, packaging, commitment, effort, or time-to-value, or when the organization explicitly wants to evaluate its Offer structure.

## Process
1. [HYBRID] Reuse the current Offer, ProductService, economics, Customer/Competitor evidence, conversion/sales performance, refunds/churn, delivery constraints, established claims, Brand, and other context that materially bears on the decision. Exact retrieval is mechanical; deciding relevance/sufficiency is model judgment.
2. [AI] Diagnose the value exchange across the dimensions actually implicated by the evidence: desired customer outcome, confidence/proof, time-to-value/delay, customer effort/sacrifice, included scope, price/payment, commitment, risk, qualification, complexity, and switching/implementation friction. A named value equation may be a useful lens but is not a literal scoring formula or universal doctrine.
3. [AI] Distinguish presentation misunderstanding from a real structural Offer weakness and from a product/service/fit or operational problem that should be addressed differently.
4. [AI] Compare rejection patterns across relevant qualified/unqualified segments and successful/unsuccessful customers where evidence allows, so the Offer is not optimized for poor fit.
5. [AI] Consider legitimate structural options only when they address a supported barrier: risk reversal/guarantee, bonus, payment terms, packaging, naming, onboarding/implementation support, or another real value component. Never invent capacity, deadlines, savings, outcomes, refund terms, proof, scarcity, or arbitrary value stacks.
6. [AI] Account for actual operational, economic, legal/compliance, customer-success, and Brand constraints. A preferred marketing framework is a preference, not authorization or business truth.
7. [AI] Produce the narrowest useful Offer hypothesis/recommendation, expected mechanism, evidence basis, material uncertainty, and what would distinguish it from alternatives. Do not force an experiment or multi-variable redesign when the decision does not require one.
8. [AI] Keep a recommendation distinct from current Offer truth. If the user/organization explicitly makes a business decision, persist the resulting Offer/context through the supported current-truth path. If the change remains a hypothesis, preserve it as hypothesis/Insight/Opportunity/Experiment only when future work benefits. Use Core `ContextUpdateProposal` only when an unresolved candidate change to existing durable context is itself worth remembering; it is not a mandatory approval step.

## Verification
- Structural diagnosis is traceable to relevant customer/commercial/operational evidence rather than marketing convention.
- Proposed terms, guarantees, pricing, scarcity, or other commitments are not presented as current business truth until actually established.
- No ContextUpdateProposal, WorkRequest, approval object, or experiment is created merely because Offer diagnosis occurred.

## Completion Criteria
- The organization can distinguish the observed Offer problem, likely mechanism, recommended/hypothesized structural change, evidence/unknowns, and any real business decision without a duplicate Marketing approval lifecycle.
