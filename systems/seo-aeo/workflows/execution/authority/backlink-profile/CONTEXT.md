---
id: seo.execution.authority.backlink-profile
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
- backlink/referring-domain/mention evidence and prospect records
---
# Backlink Profile Analysis

## Purpose
Build an evidence-based view of external links, referring domains, anchors, destinations, quality, risk, and business relevance.

## Business Outcome
Understand which external references materially support discovery and authority, where meaningful weaknesses or dependencies exist, and which apparent signals are merely noise.

## Use When
Use when external-link evidence could materially inform an authority, visibility, risk, competitor, content, migration, or recovery decision.

## Process
1. Gather the strongest available backlink and referring-domain observations with source and observation time. Treat third-party indexes as partial observations rather than complete truth.
2. Normalize domains and destination URLs, deduplicate relationships where appropriate, resolve redirects/canonicals that materially affect interpretation, and preserve meaningful first/last-seen evidence when available.
3. Evaluate relationships using topical and business relevance, editorial context, audience fit, placement, destination, anchor/context, followability when observable, traffic/visibility proxies, and credible risk signals.
4. Separate likely earned/editorial value from self-created, low-value, spammy, manipulative, or genuinely unknown relationships. Raw link or domain count is not a sufficient measure of authority or business value.
5. Map meaningful links and referring sources to assets, topics, markets, and business priorities. Look for concentrated dependency, lost-value patterns, weak destination fit, or strong sources that reveal what earns references.
6. Preserve a durable baseline or create an Opportunity only when that meaning will help future work. Otherwise continue directly into the relevant authority, content, remediation, or monitoring work.

## Proportional Scope
Start with the links, domains, destinations, or changes most likely to affect the current decision. Expand when sampling cannot distinguish a systemic pattern, the stakes are high, or broader coverage could materially change the conclusion.

## Verification
- Distinguish observed links from inferred quality or causal impact.
- Do not treat third-party authority scores, link counts, or competitor link volume as proof of ranking or revenue impact.
