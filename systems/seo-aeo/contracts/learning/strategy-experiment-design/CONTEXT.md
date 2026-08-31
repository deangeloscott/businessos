---
id: seo.learning.strategy-experiment-design
type: playbook
version: 1.1.0
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
Keep SEO/AEO strategy current, evidence-governed, policy-safe, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence store.

## Run When
Run when a material SEO Domain Learning hypothesis is testable, policy-allowed, and evidence is insufficient for stronger maturity.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [HYBRID] Start from one explicit Learning hypothesis and state the proposed mechanism, expected business/search effect, applicability conditions, and material risks.
2. [HYBRID] Select representative eligible owned Assets within the active business; use multi-business evidence only through explicit Core System Learning governance.
3. [HYBRID] Define treatment, control/baseline or defensible quasi-experimental comparison, primary business/mechanism metrics, guardrails, evaluation window, and contamination controls.
4. [HYBRID] Bound initial exposure according to risk, reversibility, evidence strength, and business impact rather than implementation convenience.
5. [HYBRID] Define the exact implementation, capability/approval requirements, verification assertions, rollback, and data-quality checks so the test can be reproduced.
6. [DETERMINISTIC] Register the Experiment and link it to the Learning hypothesis; prevent standard-playbook promotion until the configured evidence/evaluation requirements are satisfied.

## Decisions / Routing
- Approved experiment → Core ActionPacket planning.
- Completed experiment → SEO measurement / Core OutcomeEvaluation.
- Unsafe or prohibited hypothesis → deprecation/policy route.

## Verification
- Validate every canonical object written, preserve SourceRecord/Observation lineage, and keep evidence strength, conclusion confidence, policy status, and risk as separate dimensions.
- Any later external state mutation must use an ActionPacket, ChangeEvent, and independent VerificationRecord.

## Measurement
- Strategy claims become stronger only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative policy evidence; popularity and confidence language are not outcome evidence.

## Learning
- Maintain SEO-specific strategy knowledge as SEO Domain Learning. Propose broader Business or System Learning only when evidence and applicability justify the broader scope.

## Failure / Fallback
- If a source cannot be retrieved automatically, create a manual evidence-retrieval Action or use another authoritative source; do not invent the missing evidence.
- If evidence remains contradictory or insufficient, preserve the uncertainty and keep the claim at hypothesis/experimental maturity instead of forcing a conclusion.

## Completion Criteria
- Outputs use current Core Observation/Insight/Experiment/Learning objects rather than legacy strategy-evidence object.
- Source provenance, contradictory evidence, applicability, confidence, risk, and policy status remain inspectable.
- No tactic is promoted, deprecated, or blocked for a reason that cannot be traced to evidence or policy.
