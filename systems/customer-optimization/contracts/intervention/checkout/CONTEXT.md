---
id: customer-optimization.intervention.checkout
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes: []
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - checkout.read
  - checkout.update
  - billing.read
  - support.ticket.read
  - experiment.run
context:
- EconomicContext
- Offer
subcontracts:
  required:
  - customer-optimization.diagnosis.root-cause
  - customer-optimization.intervention.design
  conditional:
  - id: customer-optimization.checkout.payment-failure
    when: payment failure is a material mechanism
---
# Checkout Optimization

## Purpose
Reduce preventable purchase friction while preserving trust, economics, compliance, and order quality.

## Business Outcome
Improve healthy completed purchases by fixing real checkout friction without confusing Offer/persuasion problems with checkout mechanics.

## Run When
Use when checkout abandonment, payment failure, form/flow friction, or purchase-completion quality is a material issue. An existing Opportunity may provide context but is not required.

## Process
1. [HYBRID] Map the actual checkout steps, fields, payment methods, validation/errors, fees/taxes/shipping timing, coupons, authentication, device behavior, and observed failure reasons relevant to the decision.
2. [HYBRID] Quantify abandonment and technical/payment errors by useful stage/segment/device/source where evidence exists; do not assume all abandonment is a defect.
3. [AI] Identify supported or testable hypotheses such as surprise cost, uncertainty, effort, forced account creation, payment limitation, trust, performance, accessibility, or technical failure.
4. [AI] Separate checkout mechanics from Offer/price persuasion or broader journey problems and use the relevant operating knowledge directly rather than routing work between AURA domains.
5. [AI] Design the smallest useful intervention/test with revenue, fraud, support, margin, refund, accessibility, and customer-experience guardrails proportionate to the change.
6. [HYBRID] If implementation is requested and the host has real capability/permission, apply the checkout/payment change through the external system and verify controlled transactions or resulting state where practical. Otherwise return the actionable design without implying execution.
7. [HYBRID] Evaluate completed profitable purchases and downstream order/customer quality when evidence becomes available. Preserve durable change, experiment, measurement, outcome, or Learning records only when those meanings actually occur and matter later.

## Completion Criteria
- The checkout mechanism and proposed/executed improvement are evidence-bounded, external execution state is truthful, and no generic AURA lifecycle is required.
