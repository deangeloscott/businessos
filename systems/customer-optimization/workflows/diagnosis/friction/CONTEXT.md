---
id: customer-optimization.diagnosis.friction
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- type: Insight
  domain: customer-intelligence
- Observation
- MetricObservation
writes:
- CustomerJourney
- Observation
- Insight
- Opportunity
context:
- AudienceSegment
- Objective
- Offer
---
# Customer Friction Diagnosis

## Purpose
Determine why a material customer progression problem occurs before choosing an intervention.

## Business Outcome
Improve customer progression and value realization through customer friction diagnosis, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires customer friction diagnosis to improve a defined customer transition or outcome.

## Process
1. [AI] Define the failing transition and affected population from Journey Observations.
2. [HYBRID] Gather quantitative behavior, customer feedback, support/sales evidence, technical state, process rules, and relevant marketing promises.
3. [AI] Generate cause classes: unclear value/instruction, effort, technical failure, process delay, qualification mismatch, trust/risk, price/payment, missing capability, handoff, expectation mismatch, external constraint.
4. [HYBRID] Test hypotheses against sequence/timing/segment evidence and direct customer evidence; separate correlation from plausible mechanism.
5. [AI] Determine which real business function, constraint, evidence, or specialist operating knowledge is relevant to the diagnosed cause. Use that knowledge directly when it improves the work rather than assigning the diagnosis to an internal AURA owner.
6. [HYBRID] Estimate business/customer impact and intervention leverage; create/update Optimization Insight/Opportunity only when that distinct durable meaning actually exists and the diagnosis is sufficient.
