---
id: customer-optimization.onboarding.qa
type: workflow
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
3. [DETERMINISTIC] Verify every milestone event, real operational owner, dependency, deadline, link, status, escalation, and completion condition.
4. [AI] Evaluate clarity, effort, duplicated requests, waiting, expectation match, and whether the path actually leads to the meaningful value milestone.
5. [HYBRID] Test failure/recovery and accessibility/edge cases, not only happy path.
6. [DETERMINISTIC] Record defects by severity/real owner and block launch for critical value-path failures when that authority exists in the actual delivery process.
7. [DETERMINISTIC] Re-test fixes, establish the useful baseline, and preserve monitoring intent when continued observation matters. Any recurring execution belongs to the active harness/runtime or real operational system, not AURA.
