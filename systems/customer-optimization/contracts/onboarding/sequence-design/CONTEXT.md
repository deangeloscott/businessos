---
id: customer-optimization.onboarding.sequence-design
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
