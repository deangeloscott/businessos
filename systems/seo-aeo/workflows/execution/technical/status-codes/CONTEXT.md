---
id: seo.execution.technical.status-codes
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# HTTP Status & Soft-Error Behavior

## Purpose
Correct HTTP response and soft-error behavior that misleads users, crawlers, or downstream diagnosis.

## Business Outcome
Make resource state truthful and technically coherent so valid content is served reliably, moved content routes appropriately, and genuinely unavailable content does not masquerade as success.

## Run When
Use when 2xx/3xx/4xx/5xx behavior, soft errors, intermittent failures, or template/server response patterns may materially affect users or organic discovery.

## Process
1. Crawl or sample the relevant site/template/URL sets and group response patterns by status, template, path, and likely shared mechanism rather than treating every failing URL independently.
2. Separate intentional responses from accidental ones based on the actual Asset/resource state and user purpose.
3. Trace material internal links, traffic, conversions, backlinks, or important discovery paths into failures only where they help establish business impact or the correct treatment.
4. Identify the shared origin/server/template/routing/content cause where one exists and fix that cause rather than patching symptoms URL by URL.
5. For moved content, use an appropriate redirect; for genuinely removed content, return a truthful terminal response; for valid content, correct misleading soft-error or server behavior. Do not return success merely to suppress errors.
6. Re-test representative affected and boundary cases after changes and preserve recurrence monitoring intent only when repeated failure would materially matter; the host/runtime owns any recurring checks.

## Proportionate Scope
Start with high-value and representative templates/patterns. Expand to broader crawling/log review when failures appear systemic, intermittent, security-related, or difficult to reproduce.

## Verification
- HTTP behavior matches the actual resource state and user experience.
- Soft errors and custom error pages do not misleadingly return success where the underlying resource is unavailable.
- Shared root causes are fixed systemically when supported by the evidence.
