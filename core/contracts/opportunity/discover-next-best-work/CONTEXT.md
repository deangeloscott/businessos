---
id: core.opportunity.discover-next-best-work
type: playbook
version: 1.4.0
owner_system: core
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
2. [DETERMINISTIC + AI] Apply **diagnose before intervene** without turning data representation into a permission gate. For a broad profitable-growth/"what should we do next" request, run `python3 scripts/growth_baseline_gate.py <business-id>` as a lightweight inventory of recorded economic/performance/outcome state. Treat its output as organizational context, not a deterministic judgment that evidence is sufficient or insufficient. The absence of `EconomicContext`, `MetricObservation`, or `OutcomeEvaluation` objects does not prove that usable first-party evidence is absent: inspect the actual available SourceRecords, Observations, Insights, experiments, assets, business-supplied files, and other first-party state already in context. If that evidence materially distinguishes the likely constraint or supports a bounded reversible next move, continue. If one unresolved first-party fact could materially change the choice, gather only the smallest decisive gap. Do not substitute generic competitor/industry/SEO/content/customer-segmentation research merely because it is publicly available, and do not invent how many minutes/hours the user will need to supply missing information.
3. [HYBRID] Reuse current eligible Opportunities, Insights, MetricObservations, prior outcomes, experiments, relevant first-party observations/sources, and business Learnings first; reject stale, duplicated, already-completed, or no-longer-applicable candidates.
4. [AI] Decide whether existing evidence is sufficient for a useful ranking **for this decision and level of commitment**. Imperfect information is normal. If evidence supports a useful bounded action, do not request a broad ideal dataset merely to increase certainty. If evidence is not sufficient, identify only the unresolved questions whose answers could materially change the ranking. Do **not** launch every installed system, domain, tool, or subagent merely because it is available.
5. [HYBRID] Gather evidence progressively under `core/policies/resource-aware-execution.md`: use the cheapest reliable source and shallowest adequate depth first. Default to one bounded discovery loop before any fan-out. Create a WorkRequest/delegation only for a necessary semantic owner or specialized capability and only when that extra orchestration is expected to materially improve the decision or total execution efficiency; reassess after each meaningful evidence increment. If subagent/provider work fails or times out, salvage any usable evidence and reassess before retrying/redelegating.
6. [AI] Maintain the evidence boundary in `core/policies/evidence.md`. External market/competitor/benchmark evidence may support hypotheses, but do not convert it into active-business facts or company-specific impact/ROI estimates without the required business-specific inputs.
7. [HYBRID] Qualify candidate Opportunities comparably through their domain owner/Core qualification logic. Prioritize expected business value, evidence/confidence, strategic leverage, urgency where real, dependencies, risk, reversibility, and known material constraints. Treat implementation cost/time/staffing as unknown unless supported; do not down-rank work merely using presumed conventional manual-development effort when automation may perform it.
8. [DETERMINISTIC] Apply the shared interpretable priority framework consistently and prevent double counting when Opportunities share the same causal pathway or expected outcome.
9. [AI] Apply a stop test before additional research/delegation: **would the next evidence action plausibly change the top recommendation, materially change its risk/confidence, or satisfy required verification?** If not, stop gathering and decide.
10. [AI] Select **one coherent primary next move** unless multiple actions are genuinely inseparable. A coherent move may contain parallel, sequential, or conditional work when that is naturally required by the objective; do not force a giant formal workflow merely to represent it. Explain why it outranks credible alternatives, state material unknowns/assumptions, and identify what was deferred because of lower value, uncertainty, dependency, or unnecessary scope. Do not present a menu merely to hand prioritization back to the user.
11. [AI] Respect the request boundary. If the user asked only to determine/prioritize what should happen next, complete with the selected next move or bounded evidence plan. If the user also requested execution, continue through the useful authorized work that is possible now rather than stopping at a plan solely because some ideal evidence remains missing. Stop or narrow only at a genuine information, capability, authorization, external, or business-judgment boundary.
12. [HYBRID] If multiple independently owned Opportunities genuinely need durable coordination toward one outcome, create an Initiative. Create a WorkRequest only when handing off or preserving material work actually benefits from one. Do not manufacture coordination objects merely because they are available write types.

## Verification
- Recommended work is traceable to a current Objective and the strongest relevant organizational evidence available.
- Business-specific claims are supported by business-specific evidence; external benchmarks remain labeled external.
- Missing canonical baseline object types were treated as a representation fact, not automatic proof that no usable evidence exists.
- Evidence sufficiency was judged relative to the actual decision/action, and additional information was requested only where it could materially change what should happen next.
- Research/delegation performed was decision-relevant rather than broad-by-default.
- Prioritization reasons are inspectable rather than hidden in one opaque score.

## Failure / Fallback
- If the capable model/human judges available evidence too weak to rank interventions responsibly, return or execute the smallest evidence-gathering work that would unlock the decision instead of inventing a priority list.
- If the decisive missing evidence is user/first-party business state that cannot be discovered safely, make obtaining/querying that minimal gap the next-best work. Ask only for the smallest information/access that can change the decision; do not fill the gap with unrelated external research.
- If useful bounded work can proceed while uncertainty remains, preserve that uncertainty and continue at an appropriate level of commitment instead of treating imperfect information as a global blocker.
- If a clarification or approval request times out, preserve the unresolved input/approval. Timeout is not permission to execute a fallback tactic.

## Completion Criteria
- The user receives one defensible primary next-best-work recommendation, coherent work program, or bounded evidence plan without needing to choose an internal system first.
- When execution was requested, useful authorized work was carried forward until a genuine boundary was reached rather than stopping at planning by default.
- Unknown/not-found business state has not been misrepresented as absent.
- No business-specific claim or action was justified by external evidence as though it were first-party proof.
- Additional research/delegation has stopped once it is unlikely to change the decision materially.
