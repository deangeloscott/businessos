---
id: customer-optimization.intelligence.ecosystem-radar
type: playbook
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
- Opportunity
- WorkRequest
capabilities:
  required:
  - research.web.read
  optional:
  - analytics.read
  - product_analytics.read
  - conversion.read
  - checkout.read
  - customer_success.read
  - community.read
context:
- Business
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  conditional:
  - id: customer-optimization.intelligence.relevance-evaluation
    when: External evidence must be mapped to an active journey mechanism.
  - id: customer-optimization.experimentation.lifecycle-test
    when: A promising journey intervention is testable and safe enough for bounded exposure.
  - id: customer-optimization.learning.domain-learning
    when: Verified outcomes justify reusable lifecycle guidance.
---
# Customer Optimization Ecosystem Tactic Radar

## Purpose
Discover and evaluate external tactics for conversion, qualification, checkout, onboarding, activation, adoption, retention, renewal, repeat purchase, expansion, referral, and service recovery before testing them on customers.

## Business Outcome
Improve customer progression and value realization from credible external learning while protecting customer experience, fairness, business guardrails, and causal interpretation.

## Run When
Run from the Core ecosystem radar, on demand for customer-journey refresh, or when a material lifecycle/CRO practice or result appears.

## Process
1. [HYBRID] Reuse the active CustomerJourney, bottleneck diagnosis, instrumentation health, prior experiments, domain Learnings, customer evidence, and SourceProfiles before external search.
2. [AI] Discover journey intervention claims across primary experiments, product/growth research, case studies, communities, practitioner evidence, competitors, and adjacent industries using mechanism-centered semantic discovery.
3. [HYBRID] Use Core triangulation to separate original tests from retellings and assess independent support/contradiction, sample/design quality, freshness, selection effects, metric quality, and commercial context.
4. [AI] Map each credible tactic to a specific journey transition/friction mechanism and determine whether the active business has the same customer state, constraints, instrumentation, capacity, and value proposition.
5. [HYBRID] Evaluate customer harm, fairness, dark-pattern risk, compliance, service capacity, reversibility, downstream retention/value, and whether a short-term conversion gain could damage longer-term outcomes.
6. [HYBRID] Route weak/noisy claims to ignore/watch, knowledge gaps to investigation, and promising low-enough-risk interventions to `customer-optimization.experimentation.lifecycle-test`.
7. [AI] Interpret active-business results with guardrails and downstream value, not only immediate progression; classify support, contradiction, or inconclusive without masking segment differences.
8. [DETERMINISTIC] Update customer-optimization domain Learning only when outcome evidence supports reusable scoped guidance and preserve harmful/null interventions for future avoidance.

## Verification
- A conversion proxy cannot override customer harm or downstream-value guardrails.
- External evidence never substitutes for active-business journey diagnosis.

## Completion Criteria
- Material journey tactics have evidence, active-business applicability, customer-risk status, and an owned disposition/test/learning route.
