---
id: core.diagnosis.business-problem
type: workflow
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
context:
- Business
- Objective
- EconomicContext
---
# Diagnose Broad Business Problem

## Purpose
Turn an unexplained business symptom into a bounded, evidence-backed diagnosis before recommending an intervention.

## Business Outcome
Find the most likely constraint or causal pathway behind a business problem so effort is spent on the right intervention rather than the most obvious surface symptom.

## Run When
Use when the user describes a material symptom such as stalled revenue, poor growth, deteriorating economics, or another broad problem whose cause is not yet clear.

## Do Not Run When
Do not add this diagnostic wrapper when the request already names a sufficiently clear problem and the active model can address it directly.

## Process
1. [AI] Restate the observed symptom, desired business outcome, affected scope/timeframe, and what is actually known versus assumed.
2. [HYBRID] Reuse current Business Context, measurements, evidence, Insights, Opportunities, prior outcomes, and other relevant first-party state before starting new research; rule out obvious measurement ambiguity where it could change the diagnosis.
3. [AI] Build a small hypothesis tree covering only plausible mechanisms. Consider acquisition, audience/fit, persuasion/conversion, customer journey/value realization, competitive/external change, operations, economics, and measurement only when relevant rather than as mandatory domains.
4. [AI] Rank the hypotheses by plausible impact, current evidence, and the value of additional evidence needed to discriminate among them. Apply `core/policies/resource-aware-execution.md`: gather only evidence that can materially improve the diagnosis.
5. [HYBRID] Use the active harness's real tools, Skills, subagents, connected systems, or direct analysis normally. AURA does not create internal WorkRequests merely to delegate model/runtime work. Persist a `WorkRequest` only when a real handoff must survive the current session/person/runtime and future organizational work benefits from remembering it.
6. [AI] Integrate the evidence; identify supported, contradicted, and unresolved hypotheses and the most likely bottleneck(s). Preserve competing explanations when evidence does not support one cause. Stop gathering once additional accessible evidence is unlikely to change the diagnosis materially unless stronger verification is actually required.
7. [AI] Translate supported conditions into the smallest useful next investigation or intervention. Reuse relevant AURA playbooks as operating knowledge when helpful, but the active model/user decides method and sequencing.
8. [AI] Return the diagnosis, evidence strength, unresolved uncertainty, and highest-value next move without manufacturing cross-domain routing state or coordination objects.

## Verification
- Every material diagnostic conclusion is supported by evidence or explicitly labeled as hypothesis/inference.
- Unknown causal or economic state remains unknown rather than being filled with generic benchmarks.
- Any persisted WorkRequest represents a real durable handoff, not internal orchestration.

## Failure / Fallback
- If evidence access is limited, produce the narrowest supported diagnosis and identify the smallest evidence gap that could change it. Use a real human/owner handoff only when one is genuinely needed; do not create a Manual Action Packet or other runtime-control object.

## Completion Criteria
- The broad symptom is narrowed to evidence-backed likely mechanism(s), material alternatives/unknowns are explicit, and the user/model has a useful next move without requiring AURA to orchestrate the runtime.
