---
id: core.opportunity.discover-next-best-work
type: playbook
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Business
- Objective
- Insight
- Opportunity
- MetricObservation
- OutcomeEvaluation
- Learning
writes:
- WorkRequest
- Initiative
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - core.work.requested
  - core.object.updated
context:
- Business
- Objective
- EconomicContext
---
# Discover Next Best Work

## Purpose
Translate a broad business goal or prioritization request into the highest-value next work available from current evidence and installed modules.

## Business Outcome
Allocate business attention toward the best evidence-backed opportunities instead of making the user choose a department, tactic, or BusinessOS workflow first.

## Run When
When the user asks what to work on, how to grow/improve the business broadly, or which opportunities deserve attention first.

## Do Not Run When
Do not replace a direct requested task or a broad unexplained symptom that first requires `core.diagnosis.business-problem`.

## Process
1. [AI] Resolve the governing Objective, desired business outcome, constraints, economics, timeframe, and any explicit exclusions from current Business Context before proposing work.
2. [HYBRID] Reuse current eligible Opportunities, Insights, MetricObservations, prior outcomes, and business Learnings first; reject stale, duplicated, already-completed, or no-longer-applicable candidates.
3. [AI] Decide whether the existing Opportunity set is sufficient to make a useful choice. If it is not, identify only the domain/evidence gaps likely to change prioritization rather than launching every installed system.
4. [HYBRID] Create bounded WorkRequests to relevant installed semantic owners to refresh evidence or discover candidate Opportunities. Respect module independence and never create foreign-domain canonical Opportunities on behalf of omitted systems.
5. [HYBRID] Ensure candidate Opportunities are qualified comparably through their domain owner/Core qualification logic, including expected incremental business value, evidence/confidence, cost, risk, urgency, dependencies, reversibility, and strategic leverage where material.
6. [DETERMINISTIC] Apply the shared interpretable priority framework consistently and prevent double counting when Opportunities share the same causal pathway or expected outcome.
7. [AI] Select the smallest high-value set of next work, explain why it outranks credible alternatives, and identify what was deferred because of lower value, uncertainty, dependency, or scope.
8. [HYBRID] If multiple independently owned Opportunities must be coordinated toward one outcome, create an Initiative; otherwise route the selected Opportunity directly to planning/execution according to autonomy and approval policy.

## Verification
- Recommended work is traceable to a current Objective and evidence-backed Opportunity, and prioritization reasons are inspectable rather than hidden in one opaque score.

## Failure / Fallback
- If available evidence is too weak to rank interventions responsibly, return the smallest evidence-gathering work that would unlock a decision instead of inventing a priority list.

## Completion Criteria
- The user receives a defensible next-best-work recommendation or bounded evidence plan without needing to choose an internal system first.
