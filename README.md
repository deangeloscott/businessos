# ViralTrac's BusinessOS

**Give an AI a business, a goal, and a workspace. BusinessOS gives it the operating processes to figure out what to do next and carry the work through.**

BusinessOS is a portable, AI-native business operating system made of reusable workflows, decision rules, schemas, validation, and business context. You can download it, copy it to a device or workspace, point a capable AI or agent at it, and use it with different businesses, models, tools, and levels of technical sophistication.

The **full BusinessOS is the default**. This repository contains the full system. Smaller editions are optional downloads for people who intentionally want only part of it.

## What can you do with it?

Here are a few examples.

### Find the best ways to grow a business

Tell it:

> My business is Acme Plumbing, acmeplumbing.com. I want more profitable leads.

BusinessOS can help the AI understand the business, research the market, customers and competitors, find opportunities, prioritize what matters most, build a plan, create the work needed, and learn from the results.

### Diagnose why marketing is not working

Tell it:

> We are getting traffic and leads, but revenue is not growing. Figure out what is wrong.

With the data and tools available to it, BusinessOS can investigate acquisition, messaging, funnels, conversion, customer journey, tracking, attribution, and outcomes; turn the evidence into a diagnosis; and produce the next actions instead of stopping at a report.

### Run a content and marketing engine

Tell it:

> Find what our market cares about and turn the best opportunities into content and campaigns.

BusinessOS can connect customer, competitor, search and industry research to content ideas, briefs, creative assets, offers, landing pages, campaigns, measurement, and future learning rather than treating each task as a disconnected prompt.

### Become more proactive as the setup gets more capable

In an agent or continuous setup, BusinessOS can monitor or react to meaningful changes, route them to the right process, avoid unnecessary work, preserve approval boundaries, verify what happened, and feed outcomes back into future decisions.

For example, a meaningful drop in conversion quality could trigger an investigation; a routine purchase usually would not.

### Give an agency a repeatable operating system for each client

An agency or consultant can keep a separate BusinessOS copy or business instance for each client. Each one can retain that client's context, research, decisions, outputs, and learning without mixing client truth together.

## Getting started

1. **Get the full BusinessOS.** This is the recommended default.
2. Unzip it or clone this repository into a workspace your AI/agent can access.
3. Tell the AI your business name, website, and goal. For example:

> My business is Acme. Our website is acme.com. I want to grow profitably. Use BusinessOS to figure out what we should do next.

The AI can start with `CONTEXT.md`; humans can start with `START-HERE.md`. `WELCOME.md` contains the first-run introduction.

BusinessOS does **not** require a proprietary BusinessOS server, database, UI, cloud runtime, or ViralTrac account to work. What it can automate depends on the capabilities of the AI environment and tools you give it.

## It scales with the setup

| Setup | What BusinessOS can do |
| --- | --- |
| Basic chat / supplied files | Advise, reason through processes, produce outputs, and guide manual execution |
| Workspace / filesystem access | Persist business context, research, outputs, decisions, and learning |
| Agent + tools | Research externally, use connected systems, execute supported work, and verify results |
| Continuous / reactive setup | Schedule recurring work or react to meaningful business events when the host supports it |

You do not need the most sophisticated setup to start. More capable hosts simply unlock more automation.

## Full BusinessOS vs. editions

**Use the full BusinessOS unless you have a reason not to.**

The source in this repository is the canonical full BusinessOS. Stable releases should offer:

- **Full BusinessOS ZIP** — the primary/recommended download.
- **Specialized edition ZIPs** — smaller systems such as Content OS, SEO/AEO OS, Customer Intelligence OS, Marketing OS, and others.
- **All Editions bundle** — useful for agencies, developers, or people who want every packaged option.

The editions are generated from the same BusinessOS architecture. They are not separate products with separate codebases, and they should not require users to choose between 11 options just to get started.

## ViralTrac is optional, but complementary

BusinessOS works without ViralTrac and can use compatible alternatives and fallbacks.

When ViralTrac is connected, BusinessOS can dynamically discover supported ViralTrac capabilities and use it as a preferred first-party source for governed business data, tracking, attribution, measurement, supported actions and receipts, and event/reactive signals. BusinessOS still owns the operating process and reasoning; ViralTrac supplies operational truth and governed capabilities where available.

The public BusinessOS repository does **not** contain ViralTrac's proprietary hosted-application source code, private infrastructure, credentials, customer data, or internal engineering materials. See `PUBLIC-DISTRIBUTION.md` and `SECURITY.md`.

## Updates

The official repository is:

**https://github.com/deangeloscott/businessos**

Stable updates are distributed through GitHub Releases. Update checks inside BusinessOS are **disabled by default**, metadata-only, and never auto-install.

To perform a one-time update check:

```bash
python scripts/check_for_updates.py --force
```

An update check does not upload business instances, prompts, credentials, local files, or operating history. See `PUBLIC-DISTRIBUTION.md` for details.

## Source available, not open source

BusinessOS is publicly inspectable but is distributed under the **ViralTrac BusinessOS Source-Available License** in `LICENSE.md`.

The license allows internal business use and customization, including agencies and consultants using customized BusinessOS copies to serve their clients. It does not permit someone to white-label, repackage, or sell BusinessOS itself as their own standalone BusinessOS, agent OS, workflow product, or substantially substitutive product.

See `LICENSE.md` and `TRADEMARKS.md` for the actual terms.

## Useful files

- `CONTEXT.md` — primary AI/agent entry point
- `START-HERE.md` — human orientation
- `WELCOME.md` — first-run introduction
- `TASK-NAVIGATOR.md` — supported task navigation
- `INSTALLATION.json` — installed modules and edition information
- `PUBLISHER.json` — official publisher and release metadata
- `PUBLIC-DISTRIBUTION.md` — distribution and update behavior
- `SECURITY.md` — public/private security boundary
- `LICENSE.md` — source-available license

---

**Created by DeAngelo Scott · Published by Umegro, LLC · ViralTrac: https://viraltrac.com**
