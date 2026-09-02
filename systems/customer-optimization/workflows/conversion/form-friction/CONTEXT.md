---
id: customer-optimization.conversion.form-friction
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
# Form Friction Optimization

## Purpose
Reduce unnecessary form effort/errors while preserving required qualification, consent, and operational data.

## Business Outcome
Increase qualified completion by asking only what is needed at the right time.

## Run When
Run when a lead/application/booking/checkout-adjacent form shows abandonment, errors, delay, or customer complaints.

## Process
1. [DETERMINISTIC] Measure field-level availability where possible: starts, completion, errors, validation, abandonment, time, device, and downstream quality.
2. [AI] Classify each field as legally/operationally required now, qualification-required now, useful later, inferable, duplicate, or unnecessary.
3. [AI] Review ordering, input type, instructions, defaults, validation, privacy reassurance, error recovery, and mobile effort.
4. [HYBRID] Coordinate persuasive field/CTA copy with Marketing while keeping mechanics here.
5. [AI] Propose removing/postponing/simplifying fields before adding persuasion around them.
6. [DETERMINISTIC] Test changes with qualified-completion and downstream-quality guardrails, not raw submission rate alone.
7. [DETERMINISTIC] Verify live form/event behavior and evaluate outcome.
