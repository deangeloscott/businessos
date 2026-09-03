---
id: customer-optimization.intervention.onboarding
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
# Onboarding Optimization

## Purpose
Help new customers reach the first meaningful value state with less confusion, delay, and avoidable effort.

## Business Outcome
Improve onboarding and time-to-value by removing real friction rather than maximizing checklist completion.

## Run When
Use when onboarding progression, setup, implementation, expectation, or time-to-value evidence indicates a material problem or opportunity. An existing Opportunity may provide context but is not required.

## Process
1. [AI] Define the business/customer-specific activation or first meaningful value state and the milestones genuinely required to reach it.
2. [HYBRID] Examine completion, time, drop-off, retries, support, handoffs, implementation delays, and segment differences where available; task completion alone is not success.
3. [AI] Combine behavioral evidence with Customer Insights/support/success evidence to distinguish missing instruction, missing motivation, product/service defect, operational delay, role ambiguity, expectation mismatch, or other plausible causes.
4. [AI] Use the authored onboarding submethods as relevant operating knowledge to simplify sequence, defaults, guidance, ownership, expectations, education, checklists, and escalation around the shortest safe path to value.
5. [AI] If communication, persuasion, customer research, product, sales, or operational expertise is needed, use it directly through the active model/harness. A WorkRequest is only for a real durable organizational handoff.
6. [HYBRID] Define activation/time-to-value, customer-quality, support, retention, and other guardrails proportionate to the intervention; use an experiment only when experimentation materially improves the decision.
7. [HYBRID] If implementation is requested and the host has the real capability/permission, make the relevant product/workflow/process/communication changes directly and verify actual state when useful. Otherwise return the usable design/assets without implying execution.
8. [AI] Preserve only durable meaning that actually occurred and will help future work—such as a changed process, measured outcome, Learning, or updated journey understanding—not a generic lifecycle bundle.

## Completion Criteria
- The organization has an evidence-backed onboarding improvement or usable intervention design focused on real value realization, with execution/outcome state represented truthfully.
