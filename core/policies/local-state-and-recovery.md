# Local State and Recovery

Use the filesystem workspace as the default portable persistence layer. Preserve durable organizational meaning across model/harness restarts, tool loss, product upgrades, and workspace relocation without turning AURA into a runtime recovery system.

## Workspace resolution
- With no configuration, the AURA product root is also the workspace root.
- When `BUSINESSOS_WORKSPACE` or the local untracked `.businessos/workspace.json` pointer selects an external workspace, logical state paths resolve there while product contracts/scripts/schemas remain in the AURA distribution.
- Persist workspace-relative logical refs such as `instances/<business-id>/...`; optional Run refs may use `runtime/runs/<business-id>/<run-id>/...`. Do not unnecessarily bake one machine's absolute path into canonical provenance.
- Use `scripts/workspace_status.py` to inspect active workspace resolution before moving organization-owned state.

## Storage classes
1. **Canonical organization state** — durable context, intelligence, decisions, operations, assets, measurement, Learning, and reusable process knowledge live under `instances/<business-id>/`. This is AURA's primary continuity surface. Validate canonical objects before writing.
2. **Optional work receipts** — a Run may record a bounded piece of materially useful continuity: what work was requested, which method was used, what evidence/results belong to it, and whether that receipt remains active or completed. A Run is not required to begin, continue, validate, or complete ordinary work.
3. **Human knowledge state** — generated human-readable views live under `knowledge/<business-id>/_generated/`; human working notes live under `knowledge/<business-id>/notes/`. Neither replaces canonical AURA truth.
4. **Workspace attachments** — optional files appropriate to retain with the workspace may live under `attachments/`. Keep credentials out of the workspace.
5. **External/raw state** — large, sensitive, high-volume, or system-owned source data may remain in the authoritative external system. Store SourceRecord/Asset references, lineage, timestamps, hashes, or bounded snapshots when permitted and useful. Do not turn the portable workspace into an unnecessary data lake.

## Continuity after interruption
The active model/harness should use its own working context while it exists. Across sessions or harnesses, reconstruct only the context that materially matters from current canonical organization state, relevant evidence/assets, human notes when appropriate, and an optional Run receipt if one was intentionally created for that work.

Do not create a Run merely because work might be interrupted. Do not require a future worker to find or resume a Run before using current organizational truth. If an existing receipt is clearly relevant, it can help explain what was attempted, what useful results already exist, and what remains unresolved; otherwise ignore it and work from the durable state that actually matters.

A completed Run means only that the bounded receipt was intentionally closed with the continuity/results it claims to index. It does **not** certify artifact quality, prove that an external change shipped, establish a business outcome, or make its method semantically correct. Those truths come from the actual artifact, evidence, ChangeEvent/VerificationRecord, measurement, OutcomeEvaluation, or authoritative external system as appropriate.

On interruption or failure:
1. Preserve valid durable outputs that were actually produced and remain useful.
2. Use the host's working/checkpoint facilities when available. If a Run already exists and materially improves cross-session continuity, update that receipt with concise useful state rather than preserving every transient tool event or hidden reasoning trace.
3. Do not repeat expensive research or execution merely because the model process restarted; reuse still-valid evidence and outputs.
4. Re-do only work that is actually missing, stale, invalidated, or known to have failed. Let the capable model/user judge semantic dependency from the real task and evidence instead of requiring an AURA execution graph.
5. If an external mutation may have partially occurred, inspect the authoritative external state and any useful ChangeEvent/Verification evidence before retrying so duplicate or conflicting actions are avoided.

Separate Runs are independent receipts. Completing one must not automatically complete, supersede, classify, or otherwise mutate another. If continuity must cross a real person/model/session/team boundary, use the existing durable organizational meaning—such as a relevant result/decision/AttentionItem or a real `WorkRequest` handoff—rather than creating a Run relationship graph.

## Current and historical state
- Prefer one canonical current object for one business fact/decision at the appropriate semantic scope. Do not create parallel current copies merely because another workflow, Markdown view, or tool wants the same truth.
- Update current truth directly when the same object remains meaningful; remove obsolete optional fields when they are no longer true.
- Use object-specific historical states such as `superseded`, `archived`, `contradicted`, or `retired` only where that distinction has real semantic value. Do not force every object through a universal lifecycle.
- Reuse a valid existing Asset/Observation/Insight/Opportunity/etc. when it still satisfies the job; update, retire, supersede, or forget it when evidence and future usefulness justify that choice.
- Never select among several plausible current objects by guessing. Resolve from explicit focus/relationships or let the model/user surface the ambiguity.

## Workspace relocation / version-control recovery
- An organization may clone/copy its workspace to another machine, then reselect it with `scripts/configure_workspace.py` or `BUSINESSOS_WORKSPACE`; canonical logical refs should remain valid because they are workspace-relative.
- Git history is an optional durability/rollback aid, not AURA truth governance. A historical file version is not automatically the current organizational fact merely because Git can restore it.
- Product upgrades and workspace updates are separate operations. Do not resolve a product merge conflict by silently deleting or overwriting organization state.
- Never delete an existing organization, canonical artifact, receipt, note directory, or workspace merely because a name/status suggests failure, staleness, or testing. Delete only when the user/administrator intends deletion or a deterministic test owns a documented disposable path.

## Host capability or source loss
- Tool/provider availability, credentials, retries, installation, and alternative execution paths belong to the active host/harness/user. AURA does not rerun capability preflight, resolve provider bindings, or create approval/manual-action objects when a tool disappears.
- If a needed capability is unavailable, use another valid host method when practical, ask for a real user choice/input when necessary, or preserve the limitation honestly. Persist it in AURA only when the limitation itself is durable organizational knowledge worth future awareness.
- If a source becomes unavailable, keep previously valid canonical intelligence and its provenance, represent freshness/uncertainty truthfully, and do not claim the evidence was revalidated.
- Use a `WorkRequest` only when a real durable handoff to another actor/session/team should survive. Use an `Incident` or `AttentionItem` only when the underlying condition itself has that durable business meaning. Never manufacture one solely because execution stopped.
