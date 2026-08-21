---
id: seo.learning.tactic-registry
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
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
- policy status assessments
- SEO contract registry
---
# SEO Tactic Learning Registry Maintenance

## Purpose
Maintain SEO/AEO tactics as SEO Domain Learning objects with explicit mechanisms, evidence, applicability, maturity, status, policy constraints, and linked implementation contracts.

## Business Outcome
Keep SEO/AEO strategy current, evidence-governed, policy-safe, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence store.

## Run When
Run when SEO Domain Learning is created/updated, evidence materially changes, or the tactic-learning registry needs reconciliation.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [DETERMINISTIC] Resolve a new claim to an existing SEO Domain Learning when semantically identical under the same applicability conditions; otherwise create a distinct Learning identity.
2. [HYBRID] Record the tactic mechanism, expected outcome, prerequisites, applicable surfaces/business conditions, evidence refs, confidence, maturity, status, risk, and policy status as distinct attributes.
3. [AI] Link the Learning to detectors/playbooks it informs and identify whether it changes standard instructions, remains experimental, or only supplies contextual guidance.
4. [HYBRID] Preserve contradictory evidence and historical state rather than letting a new result silently overwrite prior evidence.
5. [DETERMINISTIC] Version maturity/status changes, update last-reviewed metadata, and emit dependency-change events when active contracts or Opportunities may be affected.
6. [AI] Maintain an interpretable rationale for every Learning classified hypothesis, experimental, emerging, validated, standard, contradicted, deprecated, or superseded.

## Decisions / Routing
- Potential promotion → `seo.learning.tactic-promotion`.
- Potential deprecation/contradiction → `seo.learning.tactic-deprecation`.
- Insufficient evidence → evidence assessment or experiment design.

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
