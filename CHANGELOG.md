## 1.8.4 — Stable release

- Completed release-confidence validation across representative business domains, cross-domain orchestration, fresh-user onboarding, customer-facing completion, Brand persistence, second-harness portability, clean-session resume, legacy preference migration, and sequential multi-operator shared-state use.
- The v1.8.4 shared-workspace guarantee is explicit: sequential/coordinated multi-session and multi-operator use is supported; arbitrary unsynchronized simultaneous writes to the same canonical object are not claimed conflict-safe.
- Final multi-operator acceptance proved separate operator preferences and Run attribution on one shared business while keeping task authorization out of durable PreferenceProfile state.
- No concurrency runtime, worker pool, scheduler, lock manager, or model/harness-specific fork was added.

### Native Content execution family hardening

- Added inherited Content Intelligence and Content QA family defaults and expanded Production defaults so native execution requires auditable evidence/comparison/mechanism analysis, real medium-native deliverables, and target-specific inspection/correction records. Optional specialist Skills and tools remain selectable enhancements; they are not prerequisites for a complete native result.
- Added a reusable Content-intelligence work-record completion profile. A concise canonical Observation/Insight/Learning can no longer stand in for the sample, comparison, method, limitations, and mechanism analysis that produced it.
- Strengthened promised-medium fallback validation for podcast and presentation. Calibration-F-style keyword Markdown shells now fail, while substantive recording packets and multi-slide production specifications remain portable local fallbacks when rendering is unavailable.
- Strengthened Asset QA across Content/Marketing: each check now needs a concrete method and finding, overall pass state must preserve issues/corrections/limitations and have no blockers, and the record must target an existing exact Asset version rather than a QA wrapper created by the same Run.
- Added `tests/run_content_native_execution.py` with representative intelligence, podcast, presentation, and accessibility-QA regressions derived from Calibration F. The full 69-event qualification is intentionally deferred until representative native execution receives fresh independent quality review.

### Representative G1 Content follow-up

- Tightened the shared Content-intelligence work record so every sampled item carries a literal excerpt present in captured evidence and every sample/finding reference resolves; unsupported creator names, performance multipliers, and placeholder-source conclusions now fail structurally.
- Raised promised-medium floors: articles require at least 500 words of finished audience copy, podcast fallbacks require substantial content plus concrete timecodes and audio/edit cues, and presentation fallbacks require numeric duration plus at least six substantive slides with near-complete visual direction and speaker notes.
- Bound Content QA passes to literal excerpts from text targets, with explicit component/reason handling for non-applicable checks, so QA cannot claim absent diagrams, links, CTAs, metadata, or accessibility features were inspected successfully.
- Strengthened explicit-user `BusinessClaim` provenance by requiring `support_quote` to be a literal excerpt of its bootstrap-grounded SourceRecord rather than trusting a hand-stamped grounding label.
- Made Run completion transactional: after provenance binding and completion state are staged, full active-business validation must pass or the Run and touched canonical evidence are restored to their prior incomplete state.
- Expanded G1-derived family regressions for fabricated intelligence, thin articles, untimed podcast prose, five-slide shells, absent-feature QA, forged support quotes, and completion rollback. The full 69-event qualification remains deferred until these representative fixes receive another small independent run.

### RC18 candidate: Legacy PreferenceProfile migration hardening

- Added deterministic `scripts/migrate_preference_profiles.py` for businesses upgraded from RC16/earlier state that already contains authorization/approval semantics inside otherwise legitimate `PreferenceProfile` objects.
- Migration is dry-run by default and `--apply` is explicit. It removes only values rejected by the current preference semantic guard, preserves legitimate preference leaves and unrelated business history, and never synthesizes `Approval` or other standing authority from historical restrictions.
- Applied migrations record only removal paths, reasons, and value fingerprints plus before/after preference hashes under non-authoritative migration metadata; removed authorization content is not copied into a new permission store.
- Migration is idempotent: a second apply is a no-op and does not rewrite already-clean profiles.
- Added `tests/run_preference_profile_migration.py`, covering mixed legitimate/invalid legacy state, dry-run safety, preservation, no authority synthesis, active-business validation, and byte-stable second execution.
- RC17 enforcement remains fail-closed for newly created/updated PreferenceProfiles; RC18 adds the missing safe upgrade path rather than weakening that boundary.

### RC17 candidate: Preference / Authorization State Separation

- Added deterministic `PreferenceProfile` semantic validation so reusable style/work-method preferences cannot become a durable authorization, approval, permission, publishing/deployment/spend/contact boundary store.
- `upsert_preference_profile.py`, task-preference loading, preference resolution, and active-business validation now fail closed when permission/approval semantics are placed in preference payloads.
- Current task/action boundaries remain valid in the user request and bounded Run/task context; formal persistent authorization continues through the governed `Approval` lifecycle.
- Added `tests/run_preference_authorization_separation.py`, reproducing the clean-session issue where an earlier “do not publish without approval” boundary could otherwise be remembered as an operator preference.
- Existing preference precedence, Brand onboarding, Run preference snapshots, customer-facing production completion, routing, evidence, and domain semantics are unchanged.

# Changelog

### RC16 candidate: first-class Brand onboarding hardening

- Added `--brand-profile-file` to `bootstrap_explicit_context.py` so explicit organization brand/voice/style/audience guidance can be supplied as a small structured Brand manifest without overloading the general facts JSON. The manifest remains grounded against the original repeated `--source-file` / `--source-text` inputs; unsupported Brand expansion is rejected.
- Multiple Brand manifests may be combined only when their values are non-conflicting. Equal-path conflicts fail closed rather than allowing filesystem/order/model preference to silently choose organization Brand truth.
- Fresh-business bootstrap guidance now explicitly separates first-class `Brand` state from `BusinessClaim` constraints and from operator/team/role `PreferenceProfile` state. Brand voice/style/audience/visual rules should not be flattened into generic claim constraints merely to make onboarding easier.
- Added the canonical `context/brand/` directory to new business initialization and strengthened `core.context.bootstrap-business`, `core.context.brand-profile`, root startup guidance, and agent-execution guidance around the dedicated Brand path.
- Added `tests/run_brand_onboarding.py`, proving: dedicated Brand-manifest onboarding creates one grounded canonical Brand; Brand guidance is not silently converted into BusinessClaims; a later `marketing.assets.landing-page` context plan resolves the Brand without the original conversation; and ungrounded Brand additions are rejected.
- No domain ownership, customer-facing completion, Opportunity/WorkRequest, PreferenceProfile precedence, AttentionItem/PlatformChange, concurrency, scheduling, provider, or agent-runtime semantics changed. This is the final narrow fresh-user golden-path hardening before portability testing.

### RC15 candidate: governed customer-facing completion and operational-promise claim hardening
- Customer-facing production roots can no longer complete on a loose draft file alone; `complete_run.py` requires at least one canonical customer-facing Asset referencing the Run, containing the full contract chain, using the actual outward file as root evidence, and passing claim-manifest validation before completion.
- Expanded the customer-facing claim scanner/validator to catch unsupported operational specifics that do not necessarily name the business, including duration/timing, no-setup claims, and absolute assurance language. Scanner candidates can no longer escape by being labeled `general_guidance`.
- Strengthened onboarding guidance so explicit organization-level brand/voice/style/audience materials are persisted as durable `Brand` context rather than flattened into unrelated claim constraints.
- Added deterministic regressions for customer-facing completion gating and unsupported timing/setup/absolute promises.

### RC14 candidate: fresh-user onboarding and customer-facing draft provenance hardening

- Hardened the RC13 fresh-user golden path after the CrewBeacon acceptance run. The overall outside-in experience succeeded, but the run exposed two general gaps: reusable preferences were persisted only after downstream Runs had already started, and a newly generated homepage draft was mislabeled `customer_facing: false` / `origin: preexisting` while rooted at the leaf `marketing.landing-page.copy` contract.
- Extended `bootstrap_explicit_context.py` for **multi-source onboarding**. Repeated `--source-file` / `--source-text` inputs are grounded together without requiring an agent-created merged Markdown source; canonical provenance preserves original member references and SHA-256 hashes under a deterministic source bundle.
- The bootstrap facts JSON may now contain an explicit grounded `brand` object. Deterministically grounded organization-supplied Brand instructions may be canonical `explicit_user`; agent-assembled Brand/Audience/Offer strategy still cannot self-assert explicit authority.
- Added repeatable `--preference-profile-file` onboarding input. Explicit reusable business/team/role/operator preferences are persisted before residual routing, so the first downstream Run can snapshot them instead of depending on transient chat context.
- Clarified and enforced **intended audience ≠ publication status**. A local/unpublished homepage, landing page, email, ad, proposal, webinar, or similar outward draft remains customer-facing and retains claim/production governance.
- Hardened Run provenance so an object may not combine `origin: imported|preexisting` with a producing `run_ref`. Current execution output cannot be relabeled historical merely because it is local, draft, or awaiting approval.
- Marketing Synthesis Assets may set `customer_facing: false` only for explicit internal support roles (`internal_brief`, `internal_strategy`, `internal_analysis`, `internal_research`, `internal_planning`). Outward drafts cannot escape governance via an arbitrary `internal_working_draft` label.
- Clarified that standalone homepage/landing-page production must root the Run at `marketing.assets.landing-page`; `marketing.landing-page.copy` remains a required leaf subcontract rather than a customer-facing production root.
- Added `tests/run_onboarding_context_hardening.py` and `tests/run_customer_facing_draft_provenance.py`, reproducing the CrewBeacon onboarding/provenance failure modes and proving preference-before-Run snapshotting, explicit Brand grounding, source-member provenance, historical migration compatibility, and rejection of leaf-root/customer-facing opt-outs.
- Final user summaries are now explicitly required to preserve the epistemic strength of canonical decision state rather than strengthening hypotheses into causal claims.
- No domain ownership, WorkRequest, Opportunity, AttentionItem, PlatformChange, concurrency-runtime, provider, or notification semantics changed.

### RC13 candidate: adaptive preferences and multi-operator foundation

- Added canonical `PreferenceProfile` state for durable business/team/role/operator customization without turning preferences into business truth, permission, claims, or measurements. Profiles can be scoped to systems/contracts/output types/channels and remain isolated inside each business instance.
- Added deterministic `scripts/resolve_preferences.py` with explicit precedence `business → team → role → operator → one-task preference`, nested merge/provenance, applicability filtering, and fail-closed equal-precedence conflict detection instead of arbitrary last-writer behavior.
- Added `scripts/upsert_preference_profile.py` so organizations can configure preferences without editing BusinessOS contracts/product files. Brand/company rules remain in canonical Business Context; measured evidence about what works remains `Learning`.
- Extended bounded Runs with optional `operator_ref`, `team_ref`, `role_ref`, and `preference_snapshot_ref`. `create_run.py` accepts explicit labels or `BUSINESSOS_OPERATOR_REF` / `BUSINESSOS_TEAM_REF` / `BUSINESSOS_ROLE_REF` environment defaults and deterministically snapshots effective preferences (including optional output-type/channel applicability context) for reproducible execution. Existing Run snapshots remain fixed even if profiles change later.
- Integrated resolved preferences into `context_plan.py`, including reuse of the Run-local snapshot when `--run-id` is supplied. Every context plan now loads the preference/adaptation and shared-workspace coordination policies.
- Added `core/policies/preferences-and-adaptation.md`: BusinessOS/business/Brand/compliance/approval/contract/task requirements outrank preferences; preferences outrank defaults; valid better/faster/easier implementation methods may replace incidental technique without a BusinessOS release when the same outcome/evidence/authorization/validation contract is satisfied.
- Added `core/policies/shared-workspace-coordination.md`: BusinessOS remains durable coordination/state rather than an agent runtime. Sequential multi-session/shared-state use is supported; harnesses own spawning/scheduling/parallelism; arbitrary simultaneous independent writes to the same canonical object are explicitly **not** claimed conflict-safe yet.
- Added `tests/run_preferences_multioperator.py`, proving business/team/role/operator resolution, distinct operator results in one business, task-level preference override, applicability filtering, run attribution/snapshotting, context-plan reuse, same-precedence conflict failure, and explicit same-scope priority override.
- No agent-spawning runtime, scheduler, notification service, worker pool, lock manager, or concurrent-write claim was added. Concurrency-safe mutation primitives remain evidence-driven future work rather than being assumed by this release.

### RC12 candidate: bootstrap/reference identifier robustness

- Closed a shared bootstrap/reference-validation defect exposed during the ClearLedger cross-domain live run. Long `BusinessClaim` slugs could be truncated exactly on `-`/`_`, producing schema-valid IDs such as `clm_<business>_constraint-...-`; the generic reference scanner used word-boundary matching and then misread the same ID without its final separator as an unresolved reference.
- `bootstrap_explicit_context.py` now trims separator characters after the fixed-length claim-ID truncation so newly generated claim IDs remain clean and stable for downstream tooling.
- `validate_references.py` now matches complete canonical IDs with identifier-aware lookarounds instead of `\b`, preserving schema-valid historical/custom IDs that legitimately end in `-` or `_`. This keeps existing state migration-safe rather than requiring ad hoc renames.
- Added `tests/run_bootstrap_reference_ids.py`, reproducing both ClearLedger failure strings, proving fresh bootstrap output validates without manual ID repair, and proving legacy trailing-separator references remain resolvable.
- No schemas, domain ownership, WorkRequest, Opportunity, Run, claim-governance, AttentionItem, PlatformChange, notification, scheduler, or external-action semantics changed. The ClearLedger cross-domain orchestration behavior itself passed representatively; RC12 only removes the unrelated bootstrap/reference friction encountered on the way.

### RC11 candidate: semantic PlatformChange re-verification

- Closed the Industry Intelligence Phase 2 lifecycle gap where `record_platform_change.py` treated a semantically unchanged official reminder as a material change merely because the free-text state summary was worded differently.
- Added explicit `--reverify-current` lifecycle mode. After the model/harness performs the evidence-grounded semantic comparison and determines that later authoritative evidence restates the same material platform state, the deterministic helper now refreshes the existing current PlatformChange identity/count/refs instead of creating a version.
- Preserves the canonical `state_summary` / `state_fingerprint` while retaining the later observed wording, fingerprint, timestamp, and provenance in `extensions.verification_history`; re-verification also extends canonical lineage with the new evidence refs.
- Material changes still use the normal helper path and create a new current version with reciprocal supersession links. `--reverify-current` fails closed when no current semantic state exists.
- Updated shared platform-intelligence policy/contract to make the model-vs-helper boundary explicit: semantic sameness is a HYBRID reasoning decision; exact text equality is only a deterministic fallback, not the definition of unchanged platform state.
- Added `tests/run_platform_semantic_reverification.py` reproducing the exact RelayBoard Phase 2 wording-change failure and proving same-ID re-verification plus later material supersession.
- No schema, AttentionItem, Run, domain ownership, notification, scheduler, or self-modification semantics changed. RelayBoard Phase 1/2 canonical state remains usable; continue the same persisted instance into Phase 3 after applying RC11.

### RC10 candidate: portable PlatformChange helper compatibility

- Fixed a portability defect exposed by the RelayBoard Industry Intelligence Phase 1 live run: `scripts/record_platform_change.py` used a backslash inside an f-string expression, syntax accepted by newer Python but rejected by Python 3.11 and earlier.
- Rewrote only the PlatformChange ID helper so the semantic identity algorithm and resulting IDs remain unchanged while the script parses on older local Python runtimes.
- Added `tests/run_platform_python_compat.py` to prevent reintroducing the incompatible expression and to prove PlatformChange ID stability.
- No PlatformChange lifecycle, authority, dedupe, supersession, AttentionItem, Run, domain, schema, or contract semantics changed. Phase 1 Industry Intelligence behavior remains accepted; continue the same RelayBoard persisted state into Phase 2 after applying this narrow update.

### RC9 candidate: generalized bounded Run provenance and completion

- Closed the shared execution-lifecycle gap exposed by the HarborFlow Customer Optimization representative run: new execution-significant decision/action/operational state can no longer pass `validate_business.py` without auditable bounded Run provenance.
- Generalized deterministic Run enforcement beyond customer-facing Content/Marketing Assets to Opportunity/Initiative, ActionPacket/Approval/AttentionItem/ChangeEvent/Incident/VerificationRecord/WorkRequest, Experiment/OutcomeEvaluation, Learning, PlatformChange, and EventReactionDecision state.
- A `run_ref` is not sufficient by itself: the referenced Run must belong to the same business, use a valid installed root contract, be completed, and record the canonical object's actual path in root or required-subcontract completion evidence. This prevents a new object from pointing at an unrelated/stale Run merely to satisfy validation.
- `record_contract_completion.py` and `complete_run.py` now automatically bind canonical JSON evidence to the Run that records it and preserve prior Run-history references for durable objects updated by later Runs.
- Clarified the important semantic distinction: a diagnostic/design Run may complete while a downstream intervention remains unexecuted/blocked and an `AttentionItem` remains open. Run completion proves process/evidence completion; it does not imply production execution.
- Preserved migration compatibility for explicitly imported/preexisting canonical state rather than fabricating retrospective Run provenance.
- Added `tests/run_run_provenance.py` covering the exact RC8 failure, unrelated-Run rejection, correct blocked-intervention completion, automatic provenance binding, and preexisting-state compatibility.
- Preserved RC4-RC8 evidence, decision-grounding, customer-facing mutation, attention/platform lifecycle, routing, distribution, and agent-hardening behavior.

### RC8 candidate: portable attention, platform freshness, and bounded lifecycle

- Added canonical `AttentionItem` as the portable semantic queue for conditions that genuinely require user/harness awareness. BusinessOS owns reason, severity, evidence, blocker, recommended action, dedupe identity, lifecycle, and resolution; Slack/email/push/ticket delivery remains a harness/provider responsibility.
- Added `scripts/upsert_attention.py`, `scripts/list_attention.py`, and `scripts/set_attention_status.py`. Repeated detection of the same semantic condition updates `last_seen` / `occurrence_count` on one item instead of creating new files or repeated notification obligations. Resolved items leave the active queue and can reopen as the same semantic item if the condition genuinely recurs.
- Added canonical `PlatformChange` plus `scripts/record_platform_change.py` / `scripts/list_platform_state.py` so volatile external platform knowledge can change independently from BusinessOS software. Same platform/topic + same verified state refreshes one current record; a material state change creates a new version and supersedes the prior one.
- Added `core/policies/attention-lifecycle.md` and `core/policies/platform-intelligence.md`. Platform facts remain separate from measured business outcomes, and external changes may trigger Opportunities/Attention but never authorize uncontrolled BusinessOS self-modification.
- Added `scripts/maintain_lifecycle.py` to move old resolved/superseded AttentionItems and superseded PlatformChanges out of active folders into canonical history without deleting durable evidence or breaking references. This keeps current state small while retaining meaningful audit history.
- Added `scripts/validate_attention_lifecycle.py` and integrated it into `validate_business.py`; duplicate active attention dedupe keys, duplicate current platform semantic keys, and broken supersession links fail validation.
- Added `core.attention.manage` and `core.intelligence.record-platform-change`; existing authorization, delegation, event reaction, and Industry technology/platform monitoring now use the shared primitives where appropriate.
- Preserved the existing portable Event/reactive-monitoring plane rather than creating a BusinessOS notification daemon. Harnesses/models may poll/watch `AttentionItem` state or use their own scheduler/event capabilities.
- Added deterministic regressions for no-spam dedupe, acknowledgement/resolution/reopen, unchanged platform re-verification, material supersession, active/current uniqueness, history archival, reference preservation, and policy loading.
- SEO/AEO diagnosis and execution are accepted/frozen from RC7; RC8 is a shared Core foundation intended to be exercised naturally by upcoming Customer Optimization / Industry Intelligence monitoring tests rather than reopening SEO/AEO.

### RC7 candidate: claim-safe mutation of existing customer-facing assets

- Extended customer-facing claim governance beyond newly produced Content/Marketing Assets to **existing customer-facing surfaces mutated by any BusinessOS workflow**, including SEO/AEO and Customer Optimization.
- Added `core/policies/customer-facing-mutations.md`: a technical, structural, CRO, or SEO task may remove/narrow unsupported content, but may not rewrite it into a new advertised service/capability/promise without canonical support.
- Added `scripts/capture_customer_facing_state.py` and `scripts/build_mutation_claim_manifest.py` to preserve pre-change customer-facing text and deterministically compute only the business-specific claim candidates introduced by the mutation. Existing unchanged claims are not re-litigated.
- Added `scripts/validate_customer_facing_mutations.py` and integrated it into `validate_business.py`. Verified/applied `ChangeEvent` objects that mutate governed customer-facing files must reference reproducible before/delta artifacts; all changed/added customer-facing files must be represented in the ChangeEvent; each declared customer-facing target must actually differ from the before capture (blocking post-hoc fake "before" captures); newly introduced claims reuse the same substantive support rules as Content/Marketing claim manifests.
- Context planning now loads the mutation policy and `BusinessClaim` context for contracts that write `ChangeEvent`.
- Added the exact live SEO execution regression: replacing a broken `/services/maintenance.html` link with `Contact us about maintenance` is rejected when maintenance is not an established ProductService/BusinessClaim; safe removal passes; disguising the CTA as general guidance fails; unrelated repair support cannot authorize maintenance; a supported repair CTA remains allowed; and a newly created maintenance page cannot be hidden from the ChangeEvent.
- Preserved RC6 source-identity/historical-evidence behavior, RC5 decision grounding, and RC3 customer-facing production claim controls.
- SEO/AEO diagnosis remains accepted/frozen. SEO/AEO execution functionally passed and RC6 evidence identity was live-confirmed; RC7 requires one targeted rerun of the execution fixture before freezing execution.


### RC6 candidate: local-evidence source identity and historical capture preservation

- Changed deterministic local-site evidence identity from content-snapshot-only to the pair `(source identity, snapshot hash)`, where source identity is derived from the normalized workspace-relative locator.
- Byte-identical baseline, staging, working-copy, or cloned site roots now receive independent manifests and SourceRecords instead of overwriting one another.
- Same source + same snapshot capture is idempotent; same source + changed snapshot creates a new evidence capture while older captures remain immutable history.
- `validate_local_evidence.py` now binds `SourceRecord.source_reference` to manifest `source_root` / `source_identity` and rejects provenance relabeling.
- Historical captures no longer fail whole-business validation merely because the original source later changed. They cannot support a new current direct Observation until the current source state is recaptured.
- Added the exact SEO/AEO execution regression: capture two identical site roots independently, mutate the writable root, recapture it, and require baseline + working-before + working-after evidence to coexist and validate.
- Preserved RC4 direct-site fact grounding and RC5 Opportunity decision-grounding controls unchanged.
- SEO/AEO diagnosis remains accepted/frozen. SEO/AEO execution functionally passed on RC5; RC6 requires one targeted live rerun of the same execution fixture before freezing execution.

## 1.8.4 — Agent Execution Hardening
### RC5 candidate: canonical decision grounding and inference-boundary hardening
- Added `core/policies/decision-grounding.md` so verified facts no longer automatically authorize their downstream economic, causal, ranking, traffic, lead, conversion, or AI-answer consequences inside canonical Opportunities.
- Extended the canonical `Opportunity` schema with required `reasoning_basis` for `qualified`, `prioritized`, `committed`, and `active` Opportunities. The basis explicitly separates established `fact_refs`, actual `measured_refs`, derived `inferences` with basis/confidence, and material `unknowns`.
- Added `scripts/validate_opportunity_grounding.py` and integrated it into `validate_business.py`. It rejects unsupported active-business economic/value superlatives, absolute search/AI outcome claims inferred from prerequisite technical signals, and unmeasured performance assertions; deterministic local-site Observations cannot be relabeled as measured search/AI/business performance.
- Context planning now automatically loads the decision-grounding policy for every contract that writes `Opportunity`, making the rule shared across installed systems rather than SEO-specific or harness-specific.
- Added deterministic regressions for the exact RC4 SEO diagnosis failures: “replacement is the highest/high-value service” fails without business-specific economics; a robots block cannot be canonically restated as “preventing indexing and any AI-answer citation”; unmeasured traffic/ranking claims fail; and a calibrated dependency-first Opportunity with explicit inference/unknowns remains valid.
- Preserved RC4 deterministic site evidence unchanged. The model still diagnoses and prioritizes; RC5 governs how those verified observations are promoted into durable decision state.
- RC5 deterministic validation is clean, but SEO/AEO diagnosis is **not yet live-accepted** on RC5; rerun the same controlled Northstar diagnosis once in a fresh RC5 workspace before freezing the diagnosis workflow.

### RC4 candidate: deterministic first-party/local evidence verification
- Added `core/policies/local-evidence.md`, the first-party/local counterpart to research-evidence preservation. A model saying it inspected a deterministic file is no longer enough to make a material direct site Observation canonical.
- Added `scripts/inspect_site_evidence.py` to produce a reproducible local-site evidence manifest with per-file hashes, a snapshot hash, and deterministic facts for titles/H1s, meta descriptions, canonicals, meta robots, JSON-LD parse validity/context/type, internal-link target existence, image alt presence, robots rules, sitemap URLs/membership, and parsed wildcard robots blocking.
- Added `scripts/persist_site_observation.py`; direct SEO website Observations can now be generated from selected deterministic fact IDs rather than hand-authored prose. The canonical Observation statement is derived from the preserved facts and records the exact manifest/snapshot/fact refs.
- Added `scripts/validate_local_evidence.py` and integrated it into `validate_business.py`. Observations that rely on a local website/export SourceRecord must use deterministic capture; hand-authored local SourceRecords cannot bypass the path, modified source files make prior evidence stale, and a direct Observation whose statement differs from its fact refs fails validation.
- Updated SEO/AEO technical baseline, asset inventory, technical/indexing diagnosis, and AI-citation-gap guidance to use deterministic local-site evidence for mechanically inspectable facts while keeping severity, business consequence, search visibility, and AI-answer behavior as inference/unknown unless separately measured.
- Added release regression coverage for the exact SEO acceptance failure: valid homepage JSON-LD with `@context=https://schema.org` is deterministically captured as valid, and a later model-written claim that it is corrupted is rejected rather than becoming canonical truth.
- Preserved the existing SEO/AEO semantic architecture: the model still diagnoses and prioritizes; deterministic helpers verify only cheap, reproducible file facts. No new semantic registry, harness dependency, cloud service, or model-specific branch was introduced.

### RC3 candidate: substantive claim support and production-root provenance hardening
- Hardened `validate_business_claims.py` so a trusted canonical reference must **substantively authorize the customer-facing predicate**; an unrelated trusted Business/Market/BusinessClaim can no longer act as a permission token merely because it exists or shares the business name.
- Added conservative action/object support matching for customer-facing business claims while preserving narrow paraphrases such as “request a written estimate” from the approved claim “we provide written estimates.”
- Expanded promise-escalation protection to catch unsupported availability breadth such as `any time` / `anytime` in addition to the existing guarantee, timing, financing, discount, warranty, quantifier, and no-pressure controls.
- Added authored contract metadata `artifact_role: customer_facing_production_root` to legitimate Content/Marketing production entry contracts. This remains part of the existing contract source of truth and generated registry; no new playbook registry was introduced.
- Hardened `validate_run_completion.py` so a customer-facing Content/Marketing Asset must reference a producing Run whose root contract carries that production role, whose owner matches the Asset, whose `contract_chain` includes the producing root and required subcontracts, and whose root completion evidence includes the actual customer-facing deliverable file.
- This closes the RC2 loophole where an agent could complete a strategy/helper Run such as `content.strategy.format-platform`, create the final Asset afterward, point the Asset at that Run, and still pass completion validation.
- Added deterministic regressions reproducing the live RC2 Content failure: unrelated trusted identity support cannot authorize written-estimate/repair-vs-replace promises; unsupported `any time` expansion fails; strategy-only Runs cannot prove customer-facing production; and a legitimate production Run cannot complete an Asset using unrelated evidence instead of the deliverable.
- Replayed the saved RC2 acceptance states against RC3 controls: the previously accepted bad Content state is rejected at both the claim-support and production-root boundaries, while the legitimate Marketing CTA “request a written estimate” remains semantically supported. The old RC2 Marketing state is additionally rejected only for lacking RC3's newly required `contract_chain`.

### RC2 candidate hardening
- Added canonical `BusinessClaim` context for explicit reusable customer-facing claims/promises and claim constraints so Marketing/Content do not need to turn a model-authored Brand/Offer into fake `explicit_user` truth.
- Extended `bootstrap_explicit_context.py` with `approved_claims` / `claim_constraints` (and CLI equivalents) so these statements are source-grounded through the same deterministic explicit-context path.
- Hardened active-business provenance: agent-assembled Brand, AudienceSegment, and Offer objects may no longer self-assert `explicit_user` authority by manually stamping bootstrap metadata; derived strategy must be labeled `derived_inference` / `candidate_strategy` with a basis.
- Added `core/policies/context-provenance-and-claims.md`, separating generation constraints from business promises and prohibiting creative expansion of an authorized claim into a larger commitment.
- Added `scripts/build_claim_manifest.py` and `scripts/validate_business_claims.py`; customer-facing Content/Marketing Assets now require a claim manifest covering business-specific/promise-like statements, canonical support refs, and protection against unsupported high-risk promise expansion such as guarantees, timing, discounts, financing, warranties, “both/every” commitments, or no-pressure promises.
- Added auditable required-subcontract execution to Runs. `create_run.py` now creates `contract-execution.json`; `record_contract_completion.py` records evidence per required subcontract; QA requires a matching JSON pass record; `complete_run.py` blocks root completion until required subcontracts are evidenced.
- Integrated production-run completion validation into `validate_business.py`; Content/Marketing Assets must reference a completed Run unless explicitly marked imported/preexisting, and the Asset contract chain may not omit declared required subcontracts.
- Updated Landing Page and Content pre-publish contracts so a final-answer claim that “QA ran” is insufficient without the declared QA pass record and Run completion evidence.
- Added deterministic regressions reproducing the cross-workflow acceptance failures: forged explicit-user strategy, unsupported marketing-promise expansion, missing claim manifests, and implied-but-unevidenced required QA/subcontracts.
- Added acquisition provenance for research evidence: `acquisition_method` now records how the underlying source was obtained, separately from `capture_method`, which records what was saved.
- Research persistence/validation now rejects search-result, snippet, directory-preview, AI-summary, unvisited-URL, or unknown acquisition as support for material public Observations even when `captured_text` is present.
- Added sample-scope protection for supported/active prevalence and superlative Insights: broad claims such as “top,” “#1,” “most common,” or “dominant” must be scoped to the sampled evidence unless backed by a measured population basis.
- Hardened the shared external-research evidence path: material public-source claims now require preserved/reproducible underlying evidence rather than a URL or search-result snippet alone.
- Added `core/policies/research-evidence.md` with simple rules for exact text/metadata capture, optional screenshots/snapshots, authoritative external pointers, supported-insight evidence chains, and opportunity-vs-business-promise boundaries.
- Added `scripts/persist_research_bundle.py` so agents can persist SourceRecords, evidence Assets, Observations, supported/candidate Insights, and basic Competitor objects from one small structured bundle instead of reverse-engineering schemas or writing one-off canonical-writer scripts.
- Added `scripts/validate_research_evidence.py` and integrated it into active-business validation so schema-valid research can still fail when a supported/active Insight lacks an adequate evidence chain.
- Updated review/public-conversation/competitor-sentiment playbooks to open the underlying source, preserve bounded evidence before analysis, use the deterministic persistence helper, calibrate frequency claims to the actual sample, and keep unsupported conclusions `candidate`.
- Clarified that research may surface a candidate opportunity, but external evidence does not authorize new active-business services, guarantees, response-time promises, positioning, or other commitments without business-specific feasibility and authorization.
- Added a plain-language **BusinessOS Playbook Catalog** (`PLAYBOOKS.md`) generated from the existing contracts/process maps, plus edition-aware domain pages under `docs/playbooks/`. The contracts remain the source of truth; the new pages make specific jobs easier for people to browse without learning BusinessOS internals.
- Added a worked public-review research example showing source discovery, text/evidence capture, screenshots when useful and permitted, deduplication, analysis, reusable BusinessOS objects, downstream routing, and stopping logic in simple language.
- Surfaced the catalog through Welcome/Start/README navigation and edition packaging so users can ask “what can BusinessOS do?” or browse specific jobs without being required to choose a playbook.
- Hardened post-bootstrap completion so conversational setup carries any unresolved original outcome through `--residual-request`; bootstrap now returns the deterministic residual route/precheck in the same success payload, while `--initialization-only` explicitly marks true setup-only requests.
- Added regressions preventing plausible-but-unstated business-model labels such as `contracting` and `service business` from receiving `explicit_user` authority from the Northstar statement.
- Refined baseline questioning: universal constraint classes should be translated into business-contextual questions only when each question can materially change diagnosis/prioritization; domain relevance is encouraged without industry-question boilerplate.
- Prohibited unsupported user-effort duration claims (for example, invented "15–30 minute" collection estimates) unless grounded in known workflow/resources or explicitly requested as a rough estimate.
- Improved bootstrap ergonomics guidance to prefer relative runtime facts paths and avoid avoidable shell/path quoting failures.
- Added a protected **BusinessOS operating-scope boundary**: ordinary business work may operate business/runtime artifacts but must not patch product scripts/contracts/schemas/tests to work around failures; product changes remain allowed when the user's request itself is BusinessOS development/repair/configuration.
- Hardened supported-path integrity so a failed deterministic helper must be corrected through its documented interface rather than bypassed with a custom canonical writer or hand-stamped `explicit_user` state.
- Simplified explicit-context bootstrap for unfamiliar agents with `--business-id` alias support, JSON file/inline/stdin intake, stronger `--help` examples/errors, required grounding source, and deterministic validation/residual-routing handoff.
- Added provenance-aware active-business validation: schema-valid canonical objects claiming `explicit_user` authority must point to a grounded SourceRecord and pass semantic source checks; hand-authored plausible state is no longer trusted merely because its JSON validates.
- Added `scripts/growth_baseline_gate.py` and business-aware `route_and_resolve.py --business-id` prechecks so fresh broad profitable-growth requests deterministically prefer a minimal first-party constraint baseline before generic competitor/SEO/content/customer research.
- Added supplementary-artifact restraint: normal operation should not create welcome files, Markdown mirrors, helper scripts, or convenience artifacts merely to restate canonical state.
- Clarified calibrated inference: strongly entailed implications may guide reasoning without being mislabeled as explicit user truth, while unsupported specifics remain unknown.
- Extended truth/provenance hardening from canonical JSON to **all active-business artifacts and answers**: Markdown, plans, code, webpages, marketing copy, tool inputs, and generated assets may not assert unsupported business-specific claims.
- Added explicit **unknown != absent** semantics. Missing/unprovided/unfound websites, profiles, offers, capabilities, or other business state remain unknown unless absence is authoritatively established; fictional/test businesses follow the same rule.
- Added request-scope/authorization hardening: “determine/recommend what to do next” authorizes prioritization, not implementation; clarification/user/tool/provider timeout is never approval.
- Strengthened next-best-work to prefer a minimal first-party profitable-growth/constraint baseline when acquisition/conversion/retention/economics/capacity cannot yet be distinguished, rather than substituting broad competitor/industry research.
- Tightened resource-aware orchestration: default broad diagnosis/prioritization to one bounded discovery loop, delegate only when specialization/parallelism is justified, salvage partial evidence before retries, and avoid recursive delegation after provider failures.
- Hardened owned-business discovery so search misses do not prove asset absence and broad similarly-named-company searches are not used to manufacture an “existing assets: none” conclusion.
- Added resource-aware execution: minimum sufficient work, progressive research depth, explicit stopping conditions, selective fan-out, and conservation of tokens, tool/API spend, compute, elapsed time, and human attention.
- Hardened next-best-work and broad diagnosis to research only decision-critical unknowns, diagnose before intervention, and stop when more evidence is unlikely to change the decision materially.
- Added evidence-calibrated opportunity qualification so external benchmarks remain external, unknown business state remains unknown, and company-specific ROI/impact claims require company-specific inputs.
- Made prioritization automation-aware without assuming automation is free or authorized; unknown implementation time/staffing/cost is no longer a reason to apply invented conventional development penalties.
- Improved conversational bootstrap ergonomics by splitting comma-separated service and lead-source values into discrete canonical items, with focused agent-hardening regressions.
- Restored the runnable public `tests/run_all.py` release gate and added routing regressions for broad symptom-vs-goal wording, including traffic/leads growth without revenue growth.
- Added `scripts/route_and_resolve.py`, source-grounded conversational bootstrap checks, and a final-response completion gate to prevent routing-ID confusion, unsupported taxonomy persistence, and department-menu fallbacks.

- Added an explicit agent-execution policy clarifying mandatory boot sequence, contract-ID semantics, canonical persistence, truth/provenance boundaries, residual-intent continuation, active-business validation, and destructive-cleanup safety.
- Added `scripts/resolve_contract.py` so any agent can deterministically map a contract ID to its operating `CONTEXT.md` instead of treating IDs as executable paths.
- Added `scripts/bootstrap_explicit_context.py` to persist only user-supplied initial facts as schema-valid Business/Market/ProductService/Objective objects with SourceRecord lineage; unknown values remain unknown.
- Added `scripts/validate_business.py` to validate active business objects/references/isolation without misusing release/public-distribution tests.
- Hardened `core.context.bootstrap-business` to prohibit invented business facts/free-form context substitution and to continue unresolved user goals such as next-best-work after setup.
- Added agent-execution acceptance tests based on the Hermes/Ollama/Qwen fresh-agent findings.

## 1.8.3 — Natural-Language Orchestration Hardening

- Added workspace-native Core intent resolution so users can state ordinary business goals/problems without knowing BusinessOS systems or contract names.
- Added broad business diagnosis, next-best-work discovery, and multi-domain coordination entry processes while preserving semantic ownership and module independence.
- Changed deterministic routing so weak/ambiguous lexical matches escalate to Core semantic resolution instead of forcing an unrelated atomic contract.
- Preserved high-confidence direct routing for clear jobs such as webinars, competitor pricing, SEO declines, onboarding, and other explicit tasks.
- Added natural-language routing acceptance tests covering direct tasks, diagnosis vs intervention, broad prioritization/growth, compound work, and semantic fallback.
- Restored the canonical `tests/run_all.py` release gate so `scripts/package_release.py` can validate and build a release from the public source tree.

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
