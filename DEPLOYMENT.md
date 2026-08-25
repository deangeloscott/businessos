# Deploying ViralTrac's BusinessOS

BusinessOS uses one portable operating system with three obvious deployment experiences. These are **not different editions** and do not change the underlying contracts.

## 1. Simple — Download and Use
Best for first-time users or one-device use.

```text
BusinessOS folder
├── product files
├── instances/
├── runtime/
└── knowledge/
```

1. Download/clone BusinessOS.
2. Give the folder to a compatible AI/agent harness.
3. Initialize a business normally.
4. No Git, hosted service, account, Obsidian, or external workspace is required.

The product root is the workspace root by default.

## 2. Power User — Private Versioned Workspace
Best for users who want history, rollback, multi-device use, durable customizations, or a second-brain interface.

```text
BusinessOS product                    Private user workspace
core/                                 instances/
systems/                              runtime/
scripts/          reads/writes --->  knowledge/
                                      attachments/
```

Configure it:

```bash
python3 scripts/configure_workspace.py ~/My-BusinessOS-Workspace --profile power_user
python3 scripts/workspace_status.py
```

The local product stores only an untracked pointer in `.businessos/workspace.json`. The workspace itself contains a portable `.businessos/workspace.json` profile and can be copied/cloned elsewhere. You may use `BUSINESSOS_WORKSPACE=/path/to/workspace` instead of the pointer.

A private Git repository is recommended but optional. GitHub, GitLab, Forgejo, local Git, or organization-controlled infrastructure can all be used; BusinessOS does not depend on one provider.

Open `knowledge/` directly in Obsidian, VS Code, or another Markdown tool if desired.

## 3. Organization — Shared Organization Workspace
Best for teams that need controlled collaboration and organization-owned state.

```text
Canonical BusinessOS product
            │
            ▼
Private organization workspace
├── instances/       canonical BusinessOS state
├── runtime/         run/recovery state
├── knowledge/       human-readable views + human notes
├── attachments/     optional workspace-owned files
└── .businessos/     portable workspace profile
            │
      optional private Git
            │
 GitHub Org / GitLab / Forgejo / self-hosted Git
```

Configure it:

```bash
python3 scripts/configure_workspace.py /path/to/acme-businessos-workspace --profile organization
python3 scripts/workspace_status.py
```

Use the repository permissions and collaboration controls appropriate to the organization. BusinessOS does not assume unsynchronized concurrent writes to the same canonical object are conflict-safe.

## Human knowledge / second-brain view
For any profile with knowledge enabled:

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

This creates:

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

`_generated/` is a replaceable view of canonical BusinessOS JSON. `notes/` is for human-authored working notes and is **not canonical truth** until explicitly incorporated through normal BusinessOS evidence/context governance.

This is intentionally compatible with Obsidian-style second-brain use while remaining ordinary Markdown that works without Obsidian.

## Git/versioning guidance
A BusinessOS workspace is a good candidate for private Git because canonical JSON, Learning, extensions, and Markdown are text-based and auditable. The workspace bootstrap creates conservative ignore rules for secrets/ephemeral logs in an external workspace.

Do not commit:
- credentials, API keys, tokens, private keys;
- unnecessary raw customer/export datasets;
- files prohibited by the organization's data-handling rules.

Large, sensitive, high-volume, or externally authoritative data can stay in Salesforce, HubSpot, analytics platforms, Drive, databases, or other systems of record. BusinessOS should retain permitted SourceRecord/Asset references, provenance, bounded snapshots, hashes, or derived intelligence rather than becoming an unnecessary data lake.

## Upgrading BusinessOS separately from organization state
External workspaces let the product and organization state move independently:

```text
BusinessOS v1.8.x  --->  BusinessOS future version
          \                 /
           \               /
            same organization workspace
```

Business-scoped ProcessExtensions, Learning, canonical state, and human knowledge remain organization-owned. Product/schema migrations may still be needed when BusinessOS intentionally changes schemas, but an ordinary product upgrade should not require creating a new organization fork.

## Return to zero-configuration/local mode
Point the workspace back at the product root:

```bash
python3 scripts/configure_workspace.py . --profile simple
```

Or remove the local `.businessos/workspace.json` pointer and unset `BUSINESSOS_WORKSPACE`.

## Invariant
A user must always be able to download/unzip BusinessOS and operate it locally. Git, Obsidian, a hosted BusinessOS service, remote storage, or a proprietary control plane may improve the experience but may never become required merely to use the operating system.
