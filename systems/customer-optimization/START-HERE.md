# Customer Optimization

Improve how customers progress from interest through purchase, onboarding, success, retention, repeat, expansion, referral, and recovery while protecting real customer value.

## Common jobs
- Map/instrument a customer journey → `contracts/journey/`
- Diagnose friction/dropoff/root cause → `contracts/diagnosis/`
- Design or execute checkout/onboarding/activation/retention/etc. improvements → `contracts/intervention/`
- Improve a real sales/customer handoff → `customer-optimization.intervention.sales-handoff`
- Bounded journey/churn monitoring reviews → `contracts/monitoring/`
- Measure transitions, time-to-value, value, and outcomes → `contracts/measurement/`
- Reusable Customer Optimization Learning → `customer-optimization.learning.domain-learning`

## Boundary
Customer Optimization owns journey/progression/value-realization operating knowledge, not customer psychology truth, generic persuasion, or the external CRM/product/billing runtime. Reuse Customer/Marketing/Offer/measurement evidence directly where relevant.

A WorkRequest is not needed to move reasoning between AURA domains. Use one only for a real durable organizational handoff. The harness/external systems own workflow execution, customer messaging, scheduling, account permissions, and operational automation.

## AI execution
Do not load this entire system. Retrieve the smallest relevant context and choose/adapt the useful method with model/user judgment. `process-map.json` is a browse/composition aid, not runtime execution order.
