---
id: seo.execution.on-page.title-snippet
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- query-page impressions clicks CTR position SERP
---
# Title Snippet

## Purpose
Improve qualified result CTR without misrepresenting page content.

## Business Outcome
Improve valuable organic discovery through title snippet, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Title Snippet**, or when an authorized incident response requires it.

## Process
1. [INTEGRATION] Collect current title, meta description, observed snippets, query mix, positions, impressions, CTR, SERP features, and competitor presentation.
2. [HYBRID] Segment branded/nonbranded, device, market, and mixed intent.
3. [AI] Diagnose whether low CTR is plausibly presentation-related versus position, SERP feature, reputation, or intent mismatch.
4. [AI] Draft title options emphasizing accurate relevance, differentiator, and user value.
5. [AI] Improve meta description/supporting snippet content while acknowledging search engines may generate snippets dynamically.
6. [HYBRID] Check truncation/readability without writing purely to character counts.
7. [HYBRID] Avoid clickbait, unsupported superlatives, or mismatch with page content.
8. [INTEGRATION] Deploy selected version, create Change Event, and set measurement window.

## Verification
- The proposed presentation must accurately match page content and target intent; no clickbait or unsupported claims.


