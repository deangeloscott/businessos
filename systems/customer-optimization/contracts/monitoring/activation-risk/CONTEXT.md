---
id: customer-optimization.monitoring.activation-risk
type: playbook
owner_system: customer-optimization
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
# Activation Risk Monitoring

## Purpose
Detect new customers/users likely to miss the value/activation path while there is still time to help.

## Business Outcome
Increase activation by responding to specific, interpretable setup/value barriers rather than generic reminder spam.

## Run When
Run during the defined activation window for eligible new customers/users.

## Process
1. [DETERMINISTIC] Resolve expected milestones/timing and approved risk conditions from onboarding/activation Learning.
2. [DETERMINISTIC] Compare each eligible customer state with milestone timing, failures, dependencies, and support/implementation events.
3. [AI] Classify likely barrier only from observable evidence; distinguish “not yet due,” deliberate pacing, missing data, and real risk.
4. [AI] Choose the least intrusive helpful response appropriate to the barrier and customer state.
5. [HYBRID] Avoid repeated automated outreach when human/process/product intervention is required.
6. [DETERMINISTIC] Create/route Action and suppress duplicates until state changes.
7. [DETERMINISTIC] Measure milestone recovery, time-to-value, customer burden, and false-alert rate.
