---
id: seo.intelligence.ecosystem.tactic-radar
type: playbook
owner_system: seo-aeo
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
- Experiment
- OutcomeEvaluation
writes:
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - research.web.read
  optional:
  - search.observe
  - search.performance.read
  - search.rank.read
  - ai_answer.observe
  - news.read
  - community.read
  - social.observe
context:
- Business
- Market
- Objective
- ProductService
subcontracts:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  - id: seo.intelligence.ecosystem.claim-extraction
  - id: seo.intelligence.ecosystem.evidence-grading
  - id: seo.intelligence.ecosystem.official-contradiction-check
  conditional:
  - id: seo.learning.strategy-experiment-design
    when: A promising uncertain tactic is testable, material, policy-allowed, and applicable to eligible owned assets.
  - id: seo.learning.tactic-registry
    when: Evidence or an experiment materially changes SEO Domain Learning.
  - id: seo.learning.tactic-promotion
    when: Evidence may justify stronger maturity or standard guidance.
  - id: seo.learning.tactic-deprecation
    when: Evidence, policy, or outcomes materially weaken an active tactic.
---
# SEO/AEO Ecosystem Tactic Radar

## Purpose
Discover and evaluate emerging SEO/AEO mechanisms, tactics, platform changes, practitioner findings, and research, then route the few that matter into the existing SEO experiment and Learning lifecycle.

## Business Outcome
Keep organic and AI-answer discovery strategy current without blindly copying popular tactics or rebuilding the existing SEO evidence system.

## Run When
Run from the Core ecosystem radar, on demand for SEO/AEO refresh, or when a material search/answer-platform change or tactic claim appears.

## Process
1. [HYBRID] Reuse current SEO ecosystem monitoring, domain Learnings, official guidance, experiments, and Core SourceProfiles before requesting fresh discovery.
2. [AI] Define relevant SEO/AEO mechanisms and surfaces such as crawling/indexing, architecture, on-page relevance, authority, local discovery, entities, answer visibility/citations, demand, and conversion alignment; use Core discovery to find both known-source updates and semantically related new sources.
3. [HYBRID] Extract atomic claims with the existing SEO claim-extraction contract, then use Core triangulation plus SEO evidence grading to distinguish original tests, independent replications, echoes, counterevidence, policy statements, correlations, and speculation.
4. [HYBRID] Check current official policy/eligibility separately from whether a tactic appears effective; popularity, competitor adoption, or one business result never establishes a standard tactic.
5. [AI] Evaluate applicability to the active business by market, site/asset type, current baseline, search/answer surface, technical prerequisites, authority, expected business value, cost, risk, and ability to measure a meaningful effect.
6. [HYBRID] Route weak/noisy claims to ignore/watch, material evidence gaps to bounded investigation, and promising uncertain low-enough-risk claims to `seo.learning.strategy-experiment-design`.
7. [DETERMINISTIC] After experiment/outcome evidence, update the existing tactic registry/domain Learning and use promotion/deprecation only at the narrowest maturity/applicability justified.
8. [AI] Return prioritized SEO/AEO findings with freshness, novelty, independent evidence, contradictions, policy status, business relevance, and the exact next route.

## Verification
- Existing SEO evidence/experiment/Learning contracts remain authoritative; this radar orchestrates them rather than duplicating them.
- Viral discussion volume is never counted as independent validation.

## Completion Criteria
- Every material SEO/AEO discovery is ignored, watched, investigated, tested, or routed into existing Learning with an evidence-backed reason.
