# Competitor Intelligence

Maintain evidence-backed competitor understanding and interpret pricing, positioning, Offers, funnels, messaging, customer sentiment, capabilities, strategic movement, and credible implications.

## Common jobs
- Discover or refine the relevant competitive set → `workflows/discovery/`
- Profile or compare competitors → `workflows/analysis/`
- Broad competitive position/landscape → `competitor.analysis.competitive-position`
- Pricing, packaging, positioning, messaging, Offers, capabilities, and tactical evidence → the relevant method under `workflows/analysis/` or `workflows/research/`
- Detect or understand material competitor changes → `workflows/monitoring/` and related analysis methods
- Evaluate whether an observed tactic appears effective → `competitor.analysis.tactic-validation`
- Translate evidence into scoped business implications → `competitor.analysis.competitive-implications`
- Reusable Competitor Learning → `workflows/learning/`

## Boundary
Competitor Intelligence preserves competitor evidence and decision-useful interpretation. It does not automatically create foreign-domain Opportunities, relevance signals, WorkRequests, or routed actions. Other work may directly consume the same evidence and Insights when relevant.

Observed competitor behavior, inferred strategy, proxy performance signals, and actual evidence of effectiveness must remain separate. The active model/user decides what the evidence means for the current business decision and which method, if any, is useful next.

## AI execution
Do not load this entire system. Retrieve the smallest relevant context and choose, combine, adapt, skip, or replace useful methods with model/user judgment. `process-map.json` is a lightweight browse/navigation index, not runtime execution order or a Workflow graph.
