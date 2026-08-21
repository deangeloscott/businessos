# ViralTrac's BusinessOS v1.8.2

**A portable, AI-native business operating system that gives AI agents structured processes to research, operate, optimize, and grow a business.**

ViralTrac's BusinessOS packages reusable business processes, decision logic, schemas, validation rules, and operating context into a self-contained workspace that can run across different AI models, agent harnesses, tools, and levels of technical sophistication.

**Official repository:** https://github.com/deangeloscott/businessos

This distribution is **source-available, not open source**. Internal business use, customization, and agency/consulting use for clients are permitted under `LICENSE.md`; white-label resale or repackaging it as someone else's standalone BusinessOS product is not.

Business logic remains model/provider/vendor agnostic. Each customer can keep a separate copy and business instance. No proprietary BusinessOS server, database, UI, ViralTrac account, or cloud runtime is required for portable local operation.

## Start

- Automatic first-run message: `WELCOME.md`
- Human: `START-HERE.md`
- AI/agent: `CONTEXT.md`
- License: `LICENSE.md`
- Public distribution/security boundary: `PUBLIC-DISTRIBUTION.md`, `SECURITY.md`
- Publisher/origin: `PUBLISHER.json`
- Installed modules/dependencies: `INSTALLATION.json`, `distribution/ACTIVE-DEPENDENCIES.json`
- Tasks: `TASK-NAVIGATOR.md`

## ViralTrac native companion

When ViralTrac is connected, BusinessOS can dynamically discover its current machine-facing capabilities and use its governed semantic data, measurement, tracking, supported action/receipt surfaces, and event/reactive plane without making ViralTrac a required runtime. The public BusinessOS distribution contains only integration-facing metadata needed by authorized clients; it does not include ViralTrac's proprietary hosted-application source code or private infrastructure.

## Updates

The official public GitHub repository is the stable update source. Update checks are **disabled by default**, metadata-only, and never auto-install. A one-time check can be run with:

```bash
python scripts/check_for_updates.py --force
```

See `PUBLIC-DISTRIBUTION.md`.
