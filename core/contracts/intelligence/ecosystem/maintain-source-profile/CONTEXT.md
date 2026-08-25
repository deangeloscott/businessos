---
id: core.intelligence.ecosystem.maintain-source-profile
type: service
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- OutcomeEvaluation
writes:
- SourceProfile
capabilities:
  required:
  - none
  optional:
  - none
---
# Maintain External Source Profile

## Purpose
Maintain business-scoped source watch history that improves future discovery attention without turning reputation or popularity into evidence.

## Business Outcome
Spend future research effort more intelligently while preserving claim-by-claim verification and avoiding universal source trust scores.

## Run When
Run when a source is newly discovered, its monitoring usefulness changes, or traceable later evidence materially updates its fact-type-specific history.

## Process
1. [DETERMINISTIC] Resolve the canonical SourceProfile by normalized source reference and reuse it instead of creating duplicate profiles for aliases or trailing URL variants.
2. [HYBRID] Record source kind, relevant domains/topics, watch status, and attention priority based on discovery utility, directness, fact-type expertise, timeliness, access stability, and evidenced historical usefulness.
3. [DETERMINISTIC] Record a source-history outcome only when linked to a concrete evidence reference; deduplicate repeated outcome events so reruns do not inflate support/contradiction counts.
4. [AI] Keep fact-type assessments separate: strong history for official policy, technical measurement, customer observation, or causal experimentation must not automatically transfer to unrelated claims.
5. [HYBRID] Treat follower count, engagement, prestige, virality, and prior correctness as discovery priors only; never use SourceProfile history as support for a current Insight.
6. [DETERMINISTIC] Prefer `scripts/upsert_source_profile.py` for persistence, preserve business isolation, and never store credentials or unnecessary private personal data.
7. [HYBRID] Deprioritize or block sources for persistent duplication, inaccessibility, poor methods, deceptive provenance, or repeated contradiction only when the traceable history supports that operational decision.

## Verification
- Every historical support/contradiction count can be traced to deduplicated evidence refs.
- No field is interpreted as a universal truth or credibility score.

## Completion Criteria
- SourceProfile reflects current discovery utility and fact-type-specific history without altering the evidentiary status of unrelated claims.
