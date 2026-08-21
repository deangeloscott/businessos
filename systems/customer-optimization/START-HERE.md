# Customer Optimization

Improve how customers progress from interest through purchase, onboarding, success, retention, repeat, expansion, and referral.

## Common jobs
- Map/instrument journey → `contracts/journey/`
- Diagnose friction/dropoff → `contracts/diagnosis/`
- Checkout/onboarding/activation/retention/etc. → `contracts/intervention/`
- Experiment/monitor/measure → corresponding contract families

## Boundary
Read `DEFAULTS.md` before authoring or modifying domain contracts. Cross-domain facts should be consumed from their canonical owner; delegated work uses WorkRequest rather than a duplicate Opportunity.

## AI execution
Do not load this entire system. Route to one atomic contract and use the root Context Planner.

## Complete process map
`process-map.json` lists the common important activities this system claims to perform. Use `python scripts/process_plan.py --system customer-optimization --activity <activity-id>` to expand a composite activity into its required and conditional sub-processes.
