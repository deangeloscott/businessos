---
id: seo.intelligence.ecosystem.claim-extraction
type: workflow
owner_system: seo-aeo
reads:
- SourceRecord
- Observation
- type: Insight
  domain: industry-intelligence
- type: Learning
  domain: seo-aeo
writes:
- Observation
- Insight
- Learning
---
# SEO Strategy Claim Extraction

## Purpose
Convert articles, announcements, experiments, and observed outcomes into atomic, testable SEO/AEO claims with explicit source lineage and applicability.

## Business Outcome
Keep SEO/AEO strategy current and evidence-backed without creating a parallel strategy store or importing another organization's private Learning.

## Run When
Use when a SourceRecord/Observation may contain a material SEO/AEO strategy claim worth understanding or preserving.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, one business result, or model confidence as a validated tactic by itself. Do not use another organization's private AURA state as evidence for the active organization.

## Process
1. [AI] Read the source in context and separate direct platform announcement, measured result, author inference, recommendation, and speculation.
2. [AI] Extract one atomic claim at a time; state the claimed mechanism, expected outcome, affected surface, and applicability conditions without combining unrelated assertions.
3. [DETERMINISTIC] Preserve the originating SourceRecord/Observation plus source type, date, reported method/sample, and material commercial/conflict-of-interest context when present. Deterministic AURA verifies references; it does not decide the claim's semantic meaning.
4. [AI] Paraphrase rather than over-copying source text while retaining enough source reference for a capable reviewer to verify the interpretation.
5. [AI] Identify prerequisite mechanisms, alternative explanations, known counterexamples, and what observation or experiment could distinguish among them.
6. [AI] Keep the result at the narrowest useful candidate Insight/Learning maturity until support justifies more. Evidence assessment and current official-policy checking are optional related methods when they can materially change confidence or applicability.

## Related operating knowledge
- `seo.intelligence.ecosystem.evidence-grading` can help assess support strength.
- `seo.intelligence.ecosystem.official-contradiction-check` can help check current authoritative rules/guidance.
- `seo.learning.strategy-experiment-design` can help when testing would materially reduce important uncertainty.

These are reusable methods, not runtime routing requirements.

## Verification
- Canonical objects written are valid and SourceRecord/Observation lineage is preserved.
- Evidence strength, conclusion confidence, official-policy status, and practical consequence remain distinct.
- No private state from another organization is implicitly consumed.
- A later external state change is performed by the active model/harness when actually requested and capable; AURA does not require an execution/permission packet.

## Measurement
- Strategy claims strengthen only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative evidence—not popularity or confidence language alone.

## Learning
- Maintain reusable SEO-specific guidance as organization-owned SEO Domain Learning. Business Learning is appropriate only when evidence supports organization-wide applicability. Cross-organization reuse uses explicit Innovation Exchange/export/adoption or deliberate AURA product-development work.

## Failure / Fallback
- If a source cannot be retrieved automatically, use another valid source/method when practical or preserve the unresolved evidence need honestly.
- If evidence remains contradictory or insufficient, preserve uncertainty and keep the claim at the narrowest supported maturity.

## Completion Criteria
- Material SEO/AEO claims are atomic, traceable, testable where appropriate, organization-isolated, and no stronger than their evidence supports.
