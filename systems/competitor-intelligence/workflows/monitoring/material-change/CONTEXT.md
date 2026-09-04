---
id: competitor.monitoring.material-change
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
writes:
- Competitor
- SourceRecord
- Observation
- Insight
context:
- Objective
---
# Competitor Material-Change Monitoring

## Purpose
Detect decision-relevant competitor changes with snapshot comparison and model review without making AURA the scheduler or event bus.

## Business Outcome
Keep competitive understanding current enough for good decisions without mistaking observed activity for proven effectiveness or repeatedly reprocessing unchanged surfaces.

## Run When
Use for a bounded competitor-change review when the user requests it, when saved monitoring intent indicates another check would be useful, or when other evidence suggests a material change. Any recurring execution is owned by the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve the relevant current competitor surfaces with the active harness and compare them with prior preserved snapshots/state where useful.
2. [DETERMINISTIC] Use hashes/structural comparison to suppress mechanically unchanged material and obvious duplicate state; do not treat text difference alone as business materiality.
3. [AI] Classify genuinely changed content into pricing, packaging, product, offer, positioning, messaging, funnel, campaign, partnership, or another meaningful class.
4. [AI] Assess materiality against active Objectives/markets/audiences and existing competitor state.
5. [AI] Determine whether the evidence should update a factual Competitor field, remain an Observation, or support a new/updated Insight. Keep observed change separate from inferred strategy or effectiveness.
6. [DETERMINISTIC] Persist only the material state/evidence selected by the model/user and update relevant monitoring checkpoints. Do not emit runtime events merely because competitor state changed.

## Verification
- Material changes remain traceable to current/prior evidence.
- Semantic change classification and business materiality remain model/user judgments.
- Saved cadence/checkpoint intent never claims a background task exists; the external runtime owns any recurring execution.
