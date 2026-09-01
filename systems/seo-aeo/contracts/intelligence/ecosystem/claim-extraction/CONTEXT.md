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
Keep SEO/AEO strategy current, evidence-governed, policy-safe, and connected to measurable organic and business outcomes without creating a parallel strategy-evidence store.

## Run When
Run when a new SourceRecord/Observation may contain a material SEO/AEO strategy claim.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless Core System Learning governance explicitly permits it.

## Process
1. [AI] Read the source in context and separate direct platform announcement, measured result, author inference, recommendation, and speculation.
2. [HYBRID] Extract one atomic claim at a time; state the claimed mechanism, expected outcome, affected surface, and applicability conditions without combining unrelated assertions.
3. [DETERMINISTIC] Attach the originating SourceRecord/Observation and record source type, date, method/sample when reported, and material commercial/conflict-of-interest context.
4. [HYBRID] Paraphrase rather than over-copying source text while retaining enough source reference for a human to verify the interpretation.
5. [AI] Identify prerequisite mechanisms, alternative explanations, known counterexamples, and what observation or experiment would discriminate among them.
6. [HYBRID] Route claims to evidence assessment and official-policy contradiction checking; create only a candidate Insight/Learning hypothesis until sufficient support exists.

## Decisions / Routing
- Route evidence assessment → `seo.intelligence.ecosystem.evidence-grading`.
- Route policy check → `seo.intelligence.ecosystem.official-contradiction-check`.

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
