# ViralTrac AURA — Storage, Multi-Device, and Team Setup

This guide explains where AURA keeps business memory and how to use the same memory across upgrades, computers, or a team.

If you are new to AURA, start with `BEGINNERS-GUIDE.md` first.

AURA has one product architecture. The setups below are not different products or paid hosting levels. They are simply different places to keep the organization's files.

## A useful idea: software and business memory are different things

AURA has product files such as playbooks, instructions, schemas, and helper scripts.

AURA also has organization-owned files such as business context, useful work history, knowledge, and attachments.

Those can live together for the simplest setup, or separately for safer upgrades and sharing.

## 1. Simple setup — one AURA folder

Best for trying AURA, one-device use, or people who want the fewest moving parts.

```text
ViralTrac AURA folder
├── product files
├── instances/       business memory
├── runtime/         optional work receipts/continuity
├── knowledge/       human-readable knowledge
└── attachments/     optional files
```

1. Download or clone AURA.
2. Give an AI tool access to the folder.
3. Set up a business.
4. Use AURA normally.

No Git, hosted service, account, notes app, or separate workspace is required.

In this setup, the AURA folder itself is also the workspace.

This is the easiest way to try AURA. For regular use, a separate workspace is usually safer because replacing the AURA product folder does not also replace your business memory.

## 2. Regular or power-user setup — separate workspace

Best for people who want safer upgrades, history, rollback, several computers, durable customizations, or a human-readable notes view.

```text
AURA product folder                 Your workspace
core/                               instances/
systems/                            runtime/
scripts/          reads/writes ---> knowledge/
                                    attachments/
```

Create a new empty workspace:

```bash
python3 scripts/configure_workspace.py ~/My-AURA-Workspace --profile power_user
python3 scripts/workspace_status.py
```

If the current AURA folder already contains business information, **move it instead of simply changing the workspace path**:

```bash
python3 scripts/migrate_workspace.py ~/My-AURA-Workspace --profile power_user
python3 scripts/workspace_status.py
```

The migration helper is designed to avoid silent data loss. Before changing the active workspace it:

- checks for conflicting files at the destination;
- copies the organization-owned files;
- verifies every copied file with SHA-256 hashes;
- leaves the old workspace untouched;
- activates the new workspace only after verification succeeds.

Running the same migration again over identical files is safe.

### How AURA remembers the workspace location

The AURA product can keep a small local pointer in:

`.businessos/workspace.json`

The workspace also keeps its own portable profile file.

Advanced users may instead set:

```text
BUSINESSOS_WORKSPACE=/path/to/workspace
```

`BUSINESSOS_*` is an older technical compatibility name that remains supported even though the public product name is ViralTrac AURA.

## 3. Team setup — shared organization workspace

Best for teams that need organization-owned memory and controlled collaboration.

```text
AURA product
     │
     ▼
Organization workspace
├── instances/       main structured business records
├── runtime/         optional work receipts/continuity
├── knowledge/       readable views and human notes
├── attachments/     optional workspace files
└── .businessos/     workspace profile
     │
     └── optional private Git or other shared storage
```

Create a new team workspace:

```bash
python3 scripts/configure_workspace.py /path/to/acme-aura-workspace --profile organization
python3 scripts/workspace_status.py
```

Move an existing populated workspace:

```bash
python3 scripts/migrate_workspace.py /path/to/acme-aura-workspace --profile organization
python3 scripts/workspace_status.py
```

Use file, repository, or server permissions that fit the organization.

### Important: simultaneous editing

AURA does not currently promise database-style conflict handling when two agents change the same saved record at exactly the same time.

Several agents can read the same workspace. Different agents can also often create different records safely. When two agents may edit the same file or record, coordinate that work instead of assuming conflicts will be merged automatically.

## Use the same AURA memory on several computers

You have several options.

### Keep the workspace on one main computer or server

Other devices can connect to that machine using normal remote-access tools.

This gives you one clear live copy of the workspace.

### Use private Git

Git keeps a history of file changes and can help move a text-based workspace between computers.

AURA does not require Git or a particular Git hosting company. You can use GitHub, GitLab, Forgejo, local Git, or organization-controlled infrastructure.

Before using Git for a workspace, understand what information the repository will contain and who can access it.

### Use a trusted file-sync or cloud-storage tool

A normal synced folder can also move workspace files between computers.

This is convenient, but two computers editing the same file at the same time can create sync conflicts. AURA does not depend on a particular storage provider and does not hide these conflicts behind its own sync service.

## Human-readable knowledge and notes

If the workspace has the knowledge layer enabled, run:

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

This creates a structure such as:

```text
knowledge/<business-id>/
├── README.md
├── _generated/
│   ├── Home.md
│   ├── Business.md
│   ├── Priorities.md
│   ├── Learning.md
│   ├── Experiments.md
│   └── ...
└── notes/
    └── README.md
```

`_generated/` contains replaceable human-readable pages made from AURA's main structured business records.

`notes/` is for human working notes. A note does **not** become a trusted AURA business fact merely because it is stored there.

To deliberately register a human note as source material:

```bash
python3 scripts/register_human_note.py <business-id> <note-path-under-notes>
```

AURA records where the note came from and a hash of its contents. It still does not silently turn every statement in the note into an established fact or Learning.

The Markdown files work in ordinary text editors, VS Code, Obsidian, or other Markdown notes apps. No specific notes app is required.

## Private Git guidance

An AURA workspace can work well in private Git because much of its important state is text-based and easy to review over time.

Do **not** commit:

- passwords, API keys, tokens, or private keys;
- unnecessary raw customer or export datasets;
- files your organization's data rules do not allow in the repository;
- `attachments/private/` unless the organization has deliberately chosen a safe policy for those files.

Large, sensitive, or frequently changing source data often belongs in the system that already owns it, such as a CRM, analytics platform, database, Drive, or another business system.

AURA can keep useful references, bounded snapshots, hashes, evidence, or derived Learning instead of becoming an unnecessary copy of every outside data source.

## Upgrade AURA without starting over

A separate workspace lets the AURA software change while the organization's memory stays in place:

```text
old AURA version ─┐
                  ├── same organization workspace
new AURA version ─┘
```

When you upgrade:

1. keep the organization workspace;
2. get the new AURA product version;
3. point the new version to the same workspace;
4. read the release notes for any special migration step;
5. verify the workspace before deleting an older product copy.

Most upgrades should not require a new organization workspace.

A future release may sometimes need to change the format of stored records. When that happens, the release should provide an intentional migration path rather than asking the user to start over.

AURA does not run its own software updater. Git, GitHub, release downloads, the user, or the active AI/harness can handle software updates.

## Move an existing workspace safely

Use `scripts/migrate_workspace.py` instead of manually copying only one folder and forgetting related state.

When present, migration moves these organization-owned areas together:

- `instances/`
- `runtime/` (optional bounded work receipts/continuity, when present)
- `knowledge/`
- `attachments/`

The product template under `instances/_template/` is not treated as organization data.

If the destination already contains a different file with the same path, migration stops before copying begins. The old source remains untouched, so you can return to it if needed.

If the host has `BUSINESSOS_WORKSPACE` set, that setting takes priority over the local pointer. The migration helper will tell you what environment setting needs to change; it cannot secretly change the parent terminal or host process for you.

## Return to the one-folder setup

Point AURA back to the product folder:

```bash
python3 scripts/configure_workspace.py . --profile simple --allow-state-switch
```

Use `--allow-state-switch` only when you intentionally want AURA to use a different state location.

If you need to **move existing organization data back into the product folder**, use migration instead:

```bash
python3 scripts/migrate_workspace.py . --profile simple
```

## What must stay true

AURA must remain usable as a local, portable system.

Git, a notes app, hosted storage, remote infrastructure, ViralTrac, or a proprietary control plane may improve some setups, but none should become a requirement merely to use AURA.

Technical compatibility names such as the repository name `businessos` and `BUSINESSOS_*` environment variables remain supported unless a future release provides a deliberate compatibility migration.
