---
id: customer-optimization.onboarding.sequence-design
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
# Onboarding Sequence Design

## Purpose
Sequence onboarding milestones, communications, handoffs, and waiting states to minimize unnecessary time/effort.

## Business Outcome
Move customers from commitment to meaningful value with clear ownership and dependencies.

## Run When
Run after onboarding milestones are defined.

## Process
1. [DETERMINISTIC] Build the dependency graph across customer tasks, business tasks, integrations, approvals, meetings, and wait states.
2. [AI] Identify parallelizable work, unnecessary serial dependencies, duplicated data requests, handoff queues, and unclear ownership.
3. [AI] Place expectation-setting/guidance immediately before the action it supports rather than front-loading all education.
4. [AI] Define proactive status/next-step communication at meaningful transitions and delays.
5. [HYBRID] Route persuasion/motivation to Marketing and educational asset production to Content where specialized work is needed.
6. [DETERMINISTIC] Set due/expected windows, reminders only where useful, escalation triggers, and completion conditions.
7. [AI] Produce sequenced Action/WorkRequests and measurement plan.
