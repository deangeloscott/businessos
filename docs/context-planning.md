# Context Planning

The objective is **minimum sufficient context**, not minimum files at any cost. An explicitly selected Workflow should receive the durable organizational knowledge and AURA guidance that materially improve the work—and avoid unrelated state or host/runtime clutter.

## What the planner loads

For a selected AURA Workflow, the context planner may include:

1. root `CONTEXT.md` and shared operating-knowledge guidance;
2. the owning operating area's `DEFAULTS.md` when relevant;
3. useful nested family `DEFAULTS.md` files on the path to the selected Workflow;
4. the selected Workflow itself;
5. AURA policies that are mechanically relevant to the Workflow's declared durable reads/writes or operating area;
6. exact focus objects named for the work;
7. bounded referenced/provenance objects when they materially support the selected context;
8. unambiguous durable Business Context requested by the Workflow's `context` metadata;
9. canonical objects matching the Workflow's `reads` selectors when resolution is unambiguous;
10. schemas for canonical object types the Workflow may write/update;
11. explicit AURA reference files declared by the Workflow;
12. effective scoped preferences and any useful supplied evidence references.

The plan is retrieval support, not semantic routing or execution authority. The model/user still decides whether the selected Workflow is applicable and how to perform the work.

## Workflow metadata used for context

Current Workflow frontmatter may contribute:

- `context` — especially relevant durable Business Context types;
- `reads` — canonical durable object types/selectors that may help the procedure;
- `writes` — canonical durable object types the work may materially produce;
- `evidence_inputs` — external/high-volume evidence categories that may need bounded retrieval;
- `references` — exact AURA reference files that should accompany the Workflow;
- `completion_evidence` — structural evidence expectations when separately useful to validation/qualification.

These fields describe useful context and durable outputs. They are not permissions, provider requirements, lifecycle stages, or an execution graph.

## Ambiguity

If a selector matches many organization objects and no exact focus/reference resolves which one matters, the planner reports the ambiguity rather than bulk-loading an entire directory or pretending to understand the user's intent.

The capable model/user resolves semantic applicability from the request and evidence. AURA's deterministic planner handles bounded retrieval mechanics only.

## Large evidence

For large transcripts, analytics, search results, CRM histories, monitoring data, or other high-volume material, retrieve/filter only what the current job needs and preserve bounded SourceRecord/Observation references or useful summaries when they deserve durable memory.

Do not dump the complete raw corpus into every reasoning step merely because it is available. Large or sensitive source data may remain in the external system that already owns it.

## Schemas

Existing input objects normally carry enough structure to read them. The planner loads schemas for object types the selected Workflow may write rather than every schema in AURA. Additional schemas remain available on demand when genuinely needed.

## What context planning does not own

The context planner does not inspect or decide:

- host tool inventories;
- provider bindings or model choice;
- capability preflight;
- permissions or autonomy levels;
- scheduler state;
- retries or concurrency;
- semantic intent;
- publication/action authorization;
- the correct business strategy.

Those responsibilities belong to the capable model/user, active harness/runtime, or external system that actually owns them.
