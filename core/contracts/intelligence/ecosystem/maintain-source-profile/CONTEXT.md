---
id: core.intelligence.ecosystem.maintain-source-profile
type: playbook
owner_system: core
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
Maintain business-scoped source/watch history and optional resolved-subject grouping that improves future research attention without turning reputation or popularity into evidence.

## Business Outcome
Spend future research effort more intelligently, reuse durable watches across domains, and preserve claim-by-claim verification without creating a universal source trust score or a second semantic owner.

## Run When
Run when a source is newly discovered, a subject/source is intentionally watched, its monitoring usefulness changes, or traceable later evidence materially updates its fact-type-specific history.

## Process
1. [DETERMINISTIC] Resolve the canonical SourceProfile by normalized source reference and reuse it instead of creating duplicate profiles for aliases or trailing URL variants.
2. [HYBRID] When the source has been explicitly resolved to a real-world subject, record `subject_key`, subject kind/name/relationship, modality, and decision-relevant monitoring questions/signals. Reuse the same subject key across confirmed related public profiles; never merge namesakes or ambiguous identities on name similarity alone.
3. [HYBRID] Record source kind, relevant domains/topics, watch status, and attention priority based on discovery utility, directness, fact-type expertise, timeliness, access stability, decision relevance, and evidenced historical usefulness.
4. [DETERMINISTIC] Record a source-history outcome only when linked to a concrete evidence reference; deduplicate repeated outcome events so reruns do not inflate support/contradiction counts.
5. [AI] Keep fact-type assessments separate: strong history for official policy, technical measurement, customer observation, or causal experimentation must not automatically transfer to unrelated claims.
6. [HYBRID] Treat follower count, engagement, prestige, virality, and prior correctness as discovery priors only; never use SourceProfile history as support for a current Insight.
7. [DETERMINISTIC] Prefer `scripts/upsert_source_profile.py` for persistence, preserve business isolation, and never store credentials or unnecessary private personal data.
8. [HYBRID] Deprioritize or block sources for persistent duplication, inaccessibility, poor methods, deceptive provenance, or repeated contradiction only when traceable history supports that operational decision.

## Verification
- Every historical support/contradiction count can be traced to deduplicated evidence refs.
- Related source profiles share a subject key only when identity resolution is sufficiently supported.
- No field is interpreted as a universal truth or credibility score.

## Completion Criteria
- SourceProfile reflects current discovery/monitoring utility, subject relationship when known, modality, and fact-type-specific history without altering the evidentiary status of unrelated claims.
