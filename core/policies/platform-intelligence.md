# Platform Intelligence and Freshness

AURA should separate **durable product operating knowledge** from **volatile external platform knowledge**. Changes in Google, Bing, Meta, LinkedIn, YouTube, AI answer systems, standards, APIs, or other external platforms should normally update verified organization-relevant knowledge/state rather than require an AURA product release.

`PlatformChange` is a durable primitive for a business-relevant verified platform/topic state when preserving that state materially helps future work. Use `python3 scripts/record_platform_change.py ...` when useful.

## Versioning behavior
A stable `semantic_key` identifies one platform/topic (for example `google-search:faq-rich-results`).
- Re-verifying the same **material state** updates `last_verified_at`, `verification_count`, and refs on the current object. Different wording alone is not a material change. After an evidence-grounded semantic comparison determines that later authoritative evidence restates the same material state, call `record_platform_change.py --reverify-current ...`; the helper preserves the canonical identity/state fingerprint and records the later wording/provenance in verification history instead of creating another version. Exact state-summary equality remains only a deterministic fallback, not the definition of semantic sameness.
- A materially different verified state creates a new `PlatformChange`, marks the previous current state `superseded`, and links the versions. Do not use `--reverify-current` when dates, scope, requirements, availability, behavior, or other decision-relevant platform state materially changed.
- Normal retrieval uses only `status=current`; superseded/archived history remains available when later work benefits from understanding what changed.

The capable model/user decides semantic sameness, materiality, and relevance. Deterministic helpers preserve identity, references, state mechanics, and history after that judgment; they do not infer platform meaning from wording alone.

## Evidence and authority
Prefer authoritative first-party platform documentation/specifications and preserve useful `SourceRecord`/evidence refs. Distinguish announced future behavior from current behavior and official claims from independently measured behavior. A platform statement is not proof of a business outcome: rankings, traffic, leads, citations, conversion, or revenue remain unknown until measured for the business.

## Adaptation boundary
A PlatformChange may inform future analysis, a durable Opportunity, WorkRequest, AttentionItem, decision, or ordinary model reasoning when that meaning is actually useful. It does **not** authorize AURA to rewrite its product source or mutate external systems.

If current AURA operating knowledge is genuinely invalidated, changing canonical Playbooks/Workflows/policies is deliberate product-development work with appropriate validation. If only organization-relevant external knowledge changed, update that durable knowledge and let the capable model use it without changing AURA product code.

Industry Intelligence contains deeper reusable operating knowledge for discovering and interpreting industry/platform changes. Core may still preserve a useful verified `PlatformChange` because durable organizational memory should not depend on routing work through a particular operating area.
