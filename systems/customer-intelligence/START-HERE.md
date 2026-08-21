# Customer Intelligence

Understand what customers/prospects want, need, believe, ask, choose, reject, complain about, and value.

## Common jobs
- Voice of customer / recurring themes → `contracts/analysis/`
- Win/loss → `customer.analysis.win-loss`
- Churn reasons → `customer.analysis.churn`
- Interviews, surveys, CRM, support, reviews → `contracts/evidence-collection/`
- Public social/forum/review conversation → `customer.evidence-collection.public-conversation`
- Public/customer sentiment and theme change → `customer.analysis.sentiment-themes`
- Extract testimonial/before-after proof → `customer.analysis.before-after-proof`
- Link a public signal to a known CRM customer only when explicit/authorized → `customer.analysis.subject-linkage`
- Continuously watch public customer signals → `customer.monitoring.public-signal-watch`
- New/changed Insight relevance → `contracts/intelligence/`

## Boundary
Customer Intelligence interprets customer evidence; it does not own persuasion, content production, competitor truth, journey mechanics, or product decisions. Public evidence is not permission for invasive identity profiling. Reusable testimonial/results evidence becomes a shared ProofRecord.

## AI execution
Do not load this entire system. Route to one atomic contract and use the root Context Planner.

## Complete process map
`process-map.json` lists the common important activities this system claims to perform. Use `python scripts/process_plan.py --system customer-intelligence --activity <activity-id>` to expand a composite activity into its required and conditional sub-processes.
