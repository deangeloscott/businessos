# Web Technical & Machine-Readable Patterns

> Optional web craft notes. Open this only when it materially helps the selected track or page; the track files and dialect file remain usable without loading the notes.
>
> Preserves performance, semantic, structured-data, and machine-discoverability guidance; verify current platform behavior before implementation.

## Technical & Machine Discoverability Patterns

A web page that loads slowly or cannot be parsed by the intended systems can become an economic liability. Use the following as implementation patterns and measurable targets, then verify the actual artifact in the real deployment context.

### 1. Core Web Vitals (CWV) Targets
* **Largest Contentful Paint (LCP):** Set a target from the current Core Web Vitals guidance and the page's measured baseline. A 1.8-second budget can be a useful stretch target for a critical commerce page, but it is not a universal guarantee.
  * When the hero image is the LCP candidate, it often should not be lazy-loaded and may benefit from an explicit preload:
    ```html
    <link rel="preload" as="image" href="/hero.webp" fetchpriority="high">
    <img src="/hero.webp" alt="Primary Specimen" fetchpriority="high" loading="eager" width="800" height="600">
    ```
* **Interaction to Next Paint (INP):** Keep the main thread clear during interaction. Defer or isolate non-critical scripts where the host stack supports it, and measure the deployed experience. A 100ms budget is an ambitious target rather than a promise.
* **Cumulative Layout Shift (CLS):** Reserve space for images, video, and iframes with dimensions or `aspect-ratio`; zero is an excellent goal, while the actual result must be measured at relevant breakpoints.

### 2. The Speculation Rules API (Eligible Prefetch/Prerender)
Modern browsers can predictively prefetch or prerender eligible navigations. The browser, response headers, device resources, privacy rules, navigation eligibility, and application behavior determine whether this happens; it is not an instant or 0ms navigation guarantee. Use it only for likely, safe navigations and measure cost and benefit:
```html
<script type="speculationrules">
{
  "prerender": [
    {
      "source": "list",
      "urls": ["/checkout", "/products/flagship-model"],
      "eagerness": "moderate"
    }
  ]
}
</script>
```

### 3. Machine-Readable Product and Service Information (`/llms.txt` as an Optional Convention)
To make important information easier for crawlers, assistants, and procurement systems to inspect, provide accurate semantic HTML, stable URLs, a sitemap, structured data, and clear documentation. A root `/llms.txt` file is an optional proposal that some consumers may use; it cannot ensure discovery, citation, or recommendation:
```markdown
# [Brand Name]

> [1-sentence concise description of category, value proposition, and core products]

## Core Products / Services
- [Product Alpha](/products/alpha): [Detailed specifications, pricing, materials, return terms]
- [Service Beta](/services/beta): [Deliverables, turnaround time, qualification requirements]

## Technical Documentation & Data Endpoints
- [Full Machine-Readable Catalog](/llms-full.txt)
- [API / Developer Documentation](/docs/api)
```

Treat every structured field and catalog entry as a customer-facing claim: keep price, availability, ratings, credentials, and specifications current and supported.

---
