# Modular Distribution

**ViralTrac AURA** can be distributed as a complete copy, a standalone AURA domain edition, a predefined bundle, or a custom module set. Every domain module requires Core; other domain modules are optional enrichments rather than hidden runtime dependencies.

AURA distributions are portable-first and preserve `PUBLISHER.json`, `BRANDING.md`, and provider defaults from `distribution/provider-defaults.json`. Provider metadata is kept separate from domain SOPs so a branded distribution can prefer first-party/partner software without making the business logic vendor-specific.

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

The packager resolves required dependencies, includes only interface schemas needed to consume canonical objects from omitted modules, prunes unused capabilities and irrelevant provider metadata, removes real business/workspace state, preserves publisher provenance and AURA branding, creates edition-specific navigation and instance defaults, validates the resulting workspace, and emits a ZIP plus SHA-256 checksum.

## Provider defaults

`distribution/provider-defaults.json` travels with an edition. It may seed preferred providers for capabilities retained by that edition. A recipient can override those defaults at environment or business scope, and an enabled existing permitted binding wins by default.

## Portable-first rule

Every generated edition remains usable as a self-contained filesystem BusinessOS. By default, logical `instances/` and `runtime/runs/` state can live with the product folder. Recipients may instead configure a separate organization-owned workspace with `scripts/configure_workspace.py`; populated state moves through `scripts/migrate_workspace.py`. The human knowledge layer remains optional and ordinary Markdown. Git, Obsidian, hosted infrastructure, and the ViralTrac product are not required merely to operate AURA.

## Independence rule

Standalone modules preserve canonical interfaces. When an optional upstream module is absent, the active module uses supplied Business Context/evidence, existing Core objects, or bounded task-specific research. It may not create canonical domain conclusions on behalf of an uninstalled semantic owner. If the requested task itself belongs to an uninstalled module, routing reports that the module is not installed instead of silently impersonating it.

Each recipient may keep a separate copy and/or separate workspace. Organization-owned context, intelligence, proof, assets, preferences, outcomes, Learning, extensions, and human knowledge do not need to be shared with other customers merely because the reusable AURA product is updated or repackaged.
