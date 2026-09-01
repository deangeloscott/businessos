---
id: seo.learning.strategy-experiment-design
type: playbook
owner_system: seo-aeo
reads:
- type: Learning
  owner_system: seo-aeo
- Observation
- MetricDefinition
writes:
- Experiment
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - search.performance.read
  - search.rank.read
  - ai_answer.observe
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
Design a controlled or defensible quasi-experimental test for an uncertain SEO/AEO tactic so its causal/business effect can update domain learning.

## Business Outcome
Keep SEO/AEO strategy current, evidence-governed, policy-aware, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence or execution-control store.

## Run When
Use when a material SEO Domain Learning hypothesis is testable and evidence is insufficient for stronger maturity.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [HYBRID] Start from one explicit Learning hypothesis and state the proposed mechanism, expected business/search effect as a hypothesis, applicability conditions, and material uncertainties/risks.
2. [HYBRID] Select representative eligible owned Assets within the active business; use multi-business evidence only through explicit Core System Learning governance.
3. [HYBRID] Define treatment, control/baseline or defensible quasi-experimental comparison, primary business/mechanism metrics, guardrails, evaluation window, and contamination controls.
4. [HYBRID] Bound initial exposure according to reversibility, evidence strength, business consequence, and the decision being informed rather than implementation convenience.
5. [HYBRID] Define the exact implementation, real business/legal/platform/account constraints, verification assertions, recovery/rollback considerations, and data-quality checks needed to reproduce and interpret the test. AURA does not create an approval requirement merely because an experiment changes external state.
6. [DETERMINISTIC] Persist the Experiment and link it to the Learning hypothesis. Keep tactic maturity separate from execution status; later evidence/evaluation determines whether Learning should strengthen, narrow, contradict, or remain uncertain.

## Decisions / Routing
- Experiment design ready → the active model/user/harness may implement it when that is actually requested and real capabilities/constraints permit.
- Completed experiment → SEO measurement / Core `OutcomeEvaluation` when evidence supports evaluation.
- Unsafe, prohibited, or materially constrained hypothesis → preserve the applicable real policy/constraint and do not misrepresent the test as executable.

## Verification
- Validate canonical objects written and preserve SourceRecord/Observation lineage where evidence is used.
- Keep evidence strength, conclusion confidence, policy status, and practical consequence distinct.
- If a later external mutation is performed, verify actual post-state when the task/consequence warrants it. `ChangeEvent` and `VerificationRecord` are optional durable memory when the change/verification itself should survive; they are not permission prerequisites.

## Measurement
- Strategy claims become stronger only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative policy evidence; popularity and confidence language are not outcome evidence.

## Learning
- Maintain SEO-specific strategy knowledge as SEO Domain Learning. Propose broader Business or System Learning only when evidence and applicability justify the broader scope.

## Failure / Fallback
- If a source cannot be retrieved automatically, use another available authoritative source or make a real manual/human handoff when needed. Do not create an AURA action object merely to represent a missing tool capability.
- If evidence remains contradictory or insufficient, preserve the uncertainty and keep the claim at hypothesis/experimental maturity instead of forcing a conclusion.

## Completion Criteria
- Outputs use current Core Observation/Insight/Experiment/Learning objects rather than a parallel strategy-evidence store.
- Source provenance, contradictory evidence, applicability, confidence, practical consequence, and policy status remain inspectable where material.
- No tactic is promoted, deprecated, blocked, or claimed effective for a reason that cannot be traced to evidence or an actual applicable constraint.
