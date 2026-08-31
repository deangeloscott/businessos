---
id: seo.learning.tactic-promotion
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- type: Learning
  owner_system: seo-aeo
- Observation
- OutcomeEvaluation
- Experiment
writes:
- Learning
- Event
capabilities:
  required:
  - none
  optional:
  - none
evidence_inputs:
- affected SEO contracts
updates:
  Learning:
  - maturity status
---
# SEO Tactic Promotion

## Purpose
Promote an SEO Domain Learning to a stronger maturity and, when justified, update standard operating contracts without overgeneralizing its evidence.

## Business Outcome
Keep SEO/AEO strategy current, evidence-governed, policy-safe, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence store.

## Run When
Run when a tactic has materially stronger supporting evidence and may qualify for a higher maturity or standard implementation guidance.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [HYBRID] Review all material supporting and contradicting evidence, policy status, applicability boundaries, negative cases, and causal confidence.
2. [HYBRID] Confirm the tactic adds user/business value under its stated conditions and does not rely on restricted/prohibited manipulation.
3. [HYBRID] Determine the narrowest justified maturity increase and whether any standard contract actually needs to change; do not equate one validated business result with a universal standard.
4. [HYBRID] Define exact affected contract changes, applicability conditions, executor/autonomy ceilings, QA, guardrails, and measurement requirements.
5. [DETERMINISTIC] Run regression/contract tests against representative workflows and verify that updated guidance does not conflict with higher-level policy.
6. [HUMAN] Require approval for changes to standard guidance when policy/risk requires it, preserve the prior version/rationale, update the Learning, and notify dependent active Opportunities when material.

## Decisions / Routing
- If evidence remains narrow → keep current maturity and applicability.
- If contradiction/policy risk emerges → `seo.learning.tactic-deprecation`.
- If accepted → regenerate registries and revalidate affected contracts.

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
