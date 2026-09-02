---
id: seo.execution.technical.crawl-access
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
# Crawl Access

## Purpose
Ensure valuable public assets can be discovered and fetched by intended crawlers while preserving intentional privacy, security, and low-value crawl boundaries.

## Business Outcome
Keep important organic assets technically reachable without exposing areas that should remain private or changing crawler rules more broadly than the evidence requires.

## Run When
Use when crawl access is uncertain, valuable URLs appear blocked, crawler controls are changing, or a site/platform change could alter access behavior.

## Process
1. [HYBRID] Define the target URLs/sections, intended public state, and crawlers or discovery systems that materially matter to the current objective. Do not assume every crawler needs identical access.
2. [HYBRID] Inspect the actual access layers that can affect fetching: robots.txt, relevant HTTP/meta directives, response status, redirects, authentication, CDN/WAF/security controls, resource blocking, and other platform behavior.
3. [HYBRID] For robots.txt specifically, parse applicable user-agent groups, allow/disallow precedence, wildcard/boundary behavior, file accessibility/status, and sitemap declarations. Distinguish crawler access control from indexing control; robots.txt is not a guaranteed removal mechanism for already known URLs.
4. [HYBRID] Compare crawler rules with sitemap, internal-link, navigation, and other discovery paths so contradictory signals are visible.
5. [HYBRID] Test representative valuable URLs plus meaningful boundary cases. Use raw and rendered fetch evidence when JavaScript, edge controls, or resource blocking could make the two states differ.
6. [AI] Separate accidental blocks of valuable resources from intentional blocks of private, duplicative, low-value, or operational areas. Preserve security/privacy constraints even when broader crawl access might improve a metric.
7. [AI] Before changing broad path or wildcard rules, reason about the likely blast radius and choose the smallest change that resolves the supported problem. Preserve a rollback path or prior configuration when practical for consequential changes.
8. [HYBRID] Apply the change through the actual host/platform mechanism available under the user's request and real permissions, then refetch/test representative and boundary URLs. AURA does not add an autonomy tier or approval lifecycle.
9. [HYBRID] Observe subsequent crawl/index evidence at a sensible interval when the outcome cannot be verified immediately. The harness owns any later scheduling; AURA may preserve the monitoring intent and material result.

## Verification
- Valuable intended-public URLs are fetchable by the relevant crawlers where technically expected.
- Privacy/security/intentional crawl boundaries remain intact.
- Robots behavior is tested against representative and boundary URLs rather than inferred from one rule line.
- Crawl access is not reported as proof of indexing, ranking, or traffic recovery.
