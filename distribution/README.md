# Modular Distribution

**ViralTrac AURA** can be distributed as a complete copy, a standalone AURA domain edition, a predefined bundle, or a custom module set. Every domain module requires Core; other domain modules are optional bodies of operating knowledge rather than hidden runtime dependencies.

AURA distributions are portable-first and preserve publisher/branding metadata plus only the provider-neutral capability vocabulary actually referenced by the included playbooks. They do not ship provider bindings, provider-selection defaults, environment capability inventories, or a runtime resolver. The active model/harness/user chooses real tools and providers.

## Commands

List predefined editions:

```bash
python scripts/package_edition.py --list
```

Build one:

```bash
python scripts/package_edition.py --edition content
python scripts/package_edition.py --edition marketing
python scripts/package_edition.py --edition research
```

Build an arbitrary subset:

```bash
python scripts/package_edition.py --modules content-synthesis industry-intelligence
```

The packager resolves actual product-module dependencies, includes interface schemas needed to consume canonical objects referenced by included playbooks, prunes unused provider-neutral capability vocabulary, removes real organization/workspace state, preserves publisher provenance and AURA branding, creates edition-specific navigation and instance defaults, validates the resulting workspace, and emits a ZIP plus SHA-256 checksum.

## Capabilities and tools

Playbooks may declare provider-neutral capability needs because that helps a model/human understand what kind of work a method expects. Those declarations are descriptive knowledge only. A packaged edition does not choose or configure the software that satisfies them, and missing host tooling does not activate an AURA fallback subsystem.

## Portable-first rule

Every generated edition remains usable as a self-contained filesystem BusinessOS. By default, logical `instances/` and optional `runtime/runs/` state can live with the product folder. Recipients may instead configure a separate organization-owned workspace with `scripts/configure_workspace.py`; populated state moves through `scripts/migrate_workspace.py`. The human knowledge layer remains optional and ordinary Markdown. Git, Obsidian, hosted infrastructure, provider registries, custom schedulers, and the ViralTrac product are not required merely to use AURA.

## Independence rule

Standalone modules preserve canonical interfaces. When an optional adjacent knowledge module is absent, the active model may use available organization context, Core objects, supplied evidence, external Skills, or task-specific research as appropriate. It must not fabricate conclusions that require unavailable evidence merely to imitate an omitted module.

If the user asks for work for which a useful AURA playbook is not installed, say so when that fact matters and continue with another valid method when the capable model/harness can do the work. Do not route the request to an imagined internal service or treat module presence as execution permission.

Each recipient may keep a separate copy and/or separate workspace. Organization-owned context, intelligence, proof, assets, preferences, outcomes, Learning, extensions, and human knowledge do not need to be shared with other customers merely because the reusable AURA product is updated or repackaged.
