---
id: customer-optimization.intervention.rollout
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
# Journey Intervention Rollout

## Purpose
Roll out a sufficiently supported journey change beyond a limited test while preserving the ability to detect harm and recover when needed.

## Business Outcome
Scale useful improvements without losing verification, customer protection, or awareness of segment-specific harm.

## Run When
Use when the user/organization has decided to implement a journey change beyond a limited test and the active harness has the real capabilities needed to do or coordinate that work.

## Process
1. [HYBRID] Confirm the actual selected intervention, target population, current version/state, dependencies, instrumentation, recovery/rollback path, and real business/legal/platform/account constraints that matter. Do not require an AURA permission object.
2. [AI] Choose phased, cohort, feature-flag, location/team, or full rollout based on evidence, reversibility, expected interaction effects, and the consequence of failure.
3. [INTEGRATION] If execution is within the user's request and the host has the necessary capability, apply the change through the real system. Otherwise produce the smallest precise handoff/instructions needed for the actual executor; do not simulate execution inside AURA.
4. [HYBRID] Verify the intended post-change state when the consequence warrants it. Preserve a `ChangeEvent` or `VerificationRecord` only when remembering that change/verification will materially help future work or the selected method genuinely requires it.
5. [HYBRID] Observe early failure/error/customer-harm signals using the real analytics/operational systems available to the harness. AURA may preserve material monitoring intent/findings; it does not own the polling/scheduler loop.
6. [AI] Pause, narrow, or roll back when evidence indicates material harm or guardrail failure; do not average away a harmed priority segment.
7. [HYBRID] Evaluate the rollout against the intended outcome and preserve only the useful resulting context, evidence, outcome, and Learning. Update journey/process documentation when the changed state should remain durable.

## Verification
- Any claimed external change is based on actual tool/system evidence, not AURA bookkeeping.
- Rollout scope and conclusions stay within the observed evidence.
- AURA records do not substitute for the user request, real system permissions, or runtime execution capability.
