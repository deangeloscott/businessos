---
id: customer-optimization.referral.eligibility-timing
type: playbook
version: 1.3.0
owner_system: customer-optimization
risk: medium
autonomy_ceiling: 2
reads:
- CustomerJourney
- Observation
- Insight
- Opportunity
- MetricObservation
- Experiment
writes:
- Observation
- Insight
- Opportunity
- ActionPacket
capabilities:
  required:
  - analytics.read
  optional:
  - product_analytics.read
  - crm.contact.read
  - crm.opportunity.read
  - checkout.read
  - billing.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - experiment.run
  - workflow.update
  - email.send
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Referral Eligibility and Timing

## Purpose
Identify appropriate moments to ask satisfied customers for a referral, review, or advocacy action.

## Business Outcome
Generate advocacy from demonstrated value and genuine satisfaction without coercion or indiscriminate asks.

## Run When
Run when referral/review/advocacy is part of the customer journey.

## Process
1. [DETERMINISTIC] Resolve verified value milestone, satisfaction/complaint state, tenure/context, prior ask history, consent/preferences, and applicable incentive/review rules.
2. [AI] Identify natural advocacy moments such as achieved result, resolved success milestone, unsolicited praise, renewal, or completed successful project—not simply a fixed number of days.
3. [AI] Match the ask type to context: private referral, public review, testimonial/case participation, introduction, community contribution, or no ask.
4. [HYBRID] Do not condition support/service on advocacy, pressure dissatisfied customers, or manipulate public-review gating.
5. [AI] Make the request easy, transparent, and optional; disclose incentives where required.
6. [DETERMINISTIC] Suppress repeated asks and record outcome/permission for any resulting ProofRecord.
7. [AI] Evaluate advocacy quality/customer sentiment and adjust timing rules.
