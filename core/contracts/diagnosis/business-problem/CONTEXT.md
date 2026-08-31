---
id: core.diagnosis.business-problem
type: playbook
version: 1.1.0
owner_system: core
reads:
- Business
- Objective
- Observation
- Insight
- Opportunity
- MetricObservation
writes:
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - core.work.requested
context:
- Business
- Objective
- EconomicContext
---
# Diagnose Broad Business Problem

## Purpose
Turn an unexplained business symptom into a bounded, evidence-backed diagnosis across the installed semantic domains before recommending interventions.

## Business Outcome
Find the most likely constraint or causal pathway behind a business problem so effort is spent on the right intervention rather than the most obvious surface symptom.

## Run When
When the user describes a material symptom such as stalled revenue, poor growth, deteriorating economics, or an unclear business problem whose owner/cause is not yet known.

## Do Not Run When
Do not run when the request already names one clear domain diagnosis that has a valid installed entry contract.

## Process
1. [AI] Restate the observed symptom, desired business outcome, affected scope/timeframe, and what is actually known versus assumed.
2. [HYBRID] Inspect current Business Context, Objectives, MetricObservations, Observations, Insights, Opportunities, and relevant prior OutcomeEvaluations before starting new research; first rule out obvious measurement/instrumentation ambiguity.
3. [AI] Build a small diagnostic hypothesis tree covering only plausible mechanisms and installed domains; distinguish upstream acquisition, audience/fit, persuasion/conversion, customer journey/value realization, competitive/external change, and measurement effects where relevant rather than assuming causality from correlation.
4. [HYBRID] Rank hypotheses by potential business impact, current evidence, plausibility, and the resource cost of evidence needed to discriminate among them. Under `core/policies/resource-aware-execution.md`, select the minimum additional evidence likely to materially change the diagnosis; use progressive depth and do not activate domains merely because they are installed.
5. [HYBRID] Create bounded WorkRequests to the proper installed semantic owners for missing evidence/analysis. If an owner is absent, follow module-independence: use only provisional bounded evidence sufficient for continuity and preserve the scope gap without creating that owner's canonical Insight or Opportunity.
6. [AI] Integrate returned evidence; identify supported, contradicted, and unresolved hypotheses and the most likely bottleneck(s). Preserve competing explanations when evidence does not support a single cause. Stop gathering once another evidence action is unlikely to change the diagnosis materially unless stronger verification is required.
7. [HYBRID] Route supported domain conditions to their semantic owners to create/update and qualify distinct Opportunities; do not create duplicate Core Opportunities or jump directly to an intervention that lacks diagnosis.
8. [AI] Return the diagnosis, evidence strength, unresolved uncertainty, and highest-value next investigation/action. If several distinct Opportunities must move together, hand them to Core initiative coordination.

## Verification
- Every material diagnostic conclusion is linked to evidence or explicitly labeled as a hypothesis; downstream Opportunities remain owned by their proper domains.

## Failure / Fallback
- If evidence access is limited, produce the narrowest supported diagnosis and a prioritized Manual Action Packet/WorkRequest for the evidence needed next rather than claiming a cause.

## Completion Criteria
- The broad symptom is narrowed to evidence-backed likely mechanism(s), unresolved alternatives are explicit, and the next domain-owned work is canonically routed.
