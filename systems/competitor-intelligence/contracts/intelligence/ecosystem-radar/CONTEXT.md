---
id: competitor.intelligence.ecosystem-radar
type: playbook
version: 1.0.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 4
reads:
- Competitor
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
writes:
- Observation
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - social.observe
  - news.read
  - search.observe
context:
- Business
- Market
- Objective
- ProductService
subcontracts:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  conditional:
  - id: competitor.monitoring.material-change
    when: A known competitor surface may have materially changed.
  - id: competitor.analysis.tactic-validation
    when: Evidence suggests a competitor tactic may be effective rather than merely present.
  - id: competitor.learning.domain-learning
    when: Repeated outcomes or corrections justify reusable competitor-intelligence guidance.
---
# Competitive Ecosystem Radar

## Purpose
Discover important competitor entrants, movements, tactics, and strategic signals while separating observed competitor behavior from unsupported claims that the behavior works.

## Business Outcome
Improve competitive response speed and quality without copying competitors, overreacting to noise, or mistaking visible activity for causal success.

## Run When
Run from the Core ecosystem radar, on demand for competitive refresh, or when market evidence suggests a competitor or competitive pattern changed materially.

## Process
1. [DETERMINISTIC] Reuse the current competitive set, source identities, snapshots, Insights, and Learnings; identify stale competitors/surfaces and open discovery gaps.
2. [AI] Search for competitor entry/exit, pricing/package/product/offer changes, positioning/message shifts, funnels/channels, campaigns, partnerships, hiring/geography signals, and new substitute behavior using known and open semantic discovery.
3. [HYBRID] Verify entity identity and preserve direct observations; use snapshot/material-change monitoring where appropriate and Core triangulation for reported strategic claims or purported results.
4. [AI] Separate three propositions: what the competitor demonstrably did, what strategy/mechanism that may imply, and whether credible evidence shows the tactic produced a useful outcome.
5. [HYBRID] Use independent evidence, timing, repeated behavior, external outcomes, and `competitor.analysis.tactic-validation` before inferring effectiveness; one competitor's success never becomes a universal best practice.
6. [AI] Evaluate relevance to the active business by customer choice set, market, offer, capabilities, economics, objectives, and likely response options rather than imitation value.
7. [HYBRID] Route observed changes to canonical Competitor/Insight updates, broader customer/industry/marketing implications to their owners, and only material response opportunities to Core Opportunity qualification.
8. [DETERMINISTIC] Feed later prediction accuracy, missed changes, false positives, and tactic-interpretation outcomes into competitor domain Learning and source-profile history.

## Verification
- Observed behavior, inferred strategy, and proven effectiveness remain separate evidence states.
- Competitive source aliases and duplicated reports do not inflate evidence.

## Completion Criteria
- Important competitive signals are verified, scoped, and routed without unsupported effectiveness claims.
