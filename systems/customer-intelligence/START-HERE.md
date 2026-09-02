# Customer Intelligence

Understand what customers/prospects want, need, believe, ask, choose, reject, complain about, experience, and value from evidence appropriate to the question.

## Common jobs
- Voice of customer, recurring themes, sentiment, win/loss, churn, objections, or proof analysis → `workflows/analysis/`
- Interviews, surveys, CRM, support, reviews, public conversation, and other evidence collection → `workflows/evidence-collection/`
- Broader or method-specific customer research → `workflows/research/`
- Customer-signal ecosystem review → `workflows/intelligence/`
- Bounded customer/public-signal monitoring → `workflows/monitoring/`
- Reusable Customer Intelligence Learning → `workflows/learning/`
- Establish or refresh customer-intelligence starting context when useful → `workflows/bootstrap/`

Useful specific methods include `customer.analysis.win-loss`, `customer.analysis.churn`, `customer.analysis.sentiment-themes`, `customer.analysis.before-after-proof`, `customer.analysis.insight-refresh`, `customer.evidence-collection.public-conversation`, and `customer.intelligence.ecosystem-radar`.

## Boundary
Customer Intelligence interprets customer evidence; it does not own persuasion, content production, competitor truth, journey mechanics, product decisions, or a cross-domain relevance router. Public evidence is not permission for invasive identity profiling. Reusable testimonial/results evidence may become a shared `ProofRecord` when its evidence and rights support that use.

Other work may directly consume relevant Customer Insights. No relevance event or WorkRequest is required merely to use shared organizational knowledge. Monitoring intent can be remembered; the harness owns recurrence and notifications.

## AI execution
Do not load this entire system. Retrieve the smallest relevant context and choose, combine, adapt, skip, or replace useful methods with model/user judgment. `process-map.json` is a browse/composition aid, not runtime execution order.
