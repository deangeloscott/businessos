---
id: seo.learning.tactic-deprecation
type: playbook
version: 1.2.0
owner_system: seo-aeo
reads:
- type: Learning
  owner_system: seo-aeo
- Observation
- OutcomeEvaluation
- Opportunity
writes:
- Learning
capabilities:
  required:
  - none
  optional:
  - none
evidence_inputs:
- dependent playbooks and active organizational work
updates:
  Learning:
  - status maturity applicability
---
# SEO Tactic Deprecation

## Purpose
Narrow, contradict, supersede, or deprecate SEO Domain Learning when evidence weakens, external platform guidance changes, or measured outcomes are consistently harmful.

## Business Outcome
Keep SEO/AEO operating knowledge current and evidence-linked without turning one new result into universal truth or allowing ordinary business work to rewrite AURA product source.

## Run When
Run when authoritative external guidance, strong contradictory evidence, repeated harmful OutcomeEvaluations, non-replication, or repeated operational failure materially weakens an active tactic.

## Do Not Run When
Do not deprecate a tactic from a single weak signal, practitioner opinion, competitor behavior, or one business result without enough evidence for the claimed scope.

## Process
1. [HYBRID] Confirm the trigger: authoritative external change, strong contradiction, repeated harmful OutcomeEvaluations, non-replication, applicability failure, or repeated correction.
2. [AI] Identify the active Learning, relevant Opportunities/Initiatives, monitoring intents, and AURA playbooks that materially rely on the tactic.
3. [HYBRID] Choose the narrowest justified change: restrict applicability, reduce confidence/maturity, supersede with better-supported guidance, deprecate entirely, or preserve uncertainty pending more evidence.
4. [HYBRID] State any replacement guidance only when evidence supports it; never invent a replacement merely to fill the gap.
5. [DETERMINISTIC] Persist the updated SEO Learning with the evidence, contradiction, applicability, maturity/status change, and historical lineage needed for future work.
6. [HYBRID] If the evidence suggests AURA's reusable playbook knowledge itself should change, route the Learning through `core.learning.playbook-evolution`. Ordinary organization work must not directly edit canonical AURA source.
7. [HYBRID] If harmful live implementations require intervention, route that as separate business work through the appropriate domain/harness and measure recovery when possible.

## Decisions / Routing
- Immediate operational harm → relevant Incident/containment work.
- Reusable AURA method improvement → `core.learning.playbook-evolution`.
- Contradicted but conditionally valid → narrow applicability instead of full deprecation.

## Verification
- The Learning change is no broader than its evidence.
- Supporting and contradictory evidence remain traceable.
- Historical state is preserved rather than silently overwritten.
- No runtime Event, ActionPacket, approval object, autonomy tier, or generic risk gate is created.
- No canonical AURA product source is silently mutated.

## Measurement
- Deprecation confidence should strengthen through relevant observations, OutcomeEvaluations, replication/non-replication, or authoritative external guidance—not popularity or unsupported confidence language.

## Learning
- Maintain SEO-specific operating knowledge as SEO Domain Learning. Broader system/playbook changes require evidence-supported evolution through the explicit Core path.

## Failure / Fallback
- If evidence remains contradictory or insufficient, keep the tactic at the narrowest justified status/maturity and record the uncertainty rather than forcing a conclusion.
- If a preferred source/tool is unavailable, use another valid method when practical or preserve the unresolved evidence need honestly.

## Completion Criteria
- The affected Learning truthfully reflects current evidence, maturity/status, applicability, and uncertainty.
- No tactic is deprecated for a reason that cannot be traced to evidence or an actual external constraint.
