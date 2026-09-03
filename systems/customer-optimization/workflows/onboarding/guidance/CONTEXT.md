---
id: customer-optimization.onboarding.guidance
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
4. [HYBRID] Avoid using content to compensate for an unnecessarily complicated product/process; simplify the underlying experience first where possible.
5. [AI] Use relevant Content operating knowledge directly to create or specify the needed guidance with audience state, task, success, errors, screenshots/demo needs, and accessibility/language requirements. Create a WorkRequest only when a real durable handoff to another actor must survive the current interaction.
6. [DETERMINISTIC] Place guidance trigger/location in the onboarding sequence and track use/completion in the real delivery system where applicable.
7. [AI] Evaluate whether guidance reduces errors/time/support and retire redundant material when evidence supports that decision.
