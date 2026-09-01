---
id: customer-optimization.intervention.referral
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
  - crm.contact.read
  - customer_success.read
  - email.send
  - workflow.update
  - experiment.run
context:
- EconomicContext
- Offer
subcontracts:
  required:
  - customer-optimization.referral.eligibility-timing
---
# Referral Optimization

## Purpose
Make it easy and appropriate for successful customers to recommend the business when genuine value exists.

## Business Outcome
Generate healthy advocacy and referred-customer value without pressuring customers or treating referral volume as the only outcome.

## Run When
Use when referral/advocacy is a meaningful growth or customer-value opportunity and the organization has enough evidence to design an appropriate mechanism.

## Process
1. [HYBRID] Define customer success/eligibility conditions so asks occur around genuine value rather than arbitrary dates or indiscriminate outreach.
2. [HYBRID] Analyze current referral sources, timing, friction, incentives where relevant/allowed, referred-customer quality, and customer experience.
3. [AI] Identify natural advocacy moments such as an achieved outcome, explicit praise, renewal, milestone, support recovery, event/community interaction, or another evidence-backed value moment.
4. [AI] Design the smallest low-friction ask/mechanism, shareable context, recognition/incentive where appropriate, and opt-out behavior.
5. [HYBRID] Respect actual legal/industry/platform/organizational constraints and avoid referral asks during unresolved customer problems or where the relationship makes the ask inappropriate.
6. [HYBRID] If execution is requested and the host has real capability/permission, implement the relevant communication/workflow directly. Otherwise preserve the useful design or create a WorkRequest only for a real durable handoff.
7. [HYBRID] Evaluate referral rate, referred-customer quality/value, incentive economics, and customer sentiment when evidence becomes available; preserve an outcome/Learning only when it actually exists.

## Completion Criteria
- The organization has an appropriate evidence-backed referral mechanism or executed improvement, with later measurement/learning separated from design and no mandatory lifecycle bundle.
