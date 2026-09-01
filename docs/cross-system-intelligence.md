# Shared Organizational Intelligence

AURA stores useful organizational evidence and understanding once so capable models can reuse it directly across different kinds of work. It does not need an internal publish/subscribe, relevance-routing, request-refresh, or domain-handoff layer.

## Reuse before rediscovery

When work needs customer, competitor, industry, SEO/AEO, content, marketing, journey, proof, measurement, or other organizational context:

1. retrieve the smallest current evidence/Insights/state that can materially improve the decision;
2. respect the meaning and evidence boundaries of that state;
3. reason about relevance in the current task;
4. deepen or refresh evidence only when the current material is insufficient;
5. use whichever AURA playbook, external Skill, model-created method, or ad-hoc approach best fits the job.

Another domain's Insight is context, not an instruction or routing event. A capable model may use it directly without creating a duplicate Insight, Opportunity, relevance signal, or WorkRequest.

## Cross-domain production

Customer language, competitor evidence, Industry developments, SEO requirements, ProofRecords, Brand/Offer truth, prior Assets, and measured Learning may all inform the same customer-facing work when relevant.

Keep their meanings distinct:

- observed facts/evidence stay traceable to their sources;
- interpretations stay scoped to what the evidence supports;
- company claims/offer terms come from current organizational truth;
- creative/persuasion/production choices remain model/user judgment;
- results are not claimed until measured.

Internal briefs such as SEO requirements, persuasion briefs, or content briefs may be persisted as `Asset` objects when future work benefits. They do not require one AURA system to delegate to another.

## Real handoffs

Use a `WorkRequest` only when a **real organizational handoff** must survive across people, models, sessions, or time and another capable actor would materially benefit from the preserved objective/context/status.

Do not create WorkRequests for:

- ordinary cross-domain reasoning;
- subagents or tool calls;
- provider selection;
- retries/concurrency;
- moving from one AURA playbook to another;
- passing an internal brief to production in the same active work.

`core.continuity.manage-handoff` exists for genuine durable handoffs; it is not an orchestration primitive.

## Multiple workstreams

An `Initiative` can be useful when several genuinely distinct durable pieces of organizational work need shared milestones/dependencies toward a larger outcome. It is optional coordination memory, not a requirement for multi-domain reasoning or harness-managed parallelism.

## Runtime boundary

The active model/user chooses semantic relevance and method. The active harness owns tools, subagents, delegation mechanics, scheduling, notifications, retries, permissions, and execution. AURA supplies reusable organizational memory and operating knowledge so those actors do not have to start over.
