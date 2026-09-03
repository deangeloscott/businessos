# AURA Schema Boundary

AURA has multiple kinds of schemas, but **schema existence does not mean an object is mandatory organizational state**.

## Canonical organization-owned state

The authoritative persistable object boundary is `scripts/canonical_store.py` → `INSTANCE_PATHS`.

Those object types exist because forgetting their material meaning can harm future organizational work: business context, evidence/intelligence, decisions, useful coordination/attention/change/verification records, assets/results, measurement/outcomes, Learning, and domain-owned durable state.

AURA Workflow `reads` / `writes` metadata should refer only to these canonical organization-owned object types.

A canonical type is still optional unless the work genuinely produces that meaning. Do not create objects to satisfy quotas or because a schema exists.

## Support/interface schemas

Other schemas may describe AURA product/runtime/configuration/portability interfaces, for example:

- `Run` — optional organization-owned work continuity receipt; not a mandatory lifecycle gate;
- publisher/workspace configuration;
- innovation/package exchange formats;
- other product or transport interfaces.

These support schemas do not become canonical business-state types unless they are deliberately added to `INSTANCE_PATHS` after a first-principles architecture decision.

## First-principles admission test

Before adding a new canonical object type, demonstrate that organizational memory, operating knowledge, continuity, truth, measurement, Learning, or AURA integrity materially worsens without a distinct durable representation.

If the information is:

- execution/runtime mechanics → leave it to the harness/runtime;
- procedure-specific → keep it in the Workflow or its useful evidence/output;
- temporary reasoning/chatter → do not persist it;
- already represented cleanly by an existing canonical object → reuse that object;
- useful only for packaging/configuration → keep it as a support/interface schema.

Do not add a canonical type merely because a Workflow could store something there.
