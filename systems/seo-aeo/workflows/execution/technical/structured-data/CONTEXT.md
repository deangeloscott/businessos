---
id: seo.execution.technical.structured-data
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
# Structured Data

## Purpose
Use structured data where it accurately represents page content, entities, and business facts and can improve machine understanding or eligible search experiences.

## Business Outcome
Make important content easier for search and answer systems to interpret without overstating what the page or business actually contains, offers, or proves.

## Use When
Use this Workflow when structured data is relevant to the page, entity, content type, or organic-discovery problem being addressed. Do not add markup merely because a schema type exists.

## Process
1. Determine the page's real purpose, visible content, represented entities, and the search/answer understanding that structured data could legitimately improve.
2. Select only structured-data types and properties that are appropriate to that content and currently useful for the surfaces that matter to the business.
3. Map markup to verified visible content and established business facts. Do not invent or embellish entities, claims, ratings, reviews, prices, availability, offers, relationships, or other properties to make markup more complete.
4. Prefer the simplest maintainable implementation that fits the site's existing architecture. Avoid duplicate, conflicting, or unnecessarily fragmented markup.
5. Validate syntax, entity/property relationships, and any applicable eligibility requirements. Validation confirms technical correctness, not that a search engine will display a particular result or that the markup will improve performance.
6. Inspect the rendered page or final implementation where possible to confirm that the markup actually shipped as intended and still matches what users can see or otherwise legitimately verify.
7. If the user requested implementation and the active host has the necessary access, make the change and verify it. Otherwise produce a precise implementation-ready recommendation or artifact without claiming deployment occurred.
8. Revisit markup when material page/business facts or relevant platform requirements change. AURA may remember that monitoring matters; the host/runtime owns any actual recurring schedule or alerting.

## Proportional Scope
Start with the pages, templates, entities, or errors most likely to matter to the business outcome. Expand when broader coverage could materially change the diagnosis, prevent systemic inconsistency, or capture meaningful additional discovery value.
