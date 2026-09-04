---
id: seo.execution.architecture.multilingual-architecture
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
---
# Multilingual / Multiregional Architecture

## Purpose
Represent languages and markets so people reach the intended localized experience and discovery systems can understand the relationships between versions.

## Business Outcome
Support useful market-specific discovery and conversion without treating localization as blind translation or creating conflicting regional versions.

## Use When
Use when the business serves multiple languages, countries, or regions and the site architecture, localization, alternates, or market-specific journeys need to be designed or corrected.

## Process
1. Establish the languages, countries/regions, currencies, legal or policy differences, offers, operations, and existing localized URLs that actually matter to the business.
2. Choose a durable URL and locale structure that fits the site's platform and organizational ownership. Avoid automatic redirects or locale assumptions that prevent users or crawlers from reaching another legitimate version.
3. Map which assets are true equivalents, which need market-specific adaptation, and which should not exist in every locale. Do not assume that translating every source page produces a useful localized experience.
4. Define coherent alternate/hreflang relationships, canonicals, language or market selectors, sitemaps, and internal links where applicable. Use the dedicated Hreflang Workflow when annotation mechanics are the core problem.
5. Validate localized intent, terminology, factual claims, offers, legal/commercial details, metadata, and conversion paths with market-specific evidence or appropriate review. Do not present machine translation or inferred terms as verified local business truth.
6. Test representative localized journeys for discoverability, rendering, index eligibility, selection behavior, and business-critical actions after changes.

## Proportional Scope
Focus on the markets, locale pairs, and templates with material business value or known risk. Expand when shared architecture or systemic annotation patterns make broader review decision-relevant.
