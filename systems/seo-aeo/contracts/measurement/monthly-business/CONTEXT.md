---
id: seo.measurement.monthly-business
type: playbook
owner_system: seo-aeo
reads:
- MetricObservation
- Opportunity
- ChangeEvent
- Experiment
- Observation
writes:
- MetricObservation
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - revenue.read
  - ai_answer.observe
context:
- EconomicContext
- Market
- Objective
- Offer
---
# Organic Discovery Business Review

## Purpose
Connect a meaningful reporting period of SEO/AEO work to business outcomes, explanations, decisions, and the evidence needed for what comes next.

## Business Outcome
Help business decisions reflect real organic contribution and material changes rather than visibility metrics alone.

## Run When
Use when a business review needs a period-level organic-discovery assessment and sufficiently current measurement evidence is available. The period may be monthly or another cadence chosen by the organization; AURA does not schedule the review.

## Process
1. [HYBRID] Confirm the review period, business Objectives, available data, and material attribution/measurement limitations.
2. [HYBRID] Lead with profit/revenue/qualified leads/conversions or the strongest available business proxies, then use qualified traffic and visibility evidence to explain them.
3. [HYBRID] Break down contribution by market, offer, audience, topic/cluster, asset type, discovery surface, and material intervention only where the evidence supports the comparison.
4. [AI] Explain gains/losses through plausible demand, visibility, CTR, conversion, technical, authority, local, AEO, ecosystem, competitor, and business-context mechanisms without forcing a cause when evidence is insufficient.
5. [AI] Review material Opportunities/changes/experiments by value captured, current evidence, real blockers/constraints, costs, and unresolved questions—not by an AURA autonomy status.
6. [AI] Recommend the smallest set of next priorities with explicit business rationale. Preserve an organizational decision only when the user/model actually makes one and future work benefits from remembering it.
7. [DETERMINISTIC] Persist only new reusable MetricObservations that are not already represented by the underlying measurement state.

## Verification
- Business outcomes lead the review; proxies remain labeled.
- Explanations distinguish evidence from hypotheses.
- The review does not create approval/autonomy bookkeeping or automatically route next work.

## Completion Criteria
- A decision-maker can understand what organic discovery contributed during the period, why material changes may have occurred, and what priorities are justified next.
