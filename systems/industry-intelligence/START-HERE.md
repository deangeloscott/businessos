# Industry Intelligence

Detect external developments that should change a business decision, risk, opportunity, or communication.

## Common jobs
- News/regulation/research/technology/market monitoring → `contracts/monitoring/`
- Public industry/social discussion watch → `industry.monitoring.social-discussion`
- Cluster/verify evolving event → event/analysis contracts
- Materiality, threat, opportunity, scenario → `contracts/analysis/`
- Explain “what happened” vs “what it means for this audience” → `industry.analysis.audience-implication`
- Delegate an approved Industry response to Content → `industry.handoff.content-response`

## Boundary
Industry Intelligence owns external developments and broad implications. Social discussion is a signal, not factual verification. Content Synthesis owns how the final message is expressed; other domains decide their own response.

## AI execution
Do not load this entire system. Route to one atomic contract and use the root Context Planner.

## Complete process map
`process-map.json` lists the common important activities this system claims to perform. Use `python scripts/process_plan.py --system industry-intelligence --activity <activity-id>` to expand a composite activity into its required and conditional sub-processes.
