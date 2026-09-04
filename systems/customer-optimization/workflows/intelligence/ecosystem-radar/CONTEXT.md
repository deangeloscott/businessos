---
id: customer-optimization.intelligence.ecosystem-radar
type: workflow
owner_system: customer-optimization
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
- CustomerJourney
writes:
- Observation
- Insight
context:
- Business
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Customer Optimization Ecosystem Tactic Radar

## Purpose
Discover and evaluate external mechanisms for conversion, qualification, checkout, onboarding, activation, adoption, retention, renewal, repeat purchase, expansion, referral, and service recovery without turning outside tactics into automatic customer interventions.

## Business Outcome
Improve customer progression and value realization from credible external learning while protecting customer experience, fairness, actual business constraints, and causal interpretation.

## Run When
Use on demand for customer-journey refresh or when a material lifecycle/CRO practice or result could affect the active business.

## Process
1. [HYBRID] Reuse the active CustomerJourney, bottleneck diagnosis, instrumentation state, prior experiments/outcomes, Domain Learning, customer evidence, and SourceProfiles before external search.
2. [AI] Discover journey-intervention claims across primary experiments, product/growth research, case studies, communities, practitioner evidence, competitors, and adjacent industries only where they can inform the current journey question. Draw on Core source-discovery knowledge when it materially improves coverage or provenance.
3. [HYBRID] Use Core triangulation when useful to separate original tests from retellings and assess independent support/contradiction, sample/design quality, freshness, selection effects, metric quality, and commercial context. Do not require ceremonial triangulation where the evidence needed for the decision is already sufficient.
4. [AI] Map each credible tactic to a specific journey transition/friction mechanism and determine whether the active business actually has sufficiently similar customer state, constraints, instrumentation, capacity, and value proposition.
5. [AI] Consider customer harm, fairness, dark-pattern risk, applicable compliance/contract constraints, service capacity, reversibility, downstream retention/value, and whether a short-term conversion gain could damage longer-term outcomes.
6. [AI] Decide what the evidence warrants next: ignore, watch, investigate, experiment, adapt into a current intervention, revise Learning, or do nothing. `customer-optimization.experimentation.lifecycle-test` and other relevant Playbooks/Workflows are optional methods, not automatic routes.
7. [AI] Where active-business results exist, interpret them with guardrails and downstream value rather than only immediate progression; preserve segment differences and inconclusive outcomes.
8. [DETERMINISTIC] Persist only material Observation/Insight evidence and exact references selected by the model/user. Customer Optimization Learning changes only when outcome evidence and semantic judgment support reusable scoped guidance.

## Verification
- A conversion proxy cannot override observed customer harm or downstream-value evidence.
- External evidence never substitutes for active-business journey diagnosis or established business facts.
- No Opportunity, WorkRequest, experiment, or customer-facing change is created merely because the radar observed a tactic.

## Completion Criteria
- Material journey mechanisms are evidence-calibrated and scoped to active-business applicability, with any suggested next method left to capable model/user judgment.
