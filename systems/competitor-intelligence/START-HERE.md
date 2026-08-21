# Competitor Intelligence

Maintain evidence-backed competitor state and interpret pricing, positioning, offers, funnels, messaging, customer sentiment, and strategic movement.

## Common jobs
- Discover/profile competitors → `contracts/discovery/` / `profiling/`
- Pricing, packaging, positioning, messaging, offers → `contracts/analysis/`
- Competitor change → `contracts/change-detection/`
- What appears to work → `contracts/tactic-validation/`
- Competitive whitespace → `contracts/whitespace/`

## Boundary
Read `DEFAULTS.md` before authoring or modifying domain contracts. Cross-domain facts should be consumed from their canonical owner; delegated work uses WorkRequest rather than a duplicate Opportunity.

## AI execution
Do not load this entire system. Route to one atomic contract and use the root Context Planner.

## Complete process map
`process-map.json` lists the common important activities this system claims to perform. Use `python scripts/process_plan.py --system competitor-intelligence --activity <activity-id>` to expand a composite activity into its required and conditional sub-processes.
