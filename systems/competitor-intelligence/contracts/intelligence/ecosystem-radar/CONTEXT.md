---
id: competitor.intelligence.ecosystem-radar
type: playbook
owner_system: competitor-intelligence
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
    when: A known competitor surface may have materially changed and model/user judgment says change comparison is useful.
  - id: competitor.analysis.tactic-validation
    when: Evidence suggests a competitor tactic may be effective rather than merely present and effectiveness matters to the decision.
---
# Competitive Ecosystem Radar

## Purpose
Discover important competitor entrants, movements, tactics, and strategic signals while separating observed competitor behavior from unsupported claims that the behavior works.

## Business Outcome
Improve competitive understanding and response quality without copying competitors, overreacting to noise, or mistaking visible activity for causal success.

## Run When
Use on demand for competitive refresh or when evidence suggests the competitive environment may have materially changed.

## Process
1. [HYBRID] Reuse the current competitive set, source identities, snapshots, Insights, Learnings, and recent evidence before searching again. The model decides which competitors/surfaces are stale or relevant; deterministic code may compare exact dates/refs but does not decide business materiality.
2. [AI] Search the competitor dimensions that can change the current decision: entry/exit, pricing/package/product/offer changes, positioning/message shifts, funnels/channels, campaigns, partnerships, hiring/geography signals, substitutes, or other relevant behavior.
3. [HYBRID] Verify entity identity from evidence, preserve direct observations, and use snapshot/change comparison or Core triangulation where useful. Exact URL/hash reuse may be deterministic; real-world identity remains model judgment.
4. [AI] Keep three propositions separate: what the competitor demonstrably did, what strategy/mechanism that may imply, and whether credible evidence shows the tactic produced an outcome.
5. [HYBRID] Use independent evidence, timing, repeated behavior, external outcomes, and `competitor.analysis.tactic-validation` when effectiveness matters. One competitor's apparent success never becomes a universal best practice.
6. [AI] Evaluate relevance to the active business by the actual customer choice set, market, offer, capabilities, economics, Objective, and response options rather than imitation value.
7. [AI] Decide what the evidence warrants next: update competitor understanding, watch, investigate, test a hypothesis, consider a business response, or do nothing. Other AURA playbooks may be useful methods, but this radar does not route work to semantic owners or manufacture Opportunities/WorkRequests.
8. [DETERMINISTIC] Persist only material Observation/Insight evidence and exact references chosen by the model/user. Reusable Learning changes occur through the appropriate evidence-based Learning path when genuinely justified, not automatically after a radar cycle.

## Verification
- Observed behavior, inferred strategy, and evidence of effectiveness remain distinct.
- Competitor aliases and duplicate reports do not inflate evidence; semantic entity merges require model judgment.
- Suggested next work is guidance, not AURA-owned routing state.

## Completion Criteria
- Important competitive signals are evidence-backed and scoped to what is known, with material implications/unknowns clear and no unsupported effectiveness or automatic-routing claim.
