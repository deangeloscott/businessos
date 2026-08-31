---
id: seo.learning.tactic-registry
type: playbook
version: 1.2.0
owner_system: seo-aeo
reads:
- type: Learning
  owner_system: seo-aeo
- Observation
- OutcomeEvaluation
- Experiment
writes:
- Learning
capabilities:
  required:
  - none
  optional:
  - none
evidence_inputs:
- external platform/guidance status assessments
- SEO playbook catalog
---
# SEO Tactic Learning Registry Maintenance

## Purpose
Maintain SEO/AEO tactics as SEO Domain Learning with explicit mechanisms, evidence, applicability, maturity, status, and links to the playbooks they may inform.

## Business Outcome
Keep SEO/AEO operating knowledge coherent, evidence-linked, and useful without creating a parallel runtime event registry or allowing durable Learning to silently rewrite AURA product behavior.

## Run When
Run when SEO Domain Learning is created/updated, evidence materially changes, or tactic knowledge needs reconciliation.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, one business result, or model confidence as sufficient evidence of a generally valid tactic.

## Process
1. [DETERMINISTIC] Resolve a new claim to an existing SEO Domain Learning when semantically identical under the same applicability conditions; otherwise create a distinct Learning identity.
2. [HYBRID] Record the tactic mechanism, expected outcome, prerequisites, applicable surfaces/business conditions, evidence refs, confidence, maturity/status, external guidance constraints, and uncertainty as distinct attributes.
3. [AI] Link the Learning to the AURA playbooks it may inform and identify whether it is merely contextual, organization-tested, experimental, broadly reusable, contradicted, deprecated, or superseded.
4. [HYBRID] Preserve contradictory evidence and historical state rather than letting a new result silently overwrite prior evidence.
5. [DETERMINISTIC] Update the Learning's maturity/status/applicability and last-reviewed meaning when justified; do not emit a runtime Event merely because dependent work may care.
6. [AI] Maintain an interpretable evidence-based rationale for the Learning's current maturity and applicability.
7. [HYBRID] When a change materially affects active organizational work, surface that through normal continuity/attention or the relevant active workstream. When it suggests a reusable AURA process improvement, route it through `core.learning.playbook-evolution`.

## Decisions / Routing
- Potential promotion → `seo.learning.tactic-promotion`.
- Potential deprecation/contradiction → `seo.learning.tactic-deprecation`.
- Insufficient evidence → evidence assessment or experiment design.
- Reusable AURA method improvement → `core.learning.playbook-evolution`.

## Verification
- Learning identity, evidence lineage, maturity/status, applicability, and contradiction history remain inspectable.
- No runtime Event, ActionPacket, approval object, autonomy tier, or generic risk gate is created.
- No canonical AURA product source is silently mutated.

## Measurement
- Tactic maturity should strengthen only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative external guidance—not popularity or confidence language alone.

## Learning
- SEO-specific operating knowledge remains SEO Domain Learning. Broader system/playbook changes require evidence-supported evolution through the explicit Core path.

## Failure / Fallback
- If evidence remains contradictory or insufficient, preserve uncertainty and keep the tactic at the narrowest justified maturity/applicability.
- If a preferred source/tool is unavailable, use another valid method when practical or preserve the unresolved evidence need honestly.

## Completion Criteria
- SEO tactic Learning is coherent, deduplicated, evidence-linked, and scoped to what the evidence supports.
- No tactic is promoted, deprecated, or generalized for a reason that cannot be traced to evidence.
