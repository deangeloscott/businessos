# Public Distribution

ViralTrac's BusinessOS is designed to be portable and distributable as a self-contained workspace. The public repository is the canonical source for official source-available releases; versioned ZIP assets are the recommended distribution format for most users.

## Public but not open source

The source is visible so users, agencies, clients, and AI systems can inspect and operate the BusinessOS. Use is governed by `LICENSE.md`. The license permits internal business use, customization, and agency/consulting use for clients, but does not permit white-label resale or repackaging the BusinessOS as someone else's standalone product.

## ViralTrac separation

The public BusinessOS does not include ViralTrac's proprietary application source code or private infrastructure. ViralTrac integrations use intentionally machine-facing, authenticated interfaces. See `SECURITY.md`.

## Releases

Use tagged GitHub Releases for stable versions. A normal user can download a ZIP, unzip it, and give the workspace to a compatible AI/agent environment. Advanced users may clone or fork the public repository subject to the source-available license and GitHub's platform terms.

The **full BusinessOS ZIP is the primary and recommended release asset**. Specialized editions are optional smaller downloads generated from the same canonical source for users who intentionally want a bounded subsystem. The source repository itself represents the full BusinessOS; editions should not be maintained as separate source branches or competing codebases.

## Updates

Update checks are optional and disabled by default. When enabled, BusinessOS can request the official GitHub Releases metadata and compare the latest stable version with the local `VERSION`. It never auto-downloads or auto-installs an update because BusinessOS copies may contain business-specific state or user modifications.

Use:

```bash
python scripts/check_for_updates.py --force
```

to perform a one-time check without enabling recurring checks, or:

```bash
python scripts/set_update_policy.py --enable
```

to allow a compatible host/agent to perform bounded stable-release checks according to `deployment/update-policy.json`.

The update request does not upload business instances, prompts, credentials, local files, or operating history. GitHub will still receive ordinary connection metadata associated with an HTTPS request.
