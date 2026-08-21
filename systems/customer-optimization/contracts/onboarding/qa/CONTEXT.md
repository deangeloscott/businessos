---
id: customer-optimization.onboarding.qa
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
# Onboarding End-to-End QA

## Purpose
Test the complete onboarding path as an actual customer across milestones, communications, handoffs, failures, and measurement.

## Business Outcome
Prevent a theoretically designed onboarding flow from failing because systems/owners/communications do not work together.

## Run When
Run before launching a new onboarding path and after material changes.

## Process
1. [DETERMINISTIC] Create representative test cases across priority segments/plans/paths and verify start/eligibility state.
2. [HYBRID] Walk the journey through customer-facing tasks, business-side actions, emails/content, scheduling, integrations, errors, support, handoffs, and completion.
3. [DETERMINISTIC] Verify every milestone event, owner, dependency, deadline, link, status, escalation, and completion condition.
4. [AI] Evaluate clarity, effort, duplicated requests, waiting, expectation match, and whether the path actually leads to the meaningful value milestone.
5. [HYBRID] Test failure/recovery and accessibility/edge cases, not only happy path.
6. [DETERMINISTIC] Record defects by severity/owner and block launch for critical value-path failures.
7. [DETERMINISTIC] Re-test fixes and establish baseline/time-to-value monitoring.
