---
id: customer-optimization.monitoring.journey-health
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- MetricObservation
- Observation
- ChangeEvent
- Learning
writes:
- Observation
- Insight
- Incident
- Opportunity
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - checkout.read
  - billing.read
  - customer_success.read
---
# Customer Journey Health Monitoring

## Purpose
Review customer progression, delays, failure states, and downstream value for material deterioration or improvement without making AURA the monitoring runtime.

## Business Outcome
Keep customer-journey understanding current enough to identify meaningful improvement opportunities or harm while avoiding alert noise and scheduler duplication.

## Run When
Use for a bounded journey-health review when the user requests it, when saved monitoring intent indicates another review would be useful, or after a material product/process/offer change. Any recurring execution is owned by the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve the relevant transition metrics, time-to-stage, failure/error, retention/renewal/expansion, and guardrail evidence from the strongest available operational/measurement systems.
2. [HYBRID] Compare recent, prior, seasonal/cohort, and expected ranges at relevant segment/offer/channel dimensions, accounting for sample size and data quality.
3. [HYBRID] Separate instrumentation/data-health changes from real customer behavior before interpreting movement.
4. [AI] Identify affected transition scope and recent material organizational/external context that may explain movement.
5. [AI] Judge whether the evidence is normal variation, worth watching, a plausible Optimization Opportunity, or a genuine Incident. Preserve only the durable object whose meaning actually occurred; do not manufacture lifecycle state merely because a metric moved.
6. [HYBRID] Preserve material Observations/Insights and, when warranted, an Opportunity or Incident with evidence lineage. Repeated unchanged reviews should update relevant checkpoints/context rather than create duplicate findings or runtime events.

## Verification
- Material findings are traceable to actual measurement/operational evidence.
- Data-quality problems remain distinct from customer-behavior conclusions.
- AURA may preserve monitoring intent but does not claim a recurring job exists unless the external runtime actually created it.
- No workflow/customer change is executed merely because monitoring found a signal.
