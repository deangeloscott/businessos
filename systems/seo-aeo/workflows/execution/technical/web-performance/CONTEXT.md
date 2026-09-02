---
id: seo.execution.technical.web-performance
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
# Web Performance

## Purpose
Improve real-user loading, responsiveness, and visual stability by diagnosing the performance bottlenecks that materially affect user experience or business outcomes.

## Business Outcome
Make important pages and journeys faster and more stable where performance is actually consequential, without chasing synthetic scores or named thresholds for their own sake.

## Run When
Use when field evidence, lab diagnostics, user behavior, or a material site change indicates that page performance may be limiting experience, conversion, crawl efficiency, or organic discovery.

## Process
1. [HYBRID] Establish the relevant user paths and representative templates. Prefer real-user field evidence where available and use lab diagnostics to explain or reproduce problems rather than treating either source as complete truth.
2. [HYBRID] Segment only where it can change the diagnosis—such as page/template type, device, geography, connection quality, browser, or logged-in state—to distinguish systemic issues from isolated ones.
3. [HYBRID] Inspect the mechanisms that plausibly create latency or instability: server/backend timing, network waterfall, render-blocking resources, JavaScript execution, third-party scripts, API latency, caching/compression, media, fonts, asset weight, layout shifts, and interaction work. Use Core Web Vitals or other current experience metrics as useful evidence, not as the definition of the problem.
4. [AI] Rank bottlenecks by actual user/business impact, prevalence, template leverage, reversibility, and expected value of fixing them. Do not optimize a metric when the change is unlikely to materially improve the experience or objective.
5. [HYBRID] Apply technically appropriate changes such as removing/replacing/defering expensive resources, improving server or API work, caching/compression, media/font optimization, code splitting, loading strategy, layout reservation, or interaction handling. The host/model chooses implementation from the actual stack and tools available.
6. [HYBRID] Test functionality, visual integrity, content, analytics, consent/ads, monetization, accessibility, and other important behavior that performance changes could accidentally break.
7. [HYBRID] Compare before/after representative journeys using the strongest available evidence. Lab changes may be visible immediately; field evidence may require its natural reporting window. AURA may remember the measurement intent, but the harness owns any later recheck schedule.

## Verification
- Performance work is tied to real users, important templates/journeys, or a credible organic/business mechanism rather than score chasing.
- Field and lab evidence are distinguished and interpreted in context.
- Improvement does not silently regress functionality, tracking, content, monetization, accessibility, or visual quality.
- Claims about outcome improvement match what was actually measured.
