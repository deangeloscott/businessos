# ViralTrac integration

ViralTrac is an optional first-party integration for ViralTrac AURA. It is **not** AURA's runtime, provider resolver, scheduler, event engine, permission system, or required execution path.

## Boundary

AURA owns durable organizational meaning: relevant facts and evidence, decisions, work/results, measurements and outcomes, and evidence-supported Learning.

The active model/harness/user owns method choice and reasoning. The active runtime owns authentication, tools, provider selection, capability discovery, retries, scheduling, webhooks/events, concurrency, and execution mechanics.

When ViralTrac is available and useful, the active intelligence may use its current interfaces for business data, attribution, tracking, measurements, experiments, artifacts, or supported actions. When another source or tool is better, use that instead. AURA must never force ViralTrac merely because it is first-party.

## Combined operating model

When AURA and ViralTrac are both available, they should compose rather than compete:

1. AURA supplies relevant organization-owned context, prior evidence, decisions, Learning, and reusable business operating knowledge.
2. The active model uses that context and its own judgment to decide what work is useful and which methods or tools fit the job.
3. ViralTrac supplies current first-party business evidence and specialist capabilities where relevant, such as attribution, tracking, measurement, experiments, funnel or content evidence, and supported growth actions.
4. AURA Playbooks and Workflows provide business operating expertise. ViralTrac agent/operator playbooks provide product-specific guidance for using ViralTrac surfaces. They may be combined when useful; neither is a routing authority or replacement for model judgment.
5. Execute through ViralTrac only when its current interface says the action is available and authorized. Otherwise use another appropriate host tool or treat ViralTrac guidance as evidence/advice rather than pretending an external action occurred.
6. After the work, preserve in AURA only the durable organizational meaning that will materially help future work, with references back to authoritative ViralTrac evidence, artifacts, measurements, experiments, or receipts when useful.

Do not create fixed one-to-one mappings between AURA Workflows and ViralTrac tools or playbooks. The active intelligence should combine them semantically according to the user's actual outcome and the capabilities currently available.

## Persist meaning, not a second data plane

Do not bulk-copy ViralTrac operational history into AURA. Preserve only the durable organizational information a capable future model would materially benefit from, with references back to authoritative ViralTrac evidence or receipts when available.

Examples include:
- evidence-backed business observations;
- metric observations and outcome evaluations;
- artifacts/results worth retaining;
- material external changes;
- durable decisions prompted by the evidence;
- unresolved attention;
- Learning supported by measured outcomes.

Absence or unavailability from ViralTrac is not evidence that a business fact is false or zero.

## Tooling

AURA does not maintain ViralTrac capability bindings. The active harness discovers and invokes whatever ViralTrac interface is actually available (for example MCP, API, connector, or future interface). Credentials remain outside AURA durable state.

When ViralTrac exposes an AI-native bootstrap, capability, tool-group, or equivalent discovery surface, prefer that current interface over hard-coding assumptions about available tools. If MCP is available and task scope is unclear, let ViralTrac's own current discovery metadata guide which product-specific surfaces to load while keeping the model responsible for the overall business method.

`semantic-mapping.json` contains optional correspondence hints between ViralTrac concepts and AURA records. Those mappings are not execution contracts or routing authority.
