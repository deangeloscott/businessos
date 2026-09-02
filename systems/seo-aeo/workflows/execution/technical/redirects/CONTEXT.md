---
id: seo.execution.technical.redirects
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
# Redirects

## Purpose
Design and validate redirects that preserve user journeys, discovery, and historical value when URLs genuinely move or disappear.

## Business Outcome
Move users and durable discovery signals to the closest appropriate destination without creating misleading mass redirects, chains, loops, or unnecessary URL churn.

## Run When
Use when one or more URLs are moving, consolidating, being removed, changing host/protocol/path, or otherwise require intentional redirection.

## Process
1. Identify the source URLs, reason for change, intended destination, permanence, current traffic/backlinks, conversion role, and any market/language relationships that materially affect the mapping.
2. Map each source to the closest legitimate equivalent destination. Do not redirect unrelated removed content to a homepage or broad category merely to avoid a terminal response.
3. Check for chains, loops, protocol/host hops, regex/pattern overreach, destination errors, redirect-to-noncanonical targets, and cases where no redirect is actually appropriate.
4. Prefer direct one-hop mappings and preserve genuinely removed content as an appropriate terminal state when no useful replacement exists.
5. Test representative and high-value mappings before broad changes; preserve or be able to restore the prior routing configuration when material risk justifies rollback.
6. Apply changes through the actual site/platform when the current task and permissions allow it, then crawl/test source and destination sets.
7. Update material internal links, sitemaps, canonicals, hreflang, navigation, or other owned references to point directly to the final intended URLs rather than relying indefinitely on redirects.
8. Re-check important errors, crawl/index behavior, traffic/conversion paths, and valuable backlinks where those outcomes materially matter.

## Proportionate Scope
Validate all high-value and pattern-boundary mappings; sample lower-risk homogeneous sets when the rule is well established. Expand to exhaustive mapping when a migration, regex rule, or large batch could create broad user/discovery harm.

## Verification
- Redirect destinations are contextually equivalent enough to serve the user and preserve relevant value.
- No material chains, loops, broken destinations, or contradictory canonical/internal-link signals remain.
- Broad changes have representative boundary tests and a practical recovery path when stakes justify it.
