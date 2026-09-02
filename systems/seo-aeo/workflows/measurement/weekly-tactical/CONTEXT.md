---
id: seo.measurement.weekly-tactical
type: workflow
owner_system: seo-aeo
reads:
- MetricObservation
- Opportunity
- ChangeEvent
- Experiment
writes:
- MetricObservation
context:
- EconomicContext
- Market
- Objective
- Offer
---
# Organic Discovery Tactical Review

## Purpose
Produce a compact operational view of material organic-discovery changes, current work, risks, and evidence-backed next priorities.

## Business Outcome
Help the organization react to meaningful SEO/AEO changes without turning a recurring report into an AURA work-routing or approval system.

## Run When
Use when the user/team needs a tactical organic-discovery review for a recent period and current measurement/work evidence is available. Weekly is a common rhythm, not an AURA-owned schedule.

## Process
1. [HYBRID] Check whether the relevant measurement inputs are sufficiently complete/reliable for the review and state important limitations.
2. [AI] Summarize only material business/search/AI/local/authority/technical changes; suppress routine noise.
3. [HYBRID] Summarize active Opportunities/work by what changed, what evidence exists, what was completed, what is blocked by a real constraint, and what remains uncertain. Do not create generic approval states for reporting convenience.
4. [HYBRID] Summarize material ChangeEvents, early/confirmed outcomes, Incidents, failed attempts, and measurement checkpoints only where they affect the decision.
5. [AI] Explain the highest-value next actions in business/evidence terms. The active model/user chooses method, sequencing, tools, delegation, and execution; there is no AURA autonomy tier.
6. [AI] Produce a concise executive summary with drill-down references to the underlying durable objects/evidence when useful.
7. [DETERMINISTIC] Persist new reusable MetricObservations only when the review computes durable measurement meaning not already represented elsewhere.

## Verification
- Tactical urgency is not manufactured from normal metric noise.
- Real blockers/constraints are distinguished from invented approval state.
- The report informs work but does not route or authorize it.

## Completion Criteria
- The team can see what materially changed, what work/results matter, and what deserves attention next without a separate AURA control lifecycle.
