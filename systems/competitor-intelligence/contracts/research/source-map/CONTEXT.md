---
id: competitor.research.source-map
type: playbook
version: 1.7.0
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - social.observe
  - review.read
  - search.observe
  - document.read
  - crawler.run
  - browser.interact
  - community.read
  - news.read
context:
- Business
- Market
- AudienceSegment
- Offer
subcontracts:
  required:
  - competitor.discovery.entity-resolution
---
# Competitor Source Map

## Purpose
Map authoritative, corroborating, and high-value recurring evidence surfaces to a correctly resolved competitor identity.

## Business Outcome
Reduce rediscovery, identity mistakes, and stale facts during competitor analysis and monitoring.

## Run When
Run when onboarding a priority competitor, adding a new evidence surface, or recurring monitoring lacks reliable source coverage.

## Process
1. [AI] List required fact/evidence classes and the decision they support; use the adaptive source-coverage reference rather than assuming one fixed source list.
2. [INTEGRATION] Discover current public locations such as official product/pricing/docs/legal/release/careers/support pages, relevant social/content profiles, advertising transparency/library surfaces, review/community profiles, marketplaces, and independent/strategic sources where legitimate.
3. [HYBRID] Run competitor entity resolution before treating newly discovered domains/profiles/advertiser identities as belonging to the canonical competitor. Similar names alone are insufficient.
4. [AI] Prefer first-party sources for first-party facts and independent/customer sources where they uniquely evidence perception, outcomes, strategic movement, or corroboration. Add newly discovered credible sources when they improve the decision.
5. [HYBRID] Mark paywalled, authenticated, prohibited, unstable, region-limited, or ambiguous sources and acceptable substitutes; do not bypass access controls or call coverage complete when material sources remain inaccessible.
6. [DETERMINISTIC] Record source URL/location, identity status, evidence classes, expected update frequency, retrieval method/capability, region/coverage constraints, last verification, and freshness.
7. [AI] Rank sources by directness, freshness, reliability, and information value for the fact type, and schedule source-health checks only for priority recurring sources.

## Verification
The source map identifies both where to look and why each surface is believed to belong to the competitor, while remaining open to new sources discovered later.
