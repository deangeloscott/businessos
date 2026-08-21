# Context Planning

The objective is **minimum sufficient context**, not minimum files at any cost. A contract should receive everything required to reason correctly and nothing unrelated.

## Resolution order
1. Root `CONTEXT.md`.
2. Core defaults.
3. Specialized-system defaults.
4. Any family `DEFAULTS.md` files between the system root and atomic contract.
5. The atomic contract.
6. Policies required by evidence type, action risk, or external mutation.
7. Exact focus objects from the active business.
8. Related upstream/downstream objects referenced by the focus object, but only when they match the contract's read selectors.
9. Unambiguous required Business Context modules.
10. Schemas for objects the contract may write/update.
11. Explicit references declared by the contract.

## Object resolution
Frontmatter separates:
- `context`: canonical Business Context modules;
- `reads`: canonical object types/selectors;
- `evidence_inputs`: external/high-volume evidence the runtime may need to retrieve or summarize;
- `writes`: canonical object types produced;
- `updates`: explicit fields on a canonical object when useful.

If a selector matches many objects and no focus/relationship disambiguates them, the planner reports it as unresolved rather than bulk-loading the directory. The operator/runtime must narrow the query.

## Large evidence
For large transcripts, analytics, search, CRM, or monitoring data: retrieve/filter deterministically, create a bounded working summary, and preserve SourceRecord/Observation references. Do not put the complete raw corpus into every reasoning step.

## Schemas
Existing input objects normally carry enough structure to read them. The planner automatically loads write schemas, not every input schema. Input schemas remain available on demand.
