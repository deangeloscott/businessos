# Deploying ViralTrac AURA

**ViralTrac AURA** stands for **Agentic Understanding and Reinforcement Architecture**. It is an AI-native BusinessOS with one portable operating architecture and three deployment experiences. These are **not different products or required hosting tiers** and do not change the underlying contracts.

## 1. Simple — Download and Use
Best for first-time users or one-device use.

```text
ViralTrac AURA folder
├── product files
├── instances/
├── runtime/
└── knowledge/
```

1. Download or clone ViralTrac AURA.
2. Give the folder to a compatible AI/agent harness.
3. Initialize a business normally.
4. No Git, hosted service, account, Obsidian, or external workspace is required.

The product root is the workspace root by default.

## 2. Power User — Private Versioned Workspace
Best for users who want history, rollback, multi-device use, durable customizations, or a second-brain interface.

```text
AURA product                         Private user workspace
core/                                instances/
systems/                             runtime/
scripts/          reads/writes ---> knowledge/
                                     attachments/
```

Configure a new empty workspace:

```bash
python3 scripts/configure_workspace.py ~/My-AURA-Workspace --profile power_user
python3 scripts/workspace_status.py
```

If the current AURA copy already contains business state, migrate instead of merely switching roots:

```bash
python3 scripts/migrate_workspace.py ~/My-AURA-Workspace --profile power_user
python3 scripts/workspace_status.py
```

Migration is non-destructive. It preflights target conflicts, copies state, verifies every migrated file by SHA-256, keeps the source workspace intact, and activates the target only after verification succeeds. A second migration over identical content is idempotent.

The local product stores only an untracked pointer in `.businessos/workspace.json`. The workspace itself contains a portable `.businessos/workspace.json` profile and can be copied/cloned elsewhere. You may use `BUSINESSOS_WORKSPACE=/path/to/workspace` instead of the pointer; the `BUSINESSOS_*` compatibility namespace is intentionally retained even though the public product name is ViralTrac AURA.

A private Git repository is recommended but optional. GitHub, GitLab, Forgejo, local Git, or organization-controlled infrastructure can all be used; AURA does not depend on one provider.

Open `knowledge/` directly in Obsidian, VS Code, or another Markdown tool if desired.

## 3. Organization — Shared Organization Workspace
Best for teams that need controlled collaboration and organization-owned state.

```text
Canonical ViralTrac AURA product
              │
              ▼
Private organization workspace
├── instances/       canonical AURA/BusinessOS state
├── runtime/         run/recovery state
├── knowledge/       human-readable views + human notes
├── attachments/     optional workspace-owned files
└── .businessos/     portable workspace profile
              │
        optional private Git
              │
 GitHub Org / GitLab / Forgejo / self-hosted Git
```

For a new organization workspace:

```bash
python3 scripts/configure_workspace.py /path/to/acme-aura-workspace --profile organization
python3 scripts/workspace_status.py
```

For an existing populated workspace:

```bash
python3 scripts/migrate_workspace.py /path/to/acme-aura-workspace --profile organization
python3 scripts/workspace_status.py
```

Use repository permissions and collaboration controls appropriate to the organization. AURA does not assume unsynchronized concurrent writes to the same canonical object are conflict-safe.

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

`_generated/` is a replaceable human view derived from canonical BusinessOS JSON. `notes/` is for human-authored working notes and is **not canonical truth** merely because it exists in the workspace.

To deliberately bring a human note into AURA's evidence pipeline:

```bash
python3 scripts/register_human_note.py <business-id> <note-path-under-notes>
```

Registration creates provenance-backed source material and a content hash. It does **not** silently turn the note's statements into Business, Observation, Insight, or Learning truth; those claims must still pass the normal evidence/context/domain process.

This is intentionally compatible with Obsidian-style second-brain use while remaining ordinary Markdown that works without Obsidian.

## Git/versioning guidance
An AURA workspace is a strong candidate for private Git because canonical JSON, Learning, extensions, and Markdown are text-based and auditable. The workspace bootstrap creates conservative ignore rules for secrets and ephemeral logs.

Do not commit:
- credentials, API keys, tokens, or private keys;
- unnecessary raw customer/export datasets;
- files prohibited by the organization's data-handling rules;
- `attachments/private/` unless the organization has explicitly chosen a safe repository policy for those files.

Large, sensitive, high-volume, or externally authoritative data can stay in Salesforce, HubSpot, analytics platforms, Drive, databases, or other systems of record. AURA should retain permitted SourceRecord/Asset references, provenance, bounded snapshots, hashes, or derived intelligence rather than becoming an unnecessary data lake.

## Upgrading AURA separately from organization state
External workspaces let product source and organization state move independently:

```text
AURA current version  --->  AURA future version
          \                       /
           \                     /
             same organization workspace
```

Business-scoped ProcessExtensions, Learning, canonical state, and human knowledge remain organization-owned. Product/schema migrations may still be needed when a future AURA release intentionally changes schemas, but an ordinary product upgrade should not require creating a new organization fork.

## Move an existing workspace safely
Use `migrate_workspace.py` rather than manually copying only `instances/` and forgetting related run/knowledge state.

The migration copies these workspace-owned namespaces when present:
- `instances/`
- `runtime/`
- `knowledge/`
- `attachments/`

The product template `instances/_template/` is never migrated as organization state. Different non-identical files already present at the target stop the migration before copying begins. The old source remains untouched, so rollback is simply re-selecting the old workspace.

If `BUSINESSOS_WORKSPACE` is set in the host, that environment variable intentionally overrides a local pointer. The migration helper will report the environment change needed rather than pretending it can modify the parent shell process.

## Return to zero-configuration/local mode
Point the workspace back at the product root:

```bash
python3 scripts/configure_workspace.py . --profile simple --allow-state-switch
```

Use `--allow-state-switch` only when you intentionally want a different state root. If the goal is to move existing state back into the product folder, run `migrate_workspace.py . --profile simple` instead.

## Invariant
A user must always be able to download/unzip ViralTrac AURA and operate it locally. Git, Obsidian, a hosted AURA service, remote storage, or a proprietary control plane may improve the experience but may never become required merely to use the operating system.

See `BRANDING.md` for the public naming rule. Technical compatibility identifiers such as the repository name `businessos` and `BUSINESSOS_*` environment variables remain stable unless a dedicated compatibility migration changes them.
