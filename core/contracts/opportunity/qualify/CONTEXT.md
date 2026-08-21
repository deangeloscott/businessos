---
id: core.opportunity.qualify
type: service
version: 1.1.0
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
Allocate attention toward interventions likely to create business value.

## Run When
When a specialized system has identified a plausible valuable condition inside its domain.

## Do Not Run When
Do not use for delegated production work or for conditions with no plausible intervention.

## Process
1. [AI] Check for an existing Opportunity representing the same intervention and update it instead of duplicating.
2. [AI] State the diagnosed condition, business mechanism, affected entities, and what intervention could plausibly change.
3. [HYBRID] Link objectives and estimate expected value as a range where possible; separate evidence for condition from evidence intervention will work.
4. [HYBRID] assess confidence, urgency, strategic leverage, risk, cost, constraints, and dependencies.
5. [DETERMINISTIC] Apply the shared interpretable priority framework and store component values/reasons.
6. [HYBRID] Set lifecycle state based on evidence sufficiency and business commitment.
7. [DETERMINISTIC] Persist and emit opportunity.qualified/prioritized when applicable.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Opportunity has exactly one owner and an interpretable business case.
