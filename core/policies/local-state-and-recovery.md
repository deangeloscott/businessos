# Local State and Recovery

Use the filesystem workspace as the default portable persistence layer. Preserve valid work across agent restarts, tool loss, product upgrades, workspace relocation, and partial runs instead of silently restarting or discarding state.

## Workspace resolution
- With no configuration, the BusinessOS product root is also the workspace root.
- When `BUSINESSOS_WORKSPACE` or the local untracked `.businessos/workspace.json` pointer selects an external workspace, logical state paths resolve there while product contracts/scripts/schemas remain in the BusinessOS distribution.
- Persist workspace-relative logical refs such as `instances/<business-id>/...` and `runtime/runs/<business-id>/<run-id>/...`; do not unnecessarily bake one machine's absolute path into canonical provenance.
- Use `scripts/workspace_status.py` to inspect the active resolution before moving/recovering state.

## Storage classes
1. **Canonical business state** — persist durable context, intelligence, decisions, operations, assets, measurement, and Learning under `instances/<business-id>/`. Validate canonical objects before writing.
2. **Run state** — keep task-specific plans, intermediate artifacts, checkpoints, and logs under `runtime/runs/<business-id>/<run-id>/`. Run state may be temporary, but it is the recovery handoff while work is active or interrupted.
3. **Human knowledge state** — generated human-readable views live under `knowledge/<business-id>/_generated/`; human working notes live under `knowledge/<business-id>/notes/`. Neither replaces canonical BusinessOS truth.
4. **Workspace attachments** — optional files appropriate to retain with the workspace may live under `attachments/`. Keep credentials out of the workspace.
5. **External/raw state** — large, sensitive, high-volume, or system-owned source data may remain in the authoritative external system. Store SourceRecord/Asset references, lineage, timestamps, hashes, or bounded snapshots when permitted and useful. Do not turn the portable workspace into an unnecessary data lake.

## Current and historical state
- Prefer one canonical current object for one business fact/decision at the appropriate semantic scope. Do not create parallel current copies merely because another workflow, Markdown view, or second-brain tool needs the same truth.
- Use existing lifecycle states such as `superseded`, `archived`, `contradicted`, or domain-specific equivalents when newer evidence replaces prior state. Preserve lineage/history when it matters to auditability or Learning.
- Reuse a valid existing Asset/Observation/Insight/Opportunity/etc. when it still satisfies the job; refresh or supersede it when evidence, scope, or freshness materially changed.
- Never select among several plausible current objects by guessing. Resolve from explicit focus/relationships or surface the ambiguity.

## Start/resume behavior
Before creating a new Run for work that may already be in progress, inspect the active business and relevant existing run state. Resume compatible unfinished work when its task, contract, inputs, and intended outcome still match; otherwise create a new bounded Run and preserve the prior Run for history.

**Destructive cleanup is not recovery.** Never delete an existing business instance, Run, canonical artifact, human-note directory, or workspace merely because its name/status suggests failure, staleness, or testing. Ignore/preserve unrelated prior state unless the user/administrator explicitly authorizes deletion or a deterministic test owns a documented disposable path.

On interruption or failure:
1. Preserve completed outputs that already validate and remain based on valid inputs.
2. Record enough run/checkpoint/log state for another compatible agent to determine what completed, what failed, and what remains.
3. Do not repeat expensive research or execution merely because the agent process restarted.
4. Re-run only failed, missing, stale, or invalidated work. If upstream inputs materially changed, invalidate downstream work that depended on them.
5. If an external mutation may have partially occurred, do not retry blindly; inspect ChangeEvent/Verification state first to avoid duplicate or conflicting actions.

## Workspace relocation / version-control recovery
- An organization may clone/copy its workspace to another machine, then reselect it with `scripts/configure_workspace.py` or `BUSINESSOS_WORKSPACE`; canonical logical refs should remain valid because they are workspace-relative.
- Git history is an optional durability/rollback aid, not BusinessOS truth governance by itself. A historical file version is not automatically the current canonical business fact merely because Git can restore it.
- Product upgrades and workspace updates are separate operations. Do not resolve a product merge conflict by silently deleting or overwriting organization state.

## Capability/source loss
- If a required capability fails or disappears, rerun capability preflight. Use another existing binding, an authorized provider path, or manual/assisted fallback. Do not fabricate the missing result.
- If a source becomes unavailable, keep previously valid canonical intelligence and its provenance, mark uncertainty/freshness appropriately, and do not claim the evidence was revalidated.
- If recovery cannot safely continue, preserve the Run and represent the blocker through the applicable WorkRequest, Incident, approval, or manual action rather than destroying state.
