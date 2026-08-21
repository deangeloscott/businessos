# Modular Distribution

ViralTrac's BusinessOS can be distributed as a complete copy, a standalone domain OS, a predefined bundle, or a custom module set. Every domain module requires Core; other domain modules are optional enrichments rather than hidden runtime dependencies.

v1.6 distributions are portable-first and also preserve `PUBLISHER.json` and can carry provider defaults from `distribution/provider-defaults.json`. Provider metadata is kept separate from domain SOPs so a branded distribution can prefer first-party/partner software without making the business logic vendor-specific.

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

The packager resolves required dependencies, includes only interface schemas needed to consume canonical objects from omitted modules, prunes unused capabilities and irrelevant provider metadata, removes real business instances, preserves publisher provenance, creates edition-specific navigation and instance defaults, validates the resulting workspace, and emits a ZIP plus SHA-256 checksum.

## Provider defaults

`distribution/provider-defaults.json` travels with an edition. It may seed preferred providers for capabilities retained by that edition. A recipient can override those defaults at environment or business scope, and an enabled existing permitted binding wins by default.

## Portable-first rule

Every generated edition remains a self-contained filesystem workspace with `instances/` for durable business state, `runtime/runs/` for bounded run/recovery state, and a built-in `deployment/environments/local/` no-integration environment for capability preflight. Optional infrastructure may enhance an edition but is not a required Business OS dependency.

## Independence rule

Standalone modules preserve canonical interfaces. When an optional upstream module is absent, the active module uses supplied Business Context/evidence, existing Core objects, or bounded task-specific research. It may not create canonical domain conclusions on behalf of an uninstalled semantic owner. If the requested task itself belongs to an uninstalled module, routing reports that the module is not installed instead of silently impersonating it.

Each recipient may keep a separate copy. Their `instances/<business-id>/` directory holds brand-specific context, intelligence, proof, assets, preferences, outcomes, and Learning. Updating or repackaging the reusable OS does not require those business instances to be shared with other customers.
