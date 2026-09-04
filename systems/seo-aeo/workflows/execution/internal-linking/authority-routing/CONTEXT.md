---
id: seo.execution.internal-linking.authority-routing
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
# Internal Authority Routing

## Purpose
Use internal-link prominence to support strategically important pages when those links are also genuinely useful to users.

## Business Outcome
Strengthen discovery and navigational prominence for valuable destinations without creating irrelevant or manipulative internal-link patterns.

## Use When
Use when important pages appear underlinked relative to their role, when stronger source pages have relevant contextual relationships, or when internal prominence is misaligned with business and user value.

## Process
1. Identify high-value target pages and plausible source pages with real topical, navigational, or journey relationships.
2. Inspect current inlinks, source prominence, context, depth, competing targets, and where users would naturally benefit from another path.
3. Prioritize links that improve the next step for the user as well as discovery. Reject placements whose only justification is transferring abstract 'authority.'
4. Choose the source, target, anchor/context, and placement that best fits the actual relationship. Preserve natural language, accessibility, and meaningful hierarchy.
5. If impact is uncertain, change the smallest useful set first and verify important source/target behavior before broadening. A ChangeEvent is useful only when remembering the material change helps later work.
6. Measure relevant crawl, visibility, click, conversion, or journey effects when they matter to the decision. Do not assume internal-link changes caused an outcome merely because metrics moved afterward.

## Proportional Scope
Focus on targets and source relationships with the strongest business/user relevance. Expand only when evidence suggests a broader internal-prominence pattern needs correction.
