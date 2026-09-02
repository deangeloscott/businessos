---
id: customer-optimization.adoption.path-design
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Observation
- Insight
- Opportunity
- MetricObservation
- Experiment
writes:
- Observation
- Insight
- Opportunity
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Adoption Path Design

## Purpose
Define how customers progress from first value to sustained use of the capabilities/actions required for their desired outcomes.

## Business Outcome
Increase durable value realization without optimizing feature usage for its own sake.

## Run When
Run when customers activate but fail to adopt behaviors/capabilities necessary for ongoing success.

## Process
1. [AI] Define target customer outcome and the minimum recurring/advanced capabilities or behaviors causally/reliably associated with it.
2. [DETERMINISTIC] Map current adoption states, prerequisite skills/configuration/data, usage patterns, barriers, and successful-customer paths.
3. [AI] Sequence adoption milestones by customer value/dependency rather than product menu order.
4. [AI] Identify where simplification, defaults, in-product guidance, Content, Customer Success, or product/process change is needed.
5. [HYBRID] Avoid forcing usage that does not improve customer outcomes or inflating “adoption” by meaningless clicks.
6. [DETERMINISTIC] Define milestone instrumentation, success/guardrail metrics, timing, and segment variations.
7. [AI] Create intervention plan and evaluate downstream value/retention, not feature usage alone.
