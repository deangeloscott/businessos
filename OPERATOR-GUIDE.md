# ViralTrac AURA — Operator Guide

This is the practical reference for people who want more control over how AURA is set up and used. If you are new to AURA, start with `BEGINNERS-GUIDE.md`.

AURA keeps useful business memory, evidence, operating knowledge, work continuity, outcomes, and Learning. The AI and its tools still do the reasoning and execution.

You do not need to memorize these commands. A capable command-line or coding agent can often run them for you.

## Choose where organization memory lives

AURA can keep organization memory inside the AURA product folder or in a separate organization-owned workspace.

A separate workspace is usually better for regular use because it makes upgrades, backups, several computers, and team use safer.

Create an empty separate workspace:

```bash
python3 scripts/configure_workspace.py /path/to/workspace --profile power_user
python3 scripts/workspace_status.py
```

If the current AURA folder already contains organization information, move it with `scripts/migrate_workspace.py` instead of copying only some folders or simply switching the workspace path.

## Attach AURA to the harness

If work usually starts outside the AURA folder, make AURA persistently discoverable once.

Preferred for Skill-capable harnesses: install/copy the included:

```text
skills/viraltrac-aura/
```

using the harness's normal personal/global Skill mechanism.

For a harness without Skills, use the small persistent instruction in `AURA-ATTACHMENT.md`.

Awareness and file access are separate. The Skill/instruction can tell the model AURA exists; the harness still needs permission or a connector/mount that lets it actually read and write the AURA product/workspace files.

## Set up an organization

```bash
python3 scripts/init_business.py <business-id> --name "Business Name"
```

Save supplied facts and evidence through AURA's supported context/evidence helpers. If something is unknown, leave it unknown instead of inventing a likely answer.

## Prepare work

Normal organization work starts with the user's natural-language request:

```bash
python3 scripts/enter.py "<complete business request>" --business-id <business-id>
```

AURA retrieves a small amount of relevant organization memory and may surface high-level Playbook candidates plus detailed Workflow candidates.

The model/user decides what actually applies. AURA does not semantically route the request.

The response includes bounded lexical `saved_work_candidates` with readable titles/purposes, versions, status, artifact pointers and matched terms. Use an ordinary-language `business_role` when saving an Asset; no extra title is required. Lookup reuses AURA's token normalization and document-frequency weighting across descriptions and filenames, not linked document contents or semantic synonyms. Broaden with `--saved-work-limit 20` (maximum 100), page with `--saved-work-offset 20`, or change search terms. Candidates are navigation suggestions, not verified conclusions; recency does not establish authority.

Repeat `--focus <object-id>` for known records, including archived/superseded history. Unknown IDs appear in `unresolved_focus`. Unreadable canonical files appear in `read_diagnostics` with a total count; either condition returns `needs_judgment` while readable context remains available. Missing matches, unreadable files and unresolved explicit references are different outcomes—not proof that the organization has no knowledge. Continue useful qualified work without relying on incomplete retrieval as evidence of absence.

### Operating knowledge hierarchy

**Playbook → Workflow → Step**

- **Playbook** — a meaningful end-to-end business job.
- **Workflow** — a reusable procedure that helps accomplish part of a Playbook and may also be useful independently.
- **Step** — the minimum useful procedural guidance inside a Workflow.

Browse candidate Playbooks:

```bash
python3 scripts/find_playbooks.py "<request>"
```

Browse candidate Workflows:

```bash
python3 scripts/find_workflows.py "<request>"
```

Load an explicitly chosen Workflow with bounded context:

```bash
python3 scripts/enter.py "<request>" --business-id <business-id> --selected-workflow <workflow-id>
```

A model may use an AURA Playbook/Workflow, adapt it, combine it with another installed Skill, use another Skill instead, create another sound method, or work ad hoc.

AURA does **not** maintain a universal capability catalog or tool allowlist. Workflows describe what should be accomplished in natural language. The active AI/harness decides which real tools, providers, Skills, APIs, subagents, renderers, and orchestration methods best serve the outcome.

For optional selection and connection help, see [tools, models, and services](docs/tools-and-services.md). It includes current-information guidance and outcome-based combinations, not a runtime registry. Reuse existing access, honor organization preferences, and confirm connections through the actual work when possible. Unlisted providers need no AURA registration; save durable local choices through existing organization memory so product upgrades preserve them.

## Minimum sufficient guidance

When authoring or improving a Workflow, specify a Step only when it materially improves repeatability, truth, evidence discipline, quality, scope, or a non-obvious piece of expertise.

Do not hardcode incidental implementation details merely because they can be specified. If a capable model can reliably choose a better implementation while preserving the real requirement, let it.

See `docs/workflow-authoring.md` and `docs/operating-knowledge.md`.

## Saving useful results

For ordinary durable organizational meaning, use:

```bash
python3 scripts/remember.py <business-id> --input <json-file>
```

The model/user supplies the semantic meaning. AURA supplies IDs, schema-supported timestamps, schema/reference checks, paths, organization isolation, atomic writes, and rollback where appropriate. Observation times remain distinct from creation/update times; schemas such as PlatformProfile are not given unsupported timestamp fields.

Before saving, ask:

> Would a capable future model working for this organization materially benefit from knowing or reusing this after the current session is gone?

Do not persist something merely because a schema exists.

When a real deliverable matters later, keep the actual artifact where it naturally belongs and remember the useful `Asset` identity/reference/provenance/status rather than automatically copying every binary or scratch file into AURA.

For example, after creating `deliverables/onboarding-guide.md`, save this payload as a JSON file and pass it to `remember.py`. Replace the example's meaning and path with the actual result:

```json
{
  "provenance": {"method": "ad_hoc"},
  "objects": [{
    "object_type": "Asset",
    "content": {
      "asset_type": "onboarding_guide",
      "business_role": "Customer onboarding guide; clearer instructions based on document inspection",
      "location_reference": "deliverables/onboarding-guide.md",
      "version": "1",
      "status": "draft_not_deployed",
      "extensions": {"evidence_limits": "Customer impact is not measured; proposed changes need field use."}
    }
  }]
}
```

Update that record using its returned ID, without creating another record for the same artifact:

```json
{"objects":[{"object_ref":"<returned-asset-id>","content":{"status":"reviewed_not_deployed"}}]}
```

Only use that status after actual review. Schemas in `core/schemas/` define each type's semantic fields; AURA supplies mechanical fields. The save receipt already includes aggregate integrity validation. Repeat it only after another material change or a specific concern; it does not assess factual accuracy, creative quality, deployment or business effect. Keep assumptions and revision conditions in the artifact and relevant existing semantic fields/extensions, not as invented observations.

## Correcting and forgetting state

When established truth changes, update the current object. When an obsolete top-level field should disappear, remove it explicitly rather than relying on omission.

When an update changes semantic fields on an object with inbound references, `remember.py` saves an existing-type `ChangeEvent` in the same rollback boundary. It retains the changed before/after fields and marks referring records as possible review impacts—not confirmed dependencies. No AttentionItem is created. An optional per-object `correction_summary` explains a material correction and preserves a ChangeEvent even when no inbound reference exists. No-op/timestamp-only saves do not create correction events.

`enter.py` exposes unresolved impacts under `correction_review`, independently of lexical matches. Open the ChangeEvent and relevant authored material. After actual review, update its `change_details` through `remember.py`, preserving each row and setting `review_status` to `reviewed` or `not_affected` with a `review_note`. A record update or generated-view refresh does not silently resolve semantic review. Relationships hidden only in prose may not be found.

When revising an authored deliverable, preserve useful prior versions, update the current Asset's purpose, location, version and status together, and record the review outcome. Do not automatically supersede unrelated artifacts.

When an entire unreferenced object should no longer exist:

```bash
python3 scripts/forget.py <business-id> <object-ref>
```

Unknown/not-found is not absence.

## Optional work receipts

A Run is an optional bounded work receipt. Create one only when continuity or provenance for a piece of work will materially help later.

If a high-level AURA Playbook materially framed the work:

```bash
python3 scripts/create_run.py <business-id> "<task>" --playbook-id <playbook-id>
```

If a detailed AURA Workflow materially framed the work:

```bash
python3 scripts/create_run.py <business-id> "<task>" --workflow-id <workflow-id>
```

For another method:

```bash
python3 scripts/create_run.py <business-id> "<task>" --method-type <external_skill|model_created|ad_hoc> [--method-ref <name>]
```

A method reference records truthful provenance. It does **not** create an execution graph, conformance regime, permission gate, or capability preflight.

When the receipt itself is worth closing:

```bash
python3 scripts/complete_run.py <business-id> <run-id> --summary "<material result>" [--evidence <ref>] [--result <ref>] [--decision <ref>] [--unresolved <item>]
```

Completing a Run means only that the useful receipt was closed and its material continuity was preserved. It does not certify Playbook/Workflow conformance, QA, publication readiness, deployment, external authorization, or business outcomes.

## Organization-specific reusable Workflows

If an organization intentionally defines a reusable local procedure or wants to augment an installed Workflow, preserve it as a `ProcessExtension` when future work materially benefits rather than changing AURA product source.

Evidence-supported Learning may also become a narrow ProcessExtension directly when procedural reuse is genuinely useful. The model/user decides whether the Learning alone is sufficient, whether an extension is worth keeping, and whether that extension applies to future work. There is no required proposal/adoption lifecycle.

Organization-authored procedure knowledge does not need fake Learning first. Organization-specific operating knowledge is retrieval context, not semantic or execution authority.

## Truth and customer-facing work

AURA can be flexible about how work is done while staying strict about factual claims.

Keep the evidence behind important claims. Never say a scan, render, publication, experiment, measurement, deployment, or outside action happened when it did not.

Artifact QA and production readiness are separate from receipt completion. Use the relevant operating knowledge, evidence/provenance checks, optional review aids, and readiness validation when they materially protect the actual output. Natural-language claim support remains a model/user judgment grounded in current organization truth rather than a deterministic language rules engine.

## Preferences and instructions

Reusable choices such as writing style or preferred output format can be saved as preferences when they are meant to apply again.

A one-time instruction such as “do not publish this” or “do not contact customers” applies to the current work. Do not silently turn it into a permanent rule unless the user clearly means it to be reusable.

## Human-readable knowledge view

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

This creates Markdown pages that are easier for people to read.

These pages are views of AURA's main structured organization records. Human notes can also live in the knowledge area, but a note does not automatically become a trusted business fact. Bring important notes into AURA's evidence process deliberately when useful.

Refresh builds and verifies a replacement before swapping directories. A failed build or recoverable rename failure leaves the previous usable view intact; human notes and canonical records are not replaced. On Windows there is a brief directory-rename gap, not a live-reader locking guarantee.

Human-note registration preserves the exact UTF-8 text as a hashed capture, so later note edits do not change an earlier source. Re-registering unchanged notes also completes missing capture metadata from the older native writer, preserving the existing source ID. Onboarding and imported contribution sources preserve their actual captured text or file bytes too. This proves what was supplied/captured, not that its statements are independently true.

When upgrading an existing workspace, retain a backup and validate a copy with the new product first. If older evidence is rejected, inspect its retained capture or acquisition receipt before correcting metadata through supported helpers. Do not bulk-relabel unknown acquisition as verified. If a referenced file has changed since its recorded hash, preserve the original SourceRecord and capture a new revision rather than replacing the old hash to hide the mismatch. Apply related record updates together with `remember.py` where validation requires a consistent batch. Update unreadable or outdated saved-artifact descriptions when their purpose/version is known, review reported impacts, and regenerate the knowledge layer. Older product versions may not understand the new optional evidence fields; use the upgraded product with the upgraded workspace.

Normal save and entry responses include `knowledge_view`: freshness checks canonical content plus the renderer, shared presentation helper and schema registry—not object counts alone. `python3 scripts/generate_knowledge_layer.py <business-id> --freshness` checks without writing. Older views without these fingerprints are not certified current; regenerate once. Missing/damaged pages or unreadable canonical records also prevent a current result. “Current” means the generated representation matches its inputs—not that authored deliverables have been reviewed or that their claims are true.

Native type sections derive from the schema registry's system ownership; optional domain values still organize generic domain-tagged records. Generated pages use the same saved-work titles as retrieval and expose artifact version/location and recorded correction-review status.

## Monitoring

AURA can remember what should be watched, why it matters, how often another check may be useful, what changes matter, and what was found before:

```bash
python3 scripts/monitoring_status.py <business-id>
python3 scripts/list_due_monitoring.py <business-id> --due-only
```

These commands do **not** mean a background task is actually scheduled.

The active AI/harness, operating system, automation service, ViralTrac, or another runtime handles real scheduling and notification delivery. AURA keeps the business meaning of the monitoring request and useful findings.

## ViralTrac

ViralTrac is optional. AURA does not require it.

When ViralTrac is useful, the active AI/harness connects through the available interface and credentials. AURA keeps only the durable business meaning and evidence references future work should retain.

See `integrations/viraltrac/README.md` for integration details.

## Validation

AURA validation should protect what AURA owns: valid stored records, valid references, organization isolation, truthful evidence/provenance mechanics, structurally usable artifacts where deterministic checking helps, Playbook/Workflow integrity, and non-contradictory durable state.

Validation should not decide semantic strategy, tool/provider choice, evidence meaning, scheduling, browser control, or whether the model is allowed to continue working.
