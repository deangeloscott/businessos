# Publisher Provenance and Updates

`PUBLISHER.json` gives every distribution a machine-readable origin and optional canonical update location.

It can record:

- publisher ID/name;
- canonical project URL;
- documentation/support URLs;
- an update-manifest URL;
- provenance rules for derivative distributions.

Generated `SYSTEM-MANIFEST.json` includes configured publisher identity and points back to `PUBLISHER.json`. Edition packaging preserves this metadata by default.

This provides durable attribution in ordinary redistribution and gives an agent a canonical place to look for documentation or updates. It is not DRM: a deliberate redistributor can remove or alter provenance metadata. Existing workspace/release SHA-256 checksums help detect changes to a particular packaged release but do not prevent copying.

Publisher metadata records origin; it does not authorize installation. Native bundled downloads offer an optional updater through **Settings → Startup & updates**. The default is **Notify me**. **Update now** explicitly authorizes that release; **Update automatically when idle** is a separate user choice. **Manual only** disables scheduled release checks. Agents and CLI users can continue their own Git/download upgrade process.

The visual interface checks the public GitHub releases at launch and at most daily while open. No separate background updater service is installed. Published numeric Alpha releases are included; drafts and development/RC/nightly tags are excluded. The existing bell shows one shared notice for the available version. **Later** defers it for a day; **Skip this version** suppresses that version, not future ones.

The updater selects the native OS/architecture bundle, verifies size and the SHA-256 digest reported by GitHub over HTTPS, bounds archive extraction, checks bundled file integrity, and probes the bundled Python before activation. These checks rely on the publisher's GitHub account and HTTPS; they are not independent code signing or macOS notarization. Missing digests or platform bundles offer the release page instead of running unverified bytes.

Application updates are staged in machine-local `ViralTrac/Aura/updates/versions`, outside the selected workspace. Activation waits for AURA requests, organization work and editing to be idle. It reopens the same local address and workspace, checks actual startup, and changes the original launcher's saved target only after success. Startup registration follows the new app when AURA owns that entry. The old app is retained; failed startup reopens it, and **Use previous version** offers rollback. A failed release is not retried automatically in a loop. Files are not deleted from original downloads.

Workspaces, AI credentials, native chats/schedulers and custom interface folders are not replaced. A source checkout or edited bundled files get manual-update guidance. A workspace inside the app folder must first be moved through the existing workspace flow. Changes to the canonical workspace schemas require an explicit backed-up manual upgrade; this updater does not run data migrations. Ordinary compatible updates need no workspace copy or repeated onboarding. Browser drafts survive an update reload in that browser session.

## Publisher configured for this release

- Creator: DeAngelo Scott
- Publisher: Umegro, LLC
- First-party product: ViralTrac
- Creator website: https://deangeloscott.com
- Product/publisher website: https://viraltrac.com
- Canonical project and releases: https://github.com/deangeloscott/businessos/releases

The updater uses this publisher's fixed GitHub repository; imported workspace files cannot supply an executable update URL.
