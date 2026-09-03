# Public Distribution

ViralTrac AURA is distributed as portable, source-available organization-owned memory and operating knowledge for capable AI.

## Current maturity

AURA is currently **Alpha**. The version in `VERSION` is the source of truth. Alpha releases may change architecture, interfaces, schemas, Playbooks, and operating guidance before 1.0.

A green product-integrity gate means the release is internally coherent; it does not by itself mean the product is stable or that every Workflow has proven real-world excellence.

## Recommended way to get AURA

For most users, the recommended artifact is the curated full ViralTrac AURA ZIP from an official GitHub prerelease/release.

Advanced users may clone or fork the public repository. The repository may include maintainer/developer tests and qualification tooling that are intentionally excluded from curated end-user packages.

## What ships to users

Curated distributions contain the AURA product source, included operating knowledge, schemas, navigation, validation helpers, and the minimal distribution test needed to verify the package itself.

They do **not** include:

- maintainer-only qualification/evaluator infrastructure;
- benchmark fixtures or hidden evaluator material;
- developer regression suites;
- business instances or customer data;
- local workspace pointers;
- credentials or secrets;
- proprietary ViralTrac application source.

The package builder fails if maintainer qualification infrastructure leaks into a user distribution.

## Full and component editions

The **full ViralTrac AURA ZIP** is the primary release artifact.

Optional component editions are smaller distributions generated from the same canonical source. A component is current AURA Core plus selected domain operating knowledge; it is not a separate product architecture and does not restrict what a capable model/harness may do with its own abilities.

## Organization-owned state

AURA can operate from one local folder or use a separate organization-owned workspace. Keeping organization state separate from product source is useful for upgrades, teams, private Git, and customized deployments.

Use the verified workspace helpers in `OPERATOR-GUIDE.md` / `DEPLOYMENT.md` rather than bundling live business state into a release artifact.

## Updating

AURA does not run its own update service or auto-updater.

Use Git/GitHub, official release assets, or the active harness/user's normal software-management workflow to check for and apply updates. Review changes before replacing a customized copy, and preserve organization-owned workspace state separately when appropriate.

## License

AURA is **source-available, not open source**. Internal business use, customization, and agency/consulting use for clients are permitted under `LICENSE.md`; see the license for restrictions on white-label resale and standalone repackaging.

See `BRANDING.md` for naming and maturity guidance and `SECURITY.md` for the public/private boundary.
