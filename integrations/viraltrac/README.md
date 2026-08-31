# ViralTrac integration

ViralTrac is an optional first-party integration for ViralTrac AURA. It is **not** AURA's runtime, provider resolver, scheduler, event engine, permission system, or required execution path.

## Boundary

AURA owns durable organizational meaning: relevant facts and evidence, decisions, work/results, measurements and outcomes, and evidence-supported Learning.

The active model/harness/user owns method choice and reasoning. The active runtime owns authentication, tools, provider selection, capability discovery, retries, scheduling, webhooks/events, concurrency, and execution mechanics.

When ViralTrac is available and useful, the active intelligence may use its current interfaces for business data, attribution, tracking, measurements, experiments, artifacts, or supported actions. When another source or tool is better, use that instead. AURA must never force ViralTrac merely because it is first-party.

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

`semantic-mapping.json` contains optional correspondence hints between ViralTrac concepts and AURA records. Those mappings are not execution contracts or routing authority.
