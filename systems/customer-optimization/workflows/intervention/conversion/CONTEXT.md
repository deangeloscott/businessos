---
id: customer-optimization.intervention.conversion
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
workflows:
  required:
  - customer-optimization.diagnosis.root-cause
  - customer-optimization.intervention.design
  conditional:
  - id: customer-optimization.conversion.form-friction
    when: form effort or errors are a material mechanism
---
# Conversion Optimization

## Purpose
Reduce non-persuasive process/UX friction between qualified intent and the intended conversion action.

## Business Outcome
Improve customer progression and value realization through conversion optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires conversion optimization to improve a defined customer transition or outcome.

## Process
1. [HYBRID] Confirm diagnosis is primarily progression/process friction rather than message/offer persuasion. When persuasion is the material mechanism, use the relevant Marketing operating knowledge directly rather than creating an internal domain handoff.
2. [DETERMINISTIC] Map the exact conversion path, fields, steps, errors, delays, device states, eligibility, and abandonment points.
3. [AI] Identify unnecessary effort, ambiguity, choice overload, trust/process uncertainty, accessibility, technical failures, or real handoff gaps.
4. [HYBRID] Select interventions that reduce friction without lowering lead/customer quality or violating required qualification/compliance.
5. [DETERMINISTIC] Define success/guardrail metrics and a test or rollout approach only when that improves the decision.
6. [INTEGRATION] Implement authorized journey changes through the active harness when capabilities and permissions exist. Use relevant Content/Marketing methods directly for communication components; persist a WorkRequest only for a real durable organizational handoff.
7. [HYBRID] Verify the changed flow when practical and evaluate qualified business outcomes, not raw conversion alone. Preserve a ChangeEvent, Experiment, measurement, evaluation, or Learning only when that meaning actually occurred and future work benefits from remembering it.
