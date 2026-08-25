# Platform Intelligence and Freshness

BusinessOS must separate **software/operating logic** from **volatile external platform knowledge**. Changes in Google, Bing, Meta, LinkedIn, YouTube, AI answer systems, standards, APIs, or other external platforms should normally update verified knowledge/state rather than require a BusinessOS code release.

`PlatformChange` is the minimal portable primitive for a business-relevant verified platform/topic state. Use `python3 scripts/record_platform_change.py ...` when possible.

## Versioning behavior
A stable `semantic_key` identifies one platform/topic (for example `google-search:faq-rich-results`).
- Re-verifying the same **material state** updates `last_verified_at`, `verification_count`, and refs on the current object. Different wording alone is not a material change. After an evidence-grounded semantic comparison determines that later authoritative evidence restates the same material state, call `record_platform_change.py --reverify-current ...`; the helper preserves the canonical identity/state fingerprint and records the later wording/provenance in verification history instead of creating another version. Exact state-summary equality remains only a deterministic fallback, not the definition of semantic sameness.
- A materially different verified state creates a new `PlatformChange`, marks the previous current state `superseded`, and links the versions. Do not use `--reverify-current` when dates, scope, requirements, availability, behavior, or other decision-relevant platform state materially changed.
- Normal retrieval uses only `status=current`; superseded/archived history remains available for audit and change reasoning.

## Evidence and authority
Prefer authoritative first-party platform documentation/specifications and preserve `SourceRecord`/evidence refs. Distinguish announced future behavior from current behavior and official claims from independently measured behavior. A platform statement is not proof of a business outcome: rankings, traffic, leads, citations, conversion, or revenue remain unknown until measured for the business.

## Adaptation boundary
A PlatformChange may trigger impact analysis, an Opportunity, WorkRequest, or AttentionItem, but it does **not** authorize BusinessOS to rewrite its own product logic or mutate external systems. If a current workflow/policy is genuinely invalidated, propose a controlled BusinessOS software update with regression validation. If only external knowledge changed, update the platform state and dependent business work without changing BusinessOS code.

Industry Intelligence owns deeper monitoring/materiality/impact analysis when installed. Core may record a verified platform state as a portable fallback so standalone editions can remain current without impersonating omitted domain analysis.
