---
id: seo.execution.technical.rendering-parity
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
# Rendering & Device Parity

## Purpose
Ensure important content, links, metadata, directives, media, and task-critical interactions survive the site's delivery/rendering path across the device and crawler contexts that materially matter.

## Business Outcome
Prevent organic-discovery and user-experience failures caused by client rendering, responsive/device variation, or delivery paths that hide, omit, or break important page meaning.

## Run When
Use when JavaScript rendering, hydration/client routing, responsive/mobile behavior, device variation, or a site/platform change could alter what users or crawlers actually receive.

## Process
1. [HYBRID] Select representative high-value templates and the device/agent contexts that can materially change the answer. Compare raw/server response, rendered DOM, and user-visible output rather than assuming one representation is authoritative for every question.
2. [HYBRID] Check parity of main content, internal links/navigation, titles/meta, canonicals, robots directives, structured data, important images/video/media, alternate relationships, and other discovery-critical elements across relevant delivery states.
3. [AI] Diagnose mechanisms such as blocked resources, hydration/render failures, delayed or infinite loading, interaction-only content, client-side routing defects, lazy-loading failures, responsive hiding, device-specific omissions, intrusive overlays, viewport/layout problems, or other delivery differences.
4. [HYBRID] For mobile/device contexts, verify that important information and actions are usable rather than merely present: responsive layout, touch targets, forms, navigation, overlays, and interaction blockers should support the actual task. Keep performance-specific diagnosis in Web Performance when latency/responsiveness is the root problem.
5. [AI] Choose the smallest robust implementation fix from the actual site stack. Prefer delivery that makes critical discovery elements reliably available without unnecessary client dependencies when practical, but do not prescribe server rendering universally when another implementation is equally reliable.
6. [HYBRID] Test representative normal, slow, and relevant error paths after the change, including the device/agent contexts that exposed the defect. Verify raw/rendered/device parity and crawlability rather than assuming deployment succeeded.
7. [AI] Preserve the material defect, affected templates/contexts, and fix when remembering it improves future migration, template, or rendering work.

## Verification
- Important content and discovery signals are present and consistent in the contexts that materially matter.
- Mobile/device usability is evaluated as a real task experience, not only a viewport screenshot.
- Rendering fixes do not silently regress canonical, robots, structured data, internal links, analytics, accessibility, or important customer interactions.
- Performance claims are left to Web Performance unless actually measured here.
