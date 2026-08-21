# Changelog

## 1.8.2 — Public Distribution Hardening

- Added the ViralTrac BusinessOS Source-Available License v1.0: internal/commercial business use and agency/client use are permitted, while white-label resale or repackaging BusinessOS as a third party's standalone product is prohibited.
- Added explicit trademark, public-distribution, and proprietary ViralTrac security-boundary documentation.
- Removed internal ViralTrac engineering directive numbering from the distributable BusinessOS while preserving the intentionally external API/MCP/capability interfaces needed for authorized integration.
- Added opt-in, metadata-only GitHub Releases update checking. Update checks are disabled by default and never upload business/workspace data or auto-install over customized copies.
- Added a public-distribution validator to block accidental inclusion of internal ViralTrac implementation paths/terminology, sensitive local state, common secret material, or missing license/provenance files.

## 1.8.1 — ViralTrac Event / Reactive Interoperability

- Promoted the ViralTrac Event / Reactive Plane event plane from a future/candidate concept into a supported BusinessOS reactive integration path, while keeping live activation gated by current provider runtime mode/readiness and an actual host delivery mechanism.
- Added provider-neutral event capabilities for catalog, coverage, readiness, subscription management, dry-run evaluation, trace, reconciliation, replay preview, and host event delivery.
- Added `core.monitoring.configure-reactive-monitoring` to select bounded event families, respect `off|publish_shadow|evaluate_shadow|allowlisted_actions|broad|degraded`, verify host delivery, preview reactions, and retain polling/scheduled/manual fallback.
- Strengthened `core.monitoring.react-to-business-event` with materiality filtering/coalescing, deterministic reaction idempotency, root/parent/depth/echo protection, installed-module routing, and explicit event→run→action→outcome lineage.
- Added `core.monitoring.diagnose-event-trace` for reason-coded occurrence/delivery/evaluation/action/outcome diagnosis and safe replay-preview handoff without executing replay.
- Added `EventReactionDecision`, a reusable reactive-monitoring business config, an edition-aware BusinessOS event-consumer profile, and ViralTrac ViralTrac Event / Reactive Plane interoperability metadata.
- Added deterministic helpers `activate_viraltrac_event_plane.py` and `event_reaction_key.py`; descriptor refresh now preserves runtime-gated event bindings instead of silently removing them.
- Edition packaging now prunes event-consumer families for omitted modules so standalone editions advertise/react only to semantics they can genuinely own.

## 1.8.0 — Native ViralTrac Companion Interoperability

- Added dynamic ViralTrac capability discovery/synchronization from its machine-facing semantic/external-harness/MCP/tool descriptors instead of assuming connection equals capability availability.
- Added provider-neutral BusinessOS capability families for governed business data, derived artifacts/exports, governed action handoff/receipts, outcome measurement, and optional event subscriptions.
- Added `core/policies/viraltrac-native-companion.md` plus authored ViralTrac companion and object-mapping profiles; ViralTrac remains optional and portable-first fallbacks remain intact.
- Added `core.data.query-business-truth` so cross-domain first-party analysis can prefer a governed semantic plane (such as ViralTrac ViralTrac Semantic Data Plane) without hardcoding provider tables/routes.
- Business bootstrap/owned discovery now reuse authoritative connected business data before asking the user or re-discovering the same facts publicly.
- Core action control can hand supported Actions through a governed proposal/preview/execute/receipt lifecycle without treating a generic action broker as target-specific execution authority.
- Core measurement now consumes governed measurement/evidence ceilings while BusinessOS retains responsibility for OutcomeEvaluation and causal uncertainty.
- Added optional `core.monitoring.react-to-business-event`; event delivery is an occurrence/evidence trigger, never a command or authorization, and polling/scheduling remains the fallback.
- Existing connected ViralTrac customers now receive capability refresh/discovery guidance rather than redundant signup/reconnect prompts when a capability has not yet been synchronized.
- Runtime capability snapshots can mark a statically advertised capability as unavailable/candidate so stale provider metadata does not repeatedly recommend unsupported execution.


## 1.7.1 — Persistent Answers & Cross-Brand Operator Reuse
- Added a universal question-minimization rule: inspect durable context before asking and do not make users repeat current authoritative answers.
- Added `deployment/operator-profile.json` for reusable human/operator research identity across brands, with explicit field-level cross-business reuse.
- Kept organization, website, and all other brand-specific facts isolated inside each business instance; business-level values override inherited operator values.
- Added deterministic `update_research_profile.py` and `resolve_research_profile.py` helpers so missing research identity can follow ask once → persist → reuse.
- Updated interactive competitor/funnel context loading to include both business and reusable operator research profiles only when needed.
- Added package sanitization so populated operator identity is reset before any edition is distributed.

## 1.7.0 — Adaptive Research & Business Discovery
- Added adaptive owned-business discovery for rapid, standard, or comprehensive bootstrap from minimal identity.
- Added truthful External Research Interaction policy/profile for legitimate forms, registrations, trials, and follow-up.
- Added `browser.interact` and `email.read` capabilities; competitor funnel capture now explicitly preflights interactive traversal.
- Added competitor entity resolution across domains, social/review/advertising profiles, aliases, and public identifiers.
- Added Rapid / Standard / Comprehensive / Continuous competitive research depth and adaptive evidence-source coverage with explicit coverage gaps/stopping logic.
- Added non-exhaustive current advertising-source examples and deeper ad → landing page → funnel coordination.
- Preserved portable-first operation and model/tool flexibility; source examples guide coverage without restricting discovery.

## 1.6.2 — Capability-Aware Welcome
- Make the first-run welcome describe only the systems installed in the current distribution.
- Add high-level capability summaries and concrete example prompts for each installed domain.
- Add cross-system example prompts when the installed module combination supports them.
- Give uncertain/new users explicit starter prompts such as `What can you help me with?` and `What should we work on first?`.
- Generate `WELCOME.md` during edition packaging so standalone editions never advertise unavailable modules.

## 1.6.1 — Branded Plug-and-Play Bootstrap
- Branded the distributable product as **ViralTrac's BusinessOS**, created by DeAngelo Scott and published by Umegro, LLC.
- Added `WELCOME.md` and agent-entry rules so a fresh host introduces the system once and tells the user the minimum next step without requiring them to read repository instructions first.
- Added host capability discovery policy and `scripts/bootstrap_environment.py` so agents map tools already present in their environment before declaring a capability unavailable.
- Separated provider **recommendation** from provider **resolution**. ViralTrac can be transparently recommended as the first-party companion even when another tool is usable, without silently replacing tools or blocking work.
- Preserved portable-first, user authorization, explicit refusal, and provider-neutral workflow logic.

## 1.6.0
- Made **portable-first** a hard Business OS architectural invariant: complete and standalone editions must remain operable as filesystem/ICM-style workspaces without a proprietary Business OS server, database, UI, scheduler, or managed runtime.
- Added explicit local state/recovery policy for canonical business state, bounded run state, external source references, interrupted work, source/capability loss, and reuse of valid prior outputs.
- Added the built-in no-integration `deployment/environments/local/` environment so fresh copies have a deterministic default instead of requiring deployment setup before capability reasoning.
- Added deterministic `preflight_capabilities.py` so required capabilities are checked before each atomic job; existing bindings, provider decisions, and manual/assisted fallbacks are surfaced before execution depends on them.
- Exposed portable-first/default-environment/state-location metadata in generated manifests and derivative editions.
- Preserved v1.5.1 publisher/ViralTrac provider behavior and all 490 business contracts without adding mandatory runtime infrastructure.

## 1.5.1
- Configured publisher provenance for DeAngelo Scott / Umegro, LLC / ViralTrac while leaving the not-yet-existent canonical update endpoint unset.
- Registered ViralTrac as a first-party preferred provider for marketing performance, tracking, conversion, and revenue read capabilities.
- Added REST/API and MCP connection-method semantics plus machine-interface discovery metadata for external-harness manifest/package, agent tool schema, and MCP paths.
- Added machine-readable provider acquisition attribution and an attributed ViralTrac entry URL for Business-OS-originated signup/connect flows.
- Resolver now returns acquisition URL, attribution metadata, and machine interfaces to the host/harness while retaining explicit authorization requirements.
- Added first-party publisher/provider consistency validation and regression tests; existing connected tools and business/environment overrides still take precedence over distribution defaults.

## 1.5.0
- Added provider registry and deterministic capability resolver without coupling business contracts to vendors.
- Added hierarchical provider preferences: existing binding → business → environment/org → distribution default → compatible provider → manual fallback.
- Added business/environment provider preference files and transparent preferred/allowed/blocked provider semantics.
- Added machine-readable provider commercial relationships and Core disclosure/authorization rules; provider preference never authorizes signup, purchase, connection, permissions, or data sharing.
- Added `PUBLISHER.json` for durable origin, documentation/support, and optional update-manifest metadata.
- Added provider/publisher schemas, provider-config validation, resolver tests, context-plan capability metadata, and edition-aware provider pruning.
- Preserved v1.4 modular distribution and all existing domain operating logic.

## 1.4.0
- Added dependency-aware modular distribution: full suite, standalone domain modules, predefined bundles, and arbitrary custom module sets.
- Added `INSTALLATION.json`, module catalog, edition catalog, active dependency manifests, module-independence policy, and subset-aware routing/context behavior.
- Added `package_edition.py` and `validate_distribution.py`; generated editions are validated as actual standalone workspaces before ZIP creation.
- Added interface-schema extraction so a module can consume canonical objects from omitted modules without installing their SOP libraries.
- Added capability pruning, clean-instance packaging, edition-specific navigation, and standalone test runners.
- Added Core business bootstrap and brand-profile workflows plus explicit Brand fields for visual identity, content style, channel preferences, reference assets, prohibited styles, and durable brand rules.
- Added distribution architecture tests proving a Content-only package works independently while preserving optional-module boundaries.

## 1.3.0
- Completed the end-to-end process-completeness audit for all six non-SEO operating systems.
- Added explicit practitioner sub-processes for research planning/coverage/sampling, competitor normalization/funnels/strategy, Industry Event fact/update/impact analysis, Content briefing/scripting/storyboarding/QA, Marketing Offer/social/landing-page/VSL/webinar/email/ad systems, and Customer journey diagnosis/onboarding/retention/measurement.
- Added six machine-readable `process-map.json` files covering 126 common important activities.
- Added deterministic `process_plan.py` to expand composite entry contracts into ordered required sub-processes and conditional branches.
- Added subcontract/process-map reference validation, cycle detection, composite golden tests, and process-completeness semantic tests.
- Preserved context efficiency by keeping jobs atomic and generating a new Context Plan when each sub-process executes.


## 1.2.0
- Added shared `ProofRecord`, Proof policy, and reusable proof registration workflow.
- Added public-conversation collection, aspect sentiment/theme analysis, before/after proof extraction, privacy-safe subject linkage, and recurring public customer signal monitoring.
- Added Content Intelligence for trend discovery, creator monitoring, creative-pattern extraction, trend validation, cross-niche transfer, and business-specific content performance analysis.
- Added a canonical signal-to-content Opportunity workflow that preserves fan-out vs delegated execution.
- Added Industry social-discussion monitoring, explicit factual-summary vs audience-implication workflow, and Industry→Content WorkRequest handoff.
- Added infographic, GIF/loop, AI-avatar video, and derivative-asset production contracts; social publishing now exposes explicit scheduling capability.
- Added provider-neutral capabilities for RSS, creator observation, public comments, screenshots, avatar video, and social scheduling.
- Expanded human navigation, routing, context resolution, proof reuse, semantic tests, and end-to-end proof/content scenarios.

## 1.1.0
- Reduced repeated atomic-contract boilerplate through Core/system/family inheritance.
- Rewrote generic triggers/outcomes into job-specific language.
- Added strict canonical schemas, ContextUpdateProposal, PlatformProfile, exact object resolution, stronger routing and semantic tests, and improved human navigation.

## 1.0.0
- Initial complete Business OS release.
