---
id: seo.learning.tactic-deprecation
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- type: Learning
  owner_system: seo-aeo
- Observation
- OutcomeEvaluation
- Opportunity
writes:
- Learning
- Event
capabilities:
  required:
  - none
  optional:
  - none
evidence_inputs:
- dependent contracts
updates:
  Learning:
  - status maturity
---
# SEO Tactic Deprecation

## Purpose
Constrain, contradict, supersede, or deprecate SEO Domain Learning and dependent guidance when evidence weakens, policy changes, or measured outcomes are consistently harmful.

## Business Outcome
Keep SEO/AEO strategy current, evidence-governed, policy-safe, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence store.

## Run When
Run when authoritative policy, replicated evidence, OutcomeEvaluations, or repeated operational failures materially weaken an active tactic.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [HYBRID] Confirm the trigger: authoritative policy change, strong contradiction, repeated harmful OutcomeEvaluations, non-replication, applicability failure, or repeated human correction.
2. [AI] Identify every active contract, example, Opportunity, Initiative, scheduled workflow, and automated Action materially dependent on the tactic.
3. [HYBRID] Classify immediate-stop, restrict-scope, supersede, or gradual replacement according to policy status, harm, reversibility, and evidence quality.
4. [HYBRID] Define replacement guidance or explicit no-action when no reliable alternative exists; never invent a replacement simply to fill the gap.
5. [HUMAN] Apply required approval for standard-guidance changes, lower autonomy where warranted, preserve historical evidence, and update the Learning status/maturity.
6. [HYBRID] Create cleanup/rollback work for harmful active implementations when needed and monitor recovery before closing the deprecation.

## Decisions / Routing
- Immediate operational harm → Incident/containment route.
- Guidance change → update affected contracts then regenerate/test registries.
- Contradicted but still conditionally valid → narrow applicability instead of full deprecation.

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
