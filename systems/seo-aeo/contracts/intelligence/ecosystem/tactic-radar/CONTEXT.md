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
    when: A promising uncertain tactic is testable and an experiment would materially improve the decision.
  - id: seo.learning.tactic-registry
    when: New evidence materially changes SEO Domain Learning and the model/user chooses to update it.
---
# SEO/AEO Ecosystem Tactic Radar

## Purpose
Discover and evaluate emerging SEO/AEO mechanisms, tactics, platform changes, practitioner findings, and research without automatically promoting them into an experiment or Learning lifecycle.

## Business Outcome
Keep organic and AI-answer discovery strategy current without blindly copying popular tactics, confusing policy with effectiveness, or turning AURA into an SEO routing engine.

## Run When
Use on demand for SEO/AEO refresh or when a material search/answer-platform change or tactic claim could affect the business.

## Process
1. [HYBRID] Reuse current SEO evidence, Domain Learning, official guidance, experiments/outcomes, and SourceProfiles before requesting fresh discovery.
2. [AI] Define the SEO/AEO mechanisms/surfaces relevant to the decision, such as crawling/indexing, architecture, on-page relevance, authority, local discovery, entities, answer visibility/citations, demand, or conversion alignment.
3. [HYBRID] Use SEO claim extraction, Core triangulation, and SEO evidence grading to separate original tests, independent replications, echoes, counterevidence, policy statements, correlations, and speculation.
4. [HYBRID] Check current official policy/eligibility separately from whether a tactic appears effective; popularity, competitor adoption, or one business result never establishes a standard tactic.
5. [AI] Evaluate applicability to the active business from the actual market, site/assets, baseline, search/answer surface, prerequisites, authority, expected business mechanism, downside, and measurement feasibility. Do not invent economics or impact.
6. [AI] Decide the narrowest useful disposition: ignore, remember, watch, investigate, experiment, apply a sufficiently supported tactic, revise Learning, or do nothing. `seo.learning.strategy-experiment-design` and the Learning playbooks are optional methods the model/user may select, not automatic next routes.
7. [DETERMINISTIC] Persist only material SEO Insight/evidence meaning and exact references chosen by the model/user. If Learning is changed, use the Learning path after semantic judgment; deterministic AURA validates/persists rather than deciding maturity/applicability.
8. [AI] Return prioritized findings with freshness, novelty, independent evidence, contradictions, policy status, business relevance, uncertainty, and any suggested next method.

## Verification
- Evidence strength, conclusion confidence, official-policy status, and business applicability remain distinct.
- Viral discussion volume is never counted as independent validation.
- No tactic is automatically promoted, deprecated, experimented on, or routed because the radar observed it.

## Completion Criteria
- Material SEO/AEO discoveries have evidence-calibrated interpretation and business relevance, with the next method left to capable model/user judgment.
