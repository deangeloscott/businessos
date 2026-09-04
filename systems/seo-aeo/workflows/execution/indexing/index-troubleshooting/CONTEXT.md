---
id: seo.execution.indexing.index-troubleshooting
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
- Incident
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Indexing Diagnosis & Recovery

## Purpose
Determine whether important URLs are in the intended discovery, crawl, canonical, eligibility, index, and serving state; diagnose material mismatches; and apply the smallest justified recovery.

## Business Outcome
Protect valuable organic discovery by separating real indexing problems from intentional states, normal propagation, unobserved states, and non-indexing causes—without repeatedly resubmitting URLs or creating an indexing lifecycle controller.

## Run When
Use when the current index state of one or more important URLs is uncertain, unexpected, materially changed, or plausibly harming organic discovery. The same method applies to a single valuable page and to a broad unexpected loss; severity changes response depth and urgency, not the underlying reasoning model.

## Process
1. [HYBRID] Define the affected URL set and intended state. For each material URL or representative segment, gather the strongest available evidence for HTTP response/availability, crawl permission, crawl occurrence, rendered content, meta/X-Robots directives, redirects, canonical signals/selection, sitemap and internal-link discovery, observed index state, serving/search evidence, and relevant timestamps.
2. [AI] Separate the states that are often incorrectly collapsed together: inaccessible, blocked from crawling, not crawled or unobserved, render failure, not eligible for indexing, eligible but not selected/indexed, canonicalized elsewhere, indexed but not serving for the observed query, intentionally excluded, and unknown.
3. [HYBRID] Compare observed state with the intended Asset/SEOAssetState and publish/change timeline. Exclude intentional noindex/redirect/removal states and reasonable propagation lag before treating absence as a defect.
4. [HYBRID] Diagnose likely causes using evidence appropriate to the affected pattern: directives/access, authentication/security, redirects/canonicals, rendering, sitemap/internal-link discovery, orphaning, duplicate/near-duplicate clusters, thin or non-distinct utility, soft errors, template/sitewide patterns, deployment/config changes, or platform diagnostics/log evidence.
5. [AI] Confirm the URL or segment actually serves independent user/business/search value and should be indexed. Do not optimize index inclusion for pages whose intended state or value does not justify it.
6. [AI] Select the smallest root-cause intervention supported by the evidence: reverse an accidental block/noindex/redirect/canonical, repair rendering/access, align canonical/internal-link/sitemap signals, improve distinct value, consolidate/remove an unnecessary page, wait for normal propagation, or investigate an unresolved cause. Do not promise indexing and do not repeatedly resubmit when the underlying problem is elsewhere.
7. [HYBRID] When a broad or high-value segment disappears unexpectedly, prioritize containment and common-cause diagnosis before per-URL work. Check recent deployments/configuration/security changes and reverse clearly accidental high-impact changes when the user's requested action and real external constraints permit it. Preserve an Incident only when the event is materially severe enough that durable cross-session visibility is useful.
8. [HYBRID] After remediation, verify technical eligibility and observe subsequent crawl/index/serving evidence at a sensible interval. Restore discovery signals or use supported URL-notification mechanisms when relevant, but treat successful submission/notification only as evidence that a signal was sent—not as proof of crawl or indexing.
9. [AI] Preserve the material diagnosis, affected scope, root cause, intervention, unresolved uncertainty, and recovery evidence when remembering it will improve future troubleshooting or measurement.

## Verification
- Claimed index state is grounded in observable evidence rather than search-result anecdotes alone.
- Accessibility, crawlability, crawl occurrence, renderability, canonical selection, index eligibility, indexed state, and serving/ranking evidence remain distinct.
- Intentional exclusion, expected lag, unknown state, root cause, severity, and business impact are not conflated.
- Broad-loss response looks for common causes before generating repetitive per-URL work.
- Recovery is verified with subsequent evidence; indexing or ranking is never guaranteed.

## Customer-Facing Mutation Guardrail
If the justified fix changes visible/customer-facing text, navigation, headings, or page content, follow `core/policies/customer-facing-mutations.md`. Prefer removal or narrowing when a broken target refers to a service/capability not established in canonical business truth.

## Deterministic local-site evidence
When scoped evidence is a local/first-party website export, use `scripts/inspect_site_evidence.py` and persist material direct Observations through `scripts/persist_site_observation.py` using captured fact IDs when those helpers apply. Keep consequences, severity, and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.
