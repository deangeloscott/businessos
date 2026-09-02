---
id: seo.learning.tactic-promotion
type: workflow
owner_system: seo-aeo
reads:
- type: Learning
  owner_system: seo-aeo
- Observation
- OutcomeEvaluation
- Experiment
writes:
- Learning
evidence_inputs:
- affected SEO playbooks
updates:
  Learning:
  - maturity status applicability
---
# SEO Tactic Promotion

## Purpose
Promote SEO Domain Learning to a stronger evidence/maturity level when justified, without overgeneralizing one business result or turning ordinary organization work into self-modifying AURA source.

## Business Outcome
Keep SEO/AEO operating knowledge evidence-linked, current, and useful while preserving the distinction between organization Learning and canonical AURA product evolution.

## Run When
Run when a tactic has materially stronger supporting evidence and may justify a higher maturity, broader-but-still-bounded applicability, or stronger reusable guidance.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, one business result, or model confidence as sufficient proof of a generally valid tactic.

## Process
1. [HYBRID] Review material supporting and contradicting evidence, external platform/guidance status, applicability boundaries, negative cases, OutcomeEvaluations, and causal uncertainty.
2. [HYBRID] Confirm the tactic adds user/business value under its stated conditions and that the evidence supports the proposed scope.
3. [HYBRID] Choose the narrowest justified maturity/status/applicability increase; do not equate one validated result with a universal standard.
4. [AI] State the mechanism, prerequisites, applicable conditions, exclusions, evidence basis, verification/QA needs, and measurement implications clearly enough for future work to use the Learning intelligently.
5. [DETERMINISTIC] Persist the updated SEO Learning with traceable evidence and historical lineage.
6. [HYBRID] If the evidence suggests AURA's reusable playbook knowledge itself should change, route the Learning through `core.learning.workflow-evolution`; ordinary business work must not directly edit canonical AURA source.
7. [HYBRID] If organization-specific adoption requires concrete business work, route that work normally through the relevant playbook, external Skill, model-created method, or ad-hoc method.

## Decisions / Routing
- Evidence remains narrow → keep the current maturity/applicability.
- Material contradiction emerges → `seo.learning.tactic-deprecation`.
- Reusable AURA method improvement appears justified → `core.learning.workflow-evolution`.

## Verification
- The Learning promotion is no broader than its evidence.
- Supporting and contradictory evidence remain traceable.
- Applicability and uncertainty are explicit.
- No runtime Event, ActionPacket, approval object, autonomy ceiling, or generic risk gate is created.
- No canonical AURA product source is silently mutated.

## Measurement
- Promotion should strengthen only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative external guidance—not popularity or confidence language alone.

## Learning
- Maintain SEO-specific operating knowledge as SEO Domain Learning. Broader system/playbook changes require evidence-supported evolution through the explicit Core path.

## Failure / Fallback
- If evidence is contradictory or insufficient, preserve the current or narrower maturity and record the uncertainty rather than forcing promotion.
- If a preferred source/tool is unavailable, use another valid method when practical or preserve the unresolved evidence need honestly.

## Completion Criteria
- The affected Learning truthfully reflects its current evidence, maturity/status, applicability, mechanism, and uncertainty.
- No tactic is promoted for a reason that cannot be traced to evidence.
