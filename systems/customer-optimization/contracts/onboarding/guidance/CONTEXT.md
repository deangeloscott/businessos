---
id: customer-optimization.onboarding.guidance
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
# Onboarding Guidance Requirements

## Purpose
Define the instructions, examples, decisions, and support a customer needs at each onboarding milestone.

## Business Outcome
Reduce confusion/rework while giving customers only the information needed at the point of action.

## Run When
Run when milestone completion is limited by uncertainty, errors, or knowledge gaps.

## Process
1. [AI] Identify the exact customer task/decision and common misunderstanding/error at the milestone using Customer/support evidence.
2. [AI] Define the minimum explanation, example, checklist, demonstration, field guidance, or troubleshooting needed for successful completion.
3. [AI] Decide whether inline guidance, email, video/demo, live support, knowledge article, or another format best fits the task/context.
4. [HYBRID] Avoid using content to compensate for an unnecessarily complicated product/process; route simplification first where possible.
5. [AI] Specify Content WorkRequest with audience state, task, success, errors, screenshots/demo needs, and accessibility/language requirements.
6. [DETERMINISTIC] Place guidance trigger/location in the onboarding sequence and track use/completion.
7. [AI] Evaluate whether guidance reduces errors/time/support and retire redundant material.
