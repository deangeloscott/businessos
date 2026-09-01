# Customer Intelligence

Understand what customers/prospects want, need, believe, ask, choose, reject, complain about, experience, and value from evidence appropriate to the question.

## Common jobs
- Voice of customer / recurring themes → `contracts/analysis/`
- Win/loss → `customer.analysis.win-loss`
- Churn reasons → `customer.analysis.churn`
- Interviews, surveys, CRM, support, reviews → `contracts/evidence-collection/`
- Public social/forum/review conversation → `customer.evidence-collection.public-conversation`
- Sentiment/theme evidence → `customer.analysis.sentiment-themes`
- Testimonial/before-after proof → `customer.analysis.before-after-proof`
- Link a public signal to a known CRM customer only when identity resolution and the real use are justified → `customer.analysis.subject-linkage`
- Bounded public-signal review → `customer.monitoring.public-signal-watch`
- Refresh an existing Customer Insight against new evidence → `customer.analysis.insight-refresh`
- External/customer signal ecosystem review → `customer.intelligence.ecosystem-radar`
- Reusable research-method Learning → `customer.learning.domain-learning`

## Boundary
Customer Intelligence interprets customer evidence; it does not own persuasion, content production, competitor truth, journey mechanics, product decisions, or a cross-domain relevance router. Public evidence is not permission for invasive identity profiling. Reusable testimonial/results evidence may become a shared `ProofRecord` when its evidence/rights support that use.

Other work may directly consume relevant Customer Insights. No relevance event or WorkRequest is required merely to use shared organizational knowledge. Monitoring intent can be remembered; the harness owns recurrence/notifications.

## AI execution
Do not load this entire system. Retrieve the smallest relevant context and choose/adapt the useful method with model/user judgment. `process-map.json` is a browse/composition aid, not runtime execution order.
