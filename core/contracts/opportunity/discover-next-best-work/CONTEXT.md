---
id: core.opportunity.discover-next-best-work
type: playbook
version: 1.3.0
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
Translate a broad business goal or prioritization request into the highest-value next work supported by the **minimum sufficient evidence**.

## Business Outcome
Allocate business attention toward the best evidence-backed opportunities without making the user choose a department/tactic first or paying for unnecessary analysis.

## Run When
When the user asks what to work on, how to grow/improve the business broadly, or which opportunities deserve attention first.

## Do Not Run When
Do not replace a direct requested task or a broad unexplained symptom that first requires `core.diagnosis.business-problem`.

## Process
1. [AI] Resolve the governing Objective, desired business outcome, known constraints/economics/timeframe, and explicit exclusions from current Business Context. Preserve unknown business state as unknown rather than filling it with benchmarks or assumptions.
2. [DETERMINISTIC + AI] Apply **diagnose before intervene**. For a broad profitable-growth/"what should we do next" request, run `python3 scripts/growth_baseline_gate.py <business-id>` before launching domain research or delegation. If it returns `baseline_required`, treat that as a hard first-pass gate: the default next-best work is the **smallest first-party profitable-growth/constraint baseline** needed to distinguish acquisition, conversion, retention/repeat behavior, economics/service mix, capacity, or another material constraint. Translate those universal constraint classes into questions natural to the active business/domain, but include a domain-specific question only when its answer could materially change diagnosis or prioritization. Do not substitute generic competitor/industry/SEO/content/customer-segmentation research simply because it is publicly available, and do not invent how many minutes/hours the user will need to supply the baseline. Only bypass this gate when current first-party evidence already distinguishes the material constraint or the user supplied a more specific problem/task.
3. [HYBRID] Reuse current eligible Opportunities, Insights, MetricObservations, prior outcomes, and business Learnings first; reject stale, duplicated, already-completed, or no-longer-applicable candidates.
4. [AI] Decide whether existing evidence is sufficient for a useful ranking. If not, identify only the unresolved questions whose answers could materially change the ranking. Do **not** launch every installed system, domain, tool, or subagent merely because it is available.
5. [HYBRID] Gather evidence progressively under `core/policies/resource-aware-execution.md`: use the cheapest reliable source and shallowest adequate depth first. Default to one bounded discovery loop before any fan-out. Create a WorkRequest/delegation only for a necessary semantic owner or specialized capability and only when that extra orchestration is expected to materially improve the decision or total execution efficiency; reassess after each meaningful evidence increment. If subagent/provider work fails or times out, salvage any usable evidence and reassess before retrying/redelegating.
6. [AI] Maintain the evidence boundary in `core/policies/evidence.md`. External market/competitor/benchmark evidence may support hypotheses, but do not convert it into active-business facts or company-specific impact/ROI estimates without the required business-specific inputs.
7. [HYBRID] Qualify candidate Opportunities comparably through their domain owner/Core qualification logic. Prioritize expected business value, evidence/confidence, strategic leverage, urgency where real, dependencies, risk, reversibility, and known material constraints. Treat implementation cost/time/staffing as unknown unless supported; do not down-rank work merely using presumed conventional manual-development effort when automation may perform it.
8. [DETERMINISTIC] Apply the shared interpretable priority framework consistently and prevent double counting when Opportunities share the same causal pathway or expected outcome.
9. [AI] Apply a stop test before additional research/delegation: **would the next evidence action plausibly change the top recommendation, materially change its risk/confidence, or satisfy required verification?** If not, stop gathering and decide.
10. [AI] Select **one primary next action** unless multiple actions are genuinely inseparable. Explain why it outranks credible alternatives, state material unknowns/assumptions, and identify what was deferred because of lower value, uncertainty, dependency, or unnecessary scope. Do not present a menu merely to hand prioritization back to the user.
11. [AI] Respect the request boundary: if the user asked only to determine/prioritize what should happen next, complete with the selected next action or bounded evidence plan. Do **not** implement that recommendation, create business-facing assets, or adopt new business commitments unless the user also requested/authorized execution.
12. [HYBRID] If multiple independently owned Opportunities must be coordinated toward one outcome, create an Initiative; otherwise route the selected Opportunity to planning/execution only when that downstream execution is within the requested scope and authorized under autonomy/approval policy.

## Verification
- Recommended work is traceable to a current Objective and evidence-backed Opportunity.
- Business-specific claims are supported by business-specific evidence; external benchmarks remain labeled external.
- Research/delegation performed was decision-relevant rather than broad-by-default.
- Broad profitable-growth work with no first-party performance/economic evidence respected the deterministic baseline gate before domain research.
- Prioritization reasons are inspectable rather than hidden in one opaque score.

## Failure / Fallback
- If available evidence is too weak to rank interventions responsibly, return the smallest evidence-gathering work that would unlock a decision instead of inventing a priority list.
- If the decisive missing evidence is user/first-party business state that cannot be discovered safely, make obtaining/querying that minimal baseline the next-best work. Ask only for the smallest information/access that can change the decision; do not fill the gap with unrelated external research.
- If a clarification or approval request times out, preserve the unresolved input/approval. Timeout is not permission to execute a fallback tactic.

## Completion Criteria
- The user receives one defensible primary next-best-work recommendation or bounded evidence plan without needing to choose an internal system first.
- Unknown/not-found business state has not been misrepresented as absent.
- No recommended intervention was implemented unless implementation was inside the user's request and authorized.
- Additional research/delegation has stopped once it is unlikely to change the decision materially.
