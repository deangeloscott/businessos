# Release Report — v1.8.2

## Theme
Public Distribution Hardening.

This release prepares ViralTrac's BusinessOS for a public, source-available GitHub repository without turning it into open-source software or exposing ViralTrac's proprietary hosted-application implementation.

## Public boundary

- BusinessOS workflows, schemas, policies, templates, helper scripts, provider-neutral capability contracts, and intentionally external ViralTrac client-interface metadata remain distributable.
- ViralTrac application source, internal engineering directives/roadmaps, database/infrastructure implementation, credentials, secrets, customer data, and private operational state are excluded.
- Public-distribution validation checks this boundary before release packaging.

## License

`LICENSE.md` permits internal/commercial business use, modification, and agency/consulting use for client operations. It prohibits white-label resale, separate licensing/subscription fees for BusinessOS itself, and representing a derivative as an official ViralTrac/Umegro release.

## Updates

GitHub Releases is the canonical stable update channel. Update checking is disabled by default, opt-in, metadata-only, and notification-only; updates are never automatically downloaded or installed.
