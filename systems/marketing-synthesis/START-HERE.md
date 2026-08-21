# Marketing Synthesis

Turn intelligence, Offer, proof, objections, and awareness into commercial persuasion and conversion assets.

## Common jobs
- Diagnose persuasion barrier → `contracts/diagnosis/`
- Positioning/messaging/value proposition → corresponding top-level families
- Landing page/VSL/webinar/email/ads/etc. → `contracts/assets/`
- Experiment and evaluate → `contracts/experimentation/` / `measurement/`

## Boundary
Read `DEFAULTS.md` before authoring or modifying domain contracts. Cross-domain facts should be consumed from their canonical owner; delegated work uses WorkRequest rather than a duplicate Opportunity.

## AI execution
Do not load this entire system. Route to one atomic contract and use the root Context Planner.

## Complete process map
`process-map.json` lists the common important activities this system claims to perform. Use `python scripts/process_plan.py --system marketing-synthesis --activity <activity-id>` to expand a composite activity into its required and conditional sub-processes.
