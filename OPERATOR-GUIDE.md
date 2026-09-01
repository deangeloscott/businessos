# ViralTrac AURA — Operator Guide

This is the practical reference for people who want more control over how AURA is set up and used. If you are new to AURA, start with `BEGINNERS-GUIDE.md`.

AURA keeps useful business memory, evidence, operating knowledge, work history, outcomes, and Learning. The AI and its tools still do the reasoning and execution.

You do not need to memorize the commands below. A capable command-line or coding agent can often run them for you.

## Choose where business memory lives

AURA can keep business memory inside the AURA product folder, or in a separate organization-owned workspace.

A separate workspace is usually better for regular use because it makes upgrades, backups, several computers, and team use safer.

Create an empty separate workspace:

```bash
python3 scripts/configure_workspace.py /path/to/workspace --profile power_user
python3 scripts/workspace_status.py
```

If the current AURA folder already contains business information, move it with `scripts/migrate_workspace.py` instead of copying only some folders or simply switching the workspace path.

## Set up a business

```bash
python3 scripts/init_business.py <business-id> --name "Business Name"
```

Save supplied facts and evidence through AURA's supported context/evidence helpers. If something is unknown, leave it unknown instead of inventing a likely answer.

## Prepare work

Normal business work starts with the user's request:

```bash
python3 scripts/enter.py "<complete business request>" --business-id <business-id>
```

AURA retrieves a small amount of relevant business memory and may recommend a playbook.

The recommendation is guidance, not authority. The AI/user may use it, adapt it, use an outside Skill, use another established method, or create a better method for the task.

AURA playbooks describe the kinds of capabilities they need in general terms. The active AI/harness decides which real tools or providers to use. AURA does not need to inspect the computer, rank providers, install software, manage credentials, schedule jobs, or control retries.

## Work receipts and saving useful results

A Run is an optional work receipt. Create one when remembering a bounded piece of work will help later:

```bash
python3 scripts/create_run.py <business-id> "<task>" --method-type <external_skill|model_created|ad_hoc> [--method-ref <name>]
```

If the work deliberately uses an AURA playbook, use that playbook's contract ID.

Do not pretend ordinary or outside work used an AURA playbook when it did not.

Save only material organization-owned meaning through AURA's supported save helpers. The AI supplies the business meaning. Deterministic helpers can safely supply things such as IDs, timestamps, paths, local references, and format checks.

A work receipt should help a future AI understand what materially happened. It should not become a full chat transcript or hidden-reasoning archive.

## Truth and customer-facing work

AURA can be flexible about how work is done, but it should stay strict about factual claims.

Keep the evidence behind important claims. Never say a scan, render, publication, experiment, measurement, deployment, or outside action happened when it did not.

## Preferences and instructions

Reusable choices such as writing style or preferred output format can be saved as preferences when they are meant to apply again.

A one-time instruction such as “do not publish this” or “do not contact customers” applies to the current work. Do not silently turn it into a permanent rule unless the user clearly means it to be reusable.

## Human-readable knowledge view

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

This creates Markdown pages that are easier for people to read.

These pages are views of AURA's main structured business records. Human notes can also live in the knowledge area, but a note does not automatically become a trusted business fact. Bring important notes into AURA's evidence process deliberately when useful.

## Monitoring

AURA can remember what should be watched, why it matters, how often another check may be useful, what changes matter, and what was found before:

```bash
python3 scripts/monitoring_status.py <business-id>
python3 scripts/list_due_monitoring.py <business-id> --due-only
```

These commands do **not** mean a background task is actually scheduled.

The active AI/harness, operating system, workflow tool, ViralTrac, or another runtime handles the real scheduling and notification delivery. AURA keeps the business meaning of the monitoring request and the useful results.

## ViralTrac

ViralTrac is optional. AURA does not require it.

When ViralTrac is useful, the active AI/harness connects to it through the available interface and credentials. AURA keeps only the useful business meaning and evidence references that should survive later.

See `integrations/viraltrac/README.md` for integration details.

## Validation

AURA validation should protect what AURA owns: valid stored records, valid references, correct business separation, truthful evidence links, and the important requirements of an AURA playbook when that playbook was actually used.

Validation should not require provider selection, scheduling, browser control, or other runtime machinery that belongs to the AI/harness.
