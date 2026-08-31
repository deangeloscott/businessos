# ViralTrac AURA — Operator Guide

AURA is the organization-owned layer for durable business context, evidence, operational knowledge, work continuity, outcomes, and Learning. It is not the model, tool runtime, provider resolver, scheduler, or orchestrator.

## Workspace

AURA can keep state with the product folder or use a separate organization-owned workspace:

```bash
python3 scripts/configure_workspace.py /path/to/workspace --profile power_user
python3 scripts/workspace_status.py
```

For a populated workspace move, use `scripts/migrate_workspace.py` rather than copying state blindly.

## Initialize an organization

```bash
python3 scripts/init_business.py <business-id> --name "Business Name"
```

Ground explicit supplied facts/evidence with supported context/evidence helpers. Unknowns remain unknown; do not fabricate plausible business details.

## Prepare work

Normal business work starts from the user's request:

```bash
python3 scripts/enter.py "<complete business request>" --business-id <business-id>
```

The result retrieves bounded organizational context and may recommend an AURA playbook. The recommendation is not authority. The active model/harness may use it, adapt it, use an external Skill, use another established method, or create an ad-hoc method.

AURA playbooks declare provider-neutral capability needs through `core/capabilities/catalog.json`. The active harness/user decides which actual tools/providers satisfy those needs. AURA does not perform capability preflight, provider resolution, host discovery, software installation, credential management, scheduling, or retries.

## Work receipts and persistence

Create a Run when durable continuity is useful:

```bash
python3 scripts/create_run.py <business-id> "<task>" --method-type <external_skill|model_created|ad_hoc> [--method-ref <name>]
```

For an explicitly selected AURA playbook, use its contract ID. General work does not fabricate contract execution.

Persist only material organization-owned meaning through supported canonical helpers. The model supplies substantive meaning; deterministic helpers may supply IDs, timestamps, paths, local references, and integrity checks.

Complete general work with the work-receipt path. AURA-playbook work may additionally use SOP-specific conformance/finalization when claiming that playbook was completed.

## Truth and customer-facing work

AURA should be flexible about method and expression but strict about factual/outward claims. Preserve evidence/provenance and never claim a scan, render, publication, experiment, measurement, deployment, or external action that did not occur.

## Preferences and instructions

Reusable style/work choices may be persisted as preferences. Current-task restrictions such as "do not publish" or "do not contact customers" are task instructions, not standing permission objects and not durable preferences unless the user clearly establishes a reusable instruction.

## Human knowledge layer

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

Generated Markdown is a readable view of canonical organization state. Human notes remain source material until deliberately incorporated with provenance.

## Monitoring

AURA may remember what should be watched, why, cadence intent, material-change signals, prior checks, and when another check would be useful:

```bash
python3 scripts/monitoring_status.py <business-id>
python3 scripts/list_due_monitoring.py <business-id> --due-only
```

These commands do **not** certify that a background task is scheduled. Scheduling/reminders/notifications belong to the active harness/runtime. If the user asks that runtime to schedule something, the runtime should do so using its own facilities; AURA retains only the organizational monitoring intent and meaningful results.

## ViralTrac

ViralTrac is an optional first-party integration, not an AURA runtime dependency. See `integrations/viraltrac/README.md`. The active harness chooses and authenticates the current ViralTrac interface when useful; AURA retains only material organizational meaning and evidence references.

## Validation

Deterministic AURA validation should protect schema/reference integrity, business isolation, truthful provenance, and selected-SOP conformance. It should not require runtime/provider machinery that belongs to the host.
