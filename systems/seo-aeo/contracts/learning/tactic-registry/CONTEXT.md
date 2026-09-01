---
id: seo.learning.tactic-registry
type: playbook
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
Keep SEO/AEO operating knowledge coherent, evidence-linked, and useful without creating a parallel runtime registry or allowing durable Learning to silently rewrite AURA product behavior.

## Run When
Use when SEO Domain Learning is created/updated, evidence materially changes, or tactic knowledge needs reconciliation.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, one business result, or model confidence as sufficient evidence of a generally valid tactic.

## Process
1. [HYBRID] Retrieve potentially related existing SEO Domain Learnings using stable identifiers/indexing/lexical cues as useful. The capable model/user decides whether a new claim is semantically the same Learning under the same applicability conditions, a refinement/supersession, or genuinely distinct; deterministic AURA must not decide semantic identity from keywords.
2. [HYBRID] Record the tactic mechanism, expected outcome, prerequisites, applicable surfaces/business conditions, evidence refs, confidence, maturity/status, external guidance constraints, and uncertainty as distinct attributes.
3. [AI] Identify which AURA playbooks the Learning may inform and whether the evidence currently supports contextual, organization-tested, experimental, broader-reuse, contradicted, deprecated, or superseded treatment. These are evidence judgments, not automatic lifecycle transitions.
4. [HYBRID] Preserve contradictory evidence and historical state when they materially affect future interpretation rather than letting a new result silently erase important context.
5. [AI] Decide whether maturity/status/applicability should change based on the evidence and scope actually established. Use deterministic persistence/validation to store the chosen current state; do not emit a runtime Event merely because dependent work may care.
6. [AI] Maintain an interpretable evidence-based rationale for the Learning's current maturity and applicability when future work materially benefits from it.
7. [AI] When a change materially affects active organizational work, surface it through the smallest appropriate continuity mechanism. When evidence suggests AURA's reusable product playbook knowledge itself should improve, `core.learning.playbook-evolution` is relevant operating knowledge, not an automatic route.

## Related operating knowledge
- `seo.learning.tactic-promotion` may help when broader maturity appears justified.
- `seo.learning.tactic-deprecation` may help when contradiction/obsolescence appears material.
- Evidence assessment or experiment design may help when uncertainty is decision-relevant.
- `core.learning.playbook-evolution` may help when organization evidence suggests reusable AURA method improvement.

The active model/user decides whether these methods apply.

## Verification
- Learning identity, evidence lineage, maturity/status, applicability, and contradiction history remain inspectable where material.
- No runtime Event, ActionPacket, approval object, autonomy tier, or generic risk gate is created.
- No canonical AURA product source is silently mutated.

## Measurement
- Tactic maturity should strengthen only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative external guidance—not popularity or confidence language alone.

## Learning
- SEO-specific operating knowledge remains SEO Domain Learning. Broader product/playbook changes require evidence-supported evolution rather than silent self-modification.

## Failure / Fallback
- If evidence remains contradictory or insufficient, preserve uncertainty and keep the tactic at the narrowest justified maturity/applicability.
- If a preferred source/tool is unavailable, use another valid method when practical or preserve the unresolved evidence need honestly.

## Completion Criteria
- SEO tactic Learning is coherent, evidence-linked, and scoped to what the evidence supports.
- Any semantic merge/deduplication or maturity change reflects capable model/user judgment backed by evidence rather than deterministic text matching.
- No tactic is promoted, deprecated, or generalized for a reason that cannot be traced to evidence.
