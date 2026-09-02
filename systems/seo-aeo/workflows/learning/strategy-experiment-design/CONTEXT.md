---
id: seo.learning.strategy-experiment-design
type: workflow
owner_system: seo-aeo
reads:
- type: Learning
  owner_system: seo-aeo
- Observation
- MetricDefinition
writes:
- Experiment
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
evidence_inputs:
- policy risk
---
# SEO Strategy Experiment Design

## Purpose
Design a controlled or defensible quasi-experimental test for an uncertain SEO/AEO tactic so its causal/business effect can improve organization-owned SEO Learning.

## Business Outcome
Reduce important SEO/AEO uncertainty with proportionate experiments connected to measurable organic and business outcomes, without creating an execution-control layer or pooling private evidence across organizations.

## Run When
Use when a material organization-owned SEO Learning hypothesis is testable and an experiment could materially improve the current decision.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, one business result, or model confidence as a validated tactic by itself. Do not use another organization's private AURA state as experimental evidence for the active organization.

## Process
1. [AI] Start from one explicit Learning hypothesis and state the proposed mechanism, expected business/search effect as a hypothesis, applicability conditions, and material uncertainties/constraints.
2. [HYBRID] Select representative eligible owned Assets or other active-organization units. Public/external evidence may inform the design, but private evidence from another organization is not silently imported.
3. [HYBRID] Define treatment, control/baseline or defensible quasi-experimental comparison, primary business/mechanism metrics, guardrails, evaluation window, and contamination controls.
4. [AI] Bound initial exposure according to reversibility, evidence strength, business consequence, and the decision being informed rather than a generic risk/autonomy tier.
5. [HYBRID] Define the exact implementation, real business/legal/platform/account constraints, verification assertions, recovery/rollback considerations, and data-quality checks needed to reproduce and interpret the test. AURA does not create an approval requirement merely because an experiment changes external state.
6. [DETERMINISTIC] Persist the Experiment only after the model/user has supplied the semantic design. Keep Learning maturity separate from experiment execution status; later evidence determines whether Learning should strengthen, narrow, contradict, or remain uncertain.

## Related operating knowledge
- The active model/user/harness may implement the experiment when execution is actually requested and real capabilities/constraints permit.
- `seo.measurement.experiment-analysis` may analyze completed experiment evidence.
- `core.measurement.evaluate-outcome` may preserve an OutcomeEvaluation when the outcome/contribution judgment has durable organizational value.
- `seo.aeo.learning.domain-learning` or `seo.learning.tactic-registry` may be useful when the resulting evidence supports reusable organization-owned guidance.

These are optional methods selected for the actual job, not runtime routes or lifecycle requirements.

## Verification
- The design can answer the stated decision question at an appropriate level of confidence.
- Applicability, policy status, evidence strength, causal limitations, and business consequence remain explicit.
- No private state from another organization is implicitly consumed.
- If an external mutation is performed later, verify actual post-state when the task/consequence warrants it. `ChangeEvent` and `VerificationRecord` are optional durable memory, not permission prerequisites.

## Measurement
- Strategy claims strengthen only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative policy evidence; popularity and confidence language are not outcome evidence.

## Learning
- Keep resulting reusable SEO guidance as organization-owned SEO Domain Learning. Use Business Learning only when evidence supports organization-wide applicability. Cross-organization reuse uses explicit Innovation Exchange/export/adoption or deliberate canonical AURA product-development work.

## Failure / Fallback
- If a source/tool cannot be used, use another valid host method when practical or preserve the concrete unresolved evidence/capability need honestly.
- If evidence remains contradictory or insufficient, preserve uncertainty and keep the Learning at the narrowest supported maturity instead of forcing a conclusion.

## Completion Criteria
- The experiment design is decision-useful, reproducible enough for its purpose, organization-isolated, and free of AURA permission/routing machinery.
