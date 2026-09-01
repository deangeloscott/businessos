---
id: core.opportunity.discover-next-best-work
type: playbook
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
context:
- Business
- Objective
- EconomicContext
---
# Discover Next Best Work

## Purpose
Translate a broad business goal or prioritization request into the highest-value next work supported by the **minimum sufficient evidence**.

## Business Outcome
Allocate attention toward the most defensible next move without making the user choose a department, tactic, or AURA playbook first and without paying for unnecessary analysis.

## Run When
Use when the user asks what to work on, how to grow/improve the business broadly, or which opportunities deserve attention first.

## Do Not Run When
Do not replace a direct requested task. When the dominant problem is an unexplained symptom whose cause must be understood first, broad diagnosis may be more useful operating knowledge.

## Process
1. [AI] Resolve the governing Objective, desired business outcome, known constraints/economics/timeframe, and explicit exclusions from current organization context. Preserve unknown business state as unknown rather than filling it with benchmarks or assumptions.
2. [HYBRID] Reuse the strongest relevant first-party and canonical state already available. `scripts/growth_baseline_gate.py <business-id>` may be used as a lightweight inventory of recorded economic/performance/outcome objects, but its output is representation context—not a gate and not a judgment that evidence is sufficient. Inspect the actual evidence available rather than equating missing object types with missing business knowledge.
3. [AI] Consider existing Opportunities, Insights, measurements, prior outcomes, experiments, Assets/results, first-party observations/sources, and Learning that materially bear on the decision. Ignore stale, duplicated, completed, superseded, or irrelevant candidates when the evidence supports doing so.
4. [AI] Decide whether the current evidence is sufficient **for this decision and level of commitment**. If a bounded reversible next move is already well supported, do not request an ideal dataset merely to increase certainty. If one unresolved fact could materially change the choice, gather only that decisive gap.
5. [HYBRID] Use the active harness's actual tools, connected systems, Skills, subagents, or direct reasoning normally, following `core/policies/resource-aware-execution.md`. AURA does not create WorkRequests to represent internal model delegation or run capability preflights. Persist a `WorkRequest` only for a real durable handoff that future organizational work should remember.
6. [AI] Keep active-business facts distinct from external evidence and inference. Competitor/market/benchmark patterns may support hypotheses, but they do not establish company-specific economics, impact, timing, or ROI.
7. [AI] Compare credible candidate moves using the factors actually material to the decision—for example business value, evidence strength, strategic leverage, urgency, dependency, downside, reversibility, and known constraints. Do not invent implementation cost, staffing, elapsed time, or ROI where unknown, and do not let a rigid score replace judgment.
8. [AI] Check for overlap so the same expected outcome/evidence is not double counted across nominally different Opportunities.
9. [AI] Before gathering more evidence, ask whether the next evidence action could plausibly change the top recommendation, materially change confidence/downside, or satisfy a real verification requirement. If not, stop gathering.
10. [AI] Select one coherent primary next move unless several actions are genuinely inseparable. Explain why it outranks credible alternatives, material assumptions/unknowns, and what was intentionally deferred. Do not hand prioritization back to the user as an undifferentiated menu unless the decision genuinely requires a user/business choice.
11. [AI] Respect the request boundary. If the user asked only what to do, give the recommendation or bounded evidence plan. If execution was requested, continue through the useful work the host can actually perform until a genuine information, capability, external, legal, or business-decision boundary is reached.
12. [AI] Create an `Initiative` only when several independently meaningful Opportunities need durable shared coordination beyond the current session. Create a `WorkRequest` only for a real durable handoff. Neither is required merely because this playbook considered several possibilities.

## Verification
- The recommendation traces to a current Objective and the strongest relevant organizational evidence available.
- Business-specific claims are supported by business-specific evidence; external evidence remains labeled external.
- Missing canonical baseline object types were treated as representation facts rather than proof that usable evidence is absent.
- Evidence sufficiency was judged relative to the actual decision/commitment level.
- Research and execution depth were decision-relevant rather than broad-by-default.
- Prioritization remains interpretable rather than hidden in one deterministic score.
- Any Initiative/WorkRequest persisted has real durable organizational meaning.

## Failure / Fallback
- If available evidence is too weak to rank interventions responsibly, identify or perform the smallest evidence-gathering work that would unlock the decision instead of inventing a priority list.
- If decisive evidence is user/first-party state that cannot be discovered safely, ask only for the smallest information/access that could change the decision.
- If useful bounded work can proceed under uncertainty, preserve the uncertainty and continue at an appropriate level of commitment rather than treating imperfect information as a global blocker.
- If an external approval/decision is genuinely required and unavailable, preserve that unresolved real-world dependency when future work benefits from it; do not treat timeout/silence as permission or create an AURA approval object.

## Completion Criteria
- The user receives one defensible primary next move, coherent work program, or bounded evidence plan without needing to choose an internal AURA system first.
- When execution was requested, useful work continues until a genuine boundary is reached rather than stopping at planning by default.
- Unknown/not-found business state is not misrepresented as absent.
- No business-specific claim or action is justified by external evidence as though it were first-party proof.
- Additional research/delegation stops once it is unlikely to materially change the decision.
