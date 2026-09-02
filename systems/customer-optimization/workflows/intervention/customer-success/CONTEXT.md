---
id: customer-optimization.intervention.customer-success
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes: []
context:
- EconomicContext
- Offer
---
# Customer Success Process Optimization

## Purpose
Improve proactive success processes that help customers achieve defined outcomes with appropriate human/automated support.

## Business Outcome
Improve customer progression and value realization through customer success process optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires customer success process optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Define success outcomes/milestones by segment and offer, plus early signals of progress/risk.
2. [DETERMINISTIC] Map current success touchpoints, ownership, cadence, alerts, playbooks, response times, and outcome coverage.
3. [HYBRID] Identify gaps such as reactive support dependence, generic cadence, missing outcome tracking, real handoff loss, or late risk detection.
4. [AI] Design segment/value-based success motions and escalation paths with clear customer purpose for each touchpoint.
5. [HYBRID] Determine what can be automated without degrading trust or missing high-context needs. Use relevant Content/Marketing operating knowledge directly when communication is part of the success motion.
6. [INTEGRATION] When requested and supported by the active harness, implement real workflow/alert/task changes directly and verify them when practical. AURA does not create an internal approval, scheduling, or delegation runtime.
7. [HYBRID] Measure outcomes and cost-to-serve when evidence is available. Preserve a WorkRequest, ChangeEvent, Experiment, measurement, evaluation, or Learning only when that meaning actually occurred and future work benefits from remembering it.
