---
id: customer-optimization.intervention.churn
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
# Churn Diagnosis & Prevention

## Purpose
Identify actionable churn mechanisms and reduce avoidable customer loss while respecting non-fit/healthy churn.

## Business Outcome
Improve durable customer value/continuation by addressing supported churn mechanisms rather than indiscriminate retention pressure.

## Run When
Use when churn, cancellation, non-renewal, or meaningful retention risk is a material business/customer problem. An existing Opportunity may provide context but is not required.

## Process
1. [HYBRID] Define the churn/renewal event, relevant horizon, cohorts, and voluntary/involuntary distinctions where they matter.
2. [HYBRID] Examine preceding product/service behavior, support, billing, success milestones, engagement, contract/timing, segment patterns, and customer-stated evidence using the strongest available sources.
3. [AI] Combine stated churn reasons with behavioral predictors without treating predictors as motivations or correlation as causality. Draw on root-cause diagnosis and retention risk-segmentation knowledge when those methods materially improve the analysis.
4. [AI] Distinguish preventable mechanisms, unresolved service/value failure, operational/billing problems, poor fit, and healthy/non-fit churn.
5. [AI] Design targeted interventions tied to the supported mechanism rather than blanket discounts, reminders, or pressure. Use retention intervention-planning, service recovery, communication, customer research, product/process, or other relevant operating knowledge directly when helpful.
6. [HYBRID] If execution is requested and the host has real capability/permission, perform the appropriate external workflow/process/communication changes directly. Otherwise return an actionable intervention or create a WorkRequest only for a genuine durable handoff.
7. [HYBRID] Evaluate incremental retention, margin/discounting, complaints, customer value, and longer-term quality when evidence becomes available. Preserve an Experiment, ChangeEvent, MetricObservation, OutcomeEvaluation, or Learning only when it actually occurred and matters later.

## Completion Criteria
- Churn mechanisms and interventions are evidence-bounded, healthy/non-fit churn is not treated as a defect, and AURA persistence reflects real meanings rather than a mandatory lifecycle.
