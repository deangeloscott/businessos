# Competitor Intelligence

Maintain evidence-backed competitor understanding and interpret pricing, positioning, offers, funnels, messaging, customer sentiment, capabilities, strategic movement, and credible implications.

## Common jobs
- Discover/profile the relevant competitive set → `contracts/discovery/` / `contracts/analysis/profiling/`
- Broad competitive position/landscape → `competitor.analysis.competitive-position`
- Pricing, packaging, positioning, messaging, offers, capabilities → `contracts/analysis/`
- Detect/understand material competitor changes → monitoring/change analysis methods
- Evaluate whether an observed tactic appears effective → `competitor.analysis.tactic-validation`
- Translate evidence into scoped business implications → `competitor.analysis.competitive-implications`
- Reusable Competitor Learning → `competitor.learning.domain-learning`

## Boundary
Competitor Intelligence preserves competitor evidence and decision-useful interpretation. It does not automatically create foreign-domain Opportunities, relevance signals, WorkRequests, or routed actions. Other work may directly consume the same evidence/Insights when relevant.

Observed competitor behavior, inferred strategy, and evidence of effectiveness must remain separate. The active model/user decides what the evidence means for the current business decision and which method is useful next.

## AI execution
Do not load this entire system. Retrieve the smallest relevant context and choose/adapt the useful method with model/user judgment. `process-map.json` is a browse/composition aid, not runtime execution order.
