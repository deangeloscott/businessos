---
id: seo.intelligence.ecosystem.claim-extraction
type: playbook
owner_system: seo-aeo
reads:
- SourceRecord
- Observation
- type: Insight
  owner_system: industry-intelligence
- type: Learning
  owner_system: seo-aeo
writes:
- Observation
- Insight
- Learning
capabilities:
  required:
  - research.web.read
  optional:
  - document.read
  - search.observe
---
# SEO Strategy Claim Extraction

## Purpose
Convert articles, announcements, experiments, and observed outcomes into atomic, testable SEO/AEO claims with explicit source lineage and applicability.

## Business Outcome
Keep SEO/AEO strategy current and evidence-governed without creating a parallel strategy-evidence or execution-control store.

## Run When
Use when a new SourceRecord/Observation may contain a material SEO/AEO strategy claim.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning rules explicitly support that broader reuse.

## Process
1. [AI] Read the source in context and separate direct platform announcement, measured result, author inference, recommendation, and speculation.
2. [HYBRID] Extract one atomic claim at a time; state the claimed mechanism, expected outcome, affected surface, and applicability conditions without combining unrelated assertions.
3. [DETERMINISTIC] Preserve the originating SourceRecord/Observation plus source type, date, reported method/sample, and material commercial/conflict-of-interest context when present. Deterministic AURA verifies references; it does not decide the claim's semantic meaning.
4. [AI] Paraphrase rather than over-copying source text while retaining enough source reference for a capable reviewer to verify the interpretation.
5. [AI] Identify prerequisite mechanisms, alternative explanations, known counterexamples, and what observation or experiment would discriminate among them.
6. [AI] Keep the result at candidate Insight/Learning maturity until support justifies more. Evidence assessment and current official-policy checking are useful related methods when they can materially change confidence or applicability; AURA does not auto-route the claim through them.

## Related operating knowledge
- `seo.intelligence.ecosystem.evidence-grading` can help assess support strength.
- `seo.intelligence.ecosystem.official-contradiction-check` can help check current authoritative rules/guidance.

These are reusable methods, not runtime routing requirements.

## Verification
- Validate canonical objects written and preserve SourceRecord/Observation lineage.
- Keep evidence strength, conclusion confidence, official-policy status, and practical consequence distinct.
- A later external state change is performed through the active model/harness when actually requested and capable. AURA does not require an ActionPacket or other permission object.

## Measurement
- Strategy claims become stronger only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative policy evidence; popularity and confidence language are not outcome evidence.

## Learning
- Maintain SEO-specific strategy knowledge as SEO Domain Learning. Propose broader Business or System Learning only when evidence and applicability justify the broader scope.

## Failure / Fallback
- If a source cannot be retrieved automatically, use another available authoritative source or create a real human/owner handoff when needed. Do not invent missing evidence or an AURA action object for a tool limitation.
- If evidence remains contradictory or insufficient, preserve the uncertainty and keep the claim at hypothesis/experimental maturity instead of forcing a conclusion.

## Completion Criteria
- Outputs use current Core Observation/Insight/Experiment/Learning objects rather than a parallel strategy-evidence store.
- Source provenance, contradictory evidence, applicability, confidence, and official-policy status remain inspectable where material.
- No tactic is promoted, deprecated, blocked, or claimed effective for a reason that cannot be traced to evidence or an actually applicable constraint.
