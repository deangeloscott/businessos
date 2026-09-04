---
id: customer-optimization.intervention.activation
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  domain: customer-intelligence
- MetricObservation
writes: []
context:
- EconomicContext
- Offer
---
# Activation Optimization

## Purpose
Increase the share of acquired customers reaching an evidence-backed early value behavior predictive of durable success.

## Business Outcome
Improve early customer value realization without inflating a convenient event that does not predict later success.

## Run When
Use when evidence suggests activation or the path to first meaningful value is a material customer/business constraint. An Opportunity may provide context but is not required.

## Process
1. [HYBRID] Validate the activation definition against later value/retention rather than choosing a convenient event.
2. [HYBRID] Analyze path/time to activation, prerequisite behaviors, cohort differences, and drop-off using the strongest available evidence.
3. [AI] Identify plausible barriers such as setup, knowledge, missing data/integration, unclear next step, poor fit, product/process failure, or delayed external dependency. Keep unsupported causes as hypotheses.
4. [AI] Prioritize the smallest interventions likely to improve true activation/customer value rather than merely increasing event counts.
5. [HYBRID] If execution is requested and the host has the real capability/permission, implement the appropriate workflow/product/process/communication change directly. Otherwise return the actionable intervention design or create a WorkRequest only for a real durable handoff.
6. [HYBRID] Check instrumentation and define/observe downstream retention, success, support, and customer-experience evidence proportionate to the decision.
7. [AI] Preserve only durable meanings that actually occurred and will help future work—for example a material change, experiment, outcome, Learning, or updated journey understanding. Do not create a generic lifecycle bundle merely because this playbook ran.

## Completion Criteria
- The activation mechanism and intervention are evidence-bounded and useful, execution state is truthful, and any retained AURA state corresponds to something that actually occurred.
