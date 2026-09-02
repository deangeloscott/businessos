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

## Minimum sufficient guidance

When authoring or improving a Workflow, specify a Step only when it materially improves repeatability, truth, evidence discipline, quality, scope, or a non-obvious piece of expertise.

Do not hardcode incidental implementation details merely because they can be specified. If a capable model can reliably choose a better implementation while preserving the real requirement, let it.

See `docs/workflow-authoring.md` and `docs/operating-knowledge.md`.

## Saving useful results

For ordinary durable organizational meaning, use:

```bash
python3 scripts/remember.py <business-id> --input <json-file>
```

The model/user supplies the semantic meaning. AURA supplies IDs, timestamps, schema/reference checks, paths, organization isolation, atomic writes, and rollback where appropriate.

Before saving, ask:

> Would a capable future model working for this organization materially benefit from knowing or reusing this after the current session is gone?

Do not persist something merely because a schema exists.

When a real deliverable matters later, keep the actual artifact where it naturally belongs and remember the useful `Asset` identity/reference/provenance/status rather than automatically copying every binary or scratch file into AURA.

## Correcting and forgetting state

When established truth changes, update the current object. When an obsolete top-level field should disappear, remove it explicitly rather than relying on omission.

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

If an organization intentionally defines a reusable local procedure or wants to augment an installed Workflow, preserve it as a `ProcessExtension` rather than changing AURA product source.

If evidence-supported Learning suggests a reusable Workflow should change, `WorkflowEvolutionProposal` can capture that evidence-backed candidate before intentional adoption.

Organization-authored procedure knowledge does not need fake Learning first.

## Truth and customer-facing work

AURA can be flexible about how work is done while staying strict about factual claims.

Keep the evidence behind important claims. Never say a scan, render, publication, experiment, measurement, deployment, or outside action happened when it did not.

Artifact QA and production readiness are separate from receipt completion. Use the relevant operating knowledge and deterministic claim/media/readiness checks when they materially protect the actual output.

## Preferences and instructions

Reusable choices such as writing style or preferred output format can be saved as preferences when they are meant to apply again.

A one-time instruction such as “do not publish this” or “do not contact customers” applies to the current work. Do not silently turn it into a permanent rule unless the user clearly means it to be reusable.

## Human-readable knowledge view

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

This creates Markdown pages that are easier for people to read.

These pages are views of AURA's main structured organization records. Human notes can also live in the knowledge area, but a note does not automatically become a trusted business fact. Bring important notes into AURA's evidence process deliberately when useful.

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
