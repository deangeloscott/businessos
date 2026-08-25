---
id: core.opportunity.qualify
type: service
version: 1.2.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Insight
- Opportunity
writes:
- Opportunity
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - core.object.updated
context:
- EconomicContext
- Objective
---
# Qualify Opportunity

## Purpose
Turn domain diagnosis into a comparable, evidence-backed potential intervention.

## Business Outcome
Allocate attention toward interventions likely to create business value without false precision about impact or implementation burden.

## Run When
When a specialized system has identified a plausible valuable condition inside its domain.

## Do Not Run When
Do not use for delegated production work or for conditions with no plausible intervention.

## Process
1. [AI] Check for an existing Opportunity representing the same intervention and update it instead of duplicating.
2. [AI] State the diagnosed condition, business mechanism, affected entities, and what intervention could plausibly change.
3. [HYBRID] Link objectives and estimate expected value only to the precision supported by evidence. Separate evidence that the condition exists from evidence the intervention will work, and separate external benchmarks from active-business measurements.
4. [HYBRID] Assess confidence, urgency, strategic leverage, risk, constraints, dependencies, reversibility, and automation feasibility. Record material implementation/resource cost only when known or evidence-backed; otherwise keep it unknown rather than inventing staffing, days, cost, or ROI timing.
5. [AI] Do not automatically penalize an opportunity using conventional manual-development effort assumptions when execution may be automated. Real blockers and known resource commitments still matter.
6. [DETERMINISTIC] Apply the shared interpretable priority framework and store component values/reasons without false numeric precision.
7. [HYBRID] Set lifecycle state based on evidence sufficiency and business commitment.
8. [DETERMINISTIC] Persist and emit opportunity.qualified/prioritized when applicable.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.
- Company-specific expected-value claims are supported by company-specific inputs or clearly expressed as scenarios/hypotheses.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Opportunity has exactly one owner and an interpretable, evidence-calibrated business case.
