---
id: seo.execution.technical.international-hreflang
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
# International & Hreflang Relationships

## Purpose
Represent legitimate language/market variants clearly enough that users and search systems can reach the appropriate version without cross-market canonical or alternate-language conflicts.

## Business Outcome
Preserve the value of genuinely localized experiences while preventing incorrect alternates, canonicals, or fallback behavior from sending discovery signals or customers to the wrong market/language version.

## Run When
Use when the business serves multiple languages or markets with separate URL/content variants and those relationships materially affect organic discovery or user experience.

## Process
1. Identify the actual locale/market variants, intended audiences, URL structure, and whether the variants are sufficiently distinct and useful to justify separate experiences.
2. Validate language/region codes and alternate relationships where hreflang is appropriate, including reciprocity and self-references when required by the implementation.
3. Check canonical behavior within each locale/market cluster so alternate pages are not inadvertently canonicalized to a different market/language version unless that is truly the intended state.
4. Verify that material localized content, Offers, currency, legal/availability information, contact details, terminology, and other customer-facing differences actually fit the target market rather than being nominally localized URLs.
5. Identify missing/incorrect alternates, unsupported combinations, redirect/canonical conflicts, fallback behavior, or locale selectors that materially impair users or discovery.
6. Apply changes through the actual site/platform when within scope, then validate representative high-value and boundary clusters rather than assuming one correct tag proves the whole implementation.

## Proportionate Scope
Validate representative locale templates and high-value market clusters first. Expand toward full pair/cluster validation when the number of locales, generation logic, migrations, or asymmetric content make sampling unsafe.

## Verification
- Alternate relationships correspond to real user-facing locale/market variants.
- Canonical and hreflang signals do not materially contradict one another.
- Localized business facts and Offers remain truthful for the target market.
- Broad implementations are tested across reciprocal and boundary cases.
