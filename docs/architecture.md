# Architecture

ViralTrac AURA is a **durable, organization-owned memory and operating-knowledge layer for capable AI**. It is not the AI model, agent runtime, provider/tool selector, scheduler, permission system, semantic router, or universal workflow engine.

The simplest useful mental model is:

- **Model / human** — understands the request, reasons, judges evidence, chooses/adapts the method, makes business decisions, and decides what should happen next.
- **AURA** — preserves durable organizational context, facts, evidence, preferences, decisions, useful results, measurements, Learning, and reusable operating knowledge.
- **Harness / runtime** — provides real tools, models/providers, browsing, APIs, subagents, concurrency, retries, scheduling, notifications, credentials, permissions, and execution mechanics.
- **External operational systems** — remain authoritative for the operational data/actions they actually own, such as CRM, analytics, accounting, publishing, or ViralTrac measurement/attribution.

The intended loop is:

**identify organization → retrieve little → work normally → remember what matters → measure/learn when evidence supports it → continue**

## Durable state is semantic, not a mandatory lifecycle

AURA does not require work to pass through one universal object pipeline. Canonical objects exist because their meanings can be useful later, not because every task must create each stage.

Examples include:

- `SourceRecord` — bounded evidence/source material worth preserving.
- `Observation` — a supported direct observation.
- `Insight` — an evidence-calibrated interpretation worth reusing.
- `Opportunity` — an optional durable intervention/improvement worth considering.
- `DecisionRecord` — a real organizational decision worth remembering.
- `Asset` — a useful produced artifact or durable reference to one.
- `WorkRequest` — a real durable handoff across people/models/sessions/time, not internal tool/subagent routing.
- `AttentionItem` — a material unresolved condition worth future awareness; AURA remembers the meaning, not notification delivery.
- `ChangeEvent` — a material real-world/organizational change worth preserving when later work benefits from knowing what changed.
- `OutcomeEvaluation` — evidence-calibrated evaluation of a result/change/experiment.
- `Learning` — reusable guidance whose scope is justified by evidence.

Create or update only the objects whose meaning actually occurred and whose persistence materially improves future work. Do not manufacture Opportunities, WorkRequests, Runs, events, approvals, or lifecycle records merely because a schema exists.

## Operating knowledge

AURA uses **Playbook → Workflow → Step** as a simple operating-knowledge hierarchy.

- A **Playbook** is a meaningful end-to-end business job.
- A **Workflow** is reusable procedure knowledge that helps accomplish part of a Playbook and may also be useful independently.
- A **Step** is the minimum guidance that materially improves repeatability, truth, evidence discipline, scope, or quality.

Playbooks and Workflows are knowledge, not executable controllers. Deterministic indexes may surface bounded candidates, but candidate retrieval is only navigation help. The active model/user owns semantic applicability and may use AURA knowledge, combine it with another Skill, adapt it, choose another sound method, or work ad hoc.

AURA does not maintain a universal provider/capability vocabulary for execution. Workflows describe the business outcome, evidence, constraints, and useful procedure in natural language; the active harness resolves actual tools/providers/Skills at execution time.

## Context retrieval

Root `CONTEXT.md` contains the small universal operating guidance for AI using AURA. `scripts/enter.py` and the context planner retrieve the smallest useful relevant organizational context and optional Playbook/Workflow candidates.

They do not:

- create a mandatory Run;
- inspect/rank providers;
- preflight the host as AURA product logic;
- calculate generic permissions/autonomy;
- choose semantic intent for the model;
- schedule work;
- authorize execution.

The design goal is **relevance over context dumping**.

## Persistence and continuity

AURA is memory consolidation, not execution logging.

Persist something when a capable future model working for this organization would materially benefit after the current session/runtime is gone. Do not persist hidden reasoning, full chats, routine tool calls, retries, subagent chatter, caches, or transient host capability state.

A `Run` is an optional bounded work receipt for useful continuity/provenance. It is not required before reasoning or ordinary persistence.

A `WorkRequest` is appropriate only when a real handoff must survive the current actor/session/runtime. Harness-managed subagents, tool calls, retries, and internal domain-to-domain reasoning do not require WorkRequests.

## Monitoring and time

AURA may preserve semantic monitoring intent: what matters, why, useful signals, dates/checkpoints, cadence intent, and what another review should answer.

The active harness/runtime/OS/workflow tool owns actual recurrence, wakeups, polling, webhooks, retries, and notification delivery. AURA does not run a background scheduler or internal event bus.

## Truth, evidence, and integrity

AURA's deterministic strength is in mechanics it can truly own:

- schema-valid canonical state;
- organization/business isolation;
- resolvable references;
- evidence/provenance integrity;
- exact identifiers/hashes/dates where appropriate;
- current-versus-historical state mechanics;
- portable persistence and workspace integrity.

Semantic interpretation stays with capable intelligence. Known, inferred, hypothetical, unknown, and externally evidenced claims should remain distinguishable. Deterministic code should not pretend to decide source identity, business materiality, causal meaning, applicability, Learning maturity, or the correct next business method when those require judgment.

## Portability

The organization-owned workspace is the durable substrate. Models, harnesses, devices, and tools can change while useful organizational memory survives.

AURA remains local-first and portable-first: no mandatory cloud, database, custom UI, provider, model, scheduler, or proprietary runtime is required. External/shared workspace roots are supported for upgrade-safe operation; one-folder portability remains possible where desired.

Multiple models or people may use the same organizational state, but ordinary filesystem atomicity should not be confused with database-level distributed transaction guarantees.

## Product boundary

During ordinary business work, AURA product source is not modified to solve an execution problem. Organization-specific facts, preferences, Learning, evidence, and results belong in organization state. Product-source changes are deliberate AURA development work.

The architectural test for a new feature is simple:

> Does this improve durable organizational memory, reusable operating knowledge, continuity, truth, or results enough to justify the added concept—and is AURA the natural owner?

If the model, human, harness, OS, ViralTrac, or another specialized system already owns the responsibility better, AURA should provide useful context/evidence and stay out of the way.
