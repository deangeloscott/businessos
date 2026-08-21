---
id: seo.bootstrap.baseline.technical-baseline
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- Asset
- Observation
writes:
- SEOAssetState
- Asset
- MetricObservation
capabilities:
  required:
  - none
  optional:
  - none
context:
- Brand
- Business
- Market
- Offer
- ProductService
evidence_inputs:
- Effective Capability Profile
- Available search analytics local authority AI
updates:
  SEOAssetState:
  - organic_performance
  - technical fields crawl indexability index structured data as applicable
  - internal_authority external_authority
---
# Technical Baseline

## Purpose
Measure current technical search accessibility and site architecture before changes.

## Business Outcome
Improve valuable organic discovery through technical baseline, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial baseline, scheduled re-baseline, or after a material site/business change when **technical baseline** must be re-observed.

## Process
1. [INTEGRATION] Crawl representative/full accessible site according to scale and resource controls.
2. [HYBRID] Collect response/status, redirects, robots, meta directives, canonicals, hreflang, sitemaps, internal links, depth, rendering, metadata, structured data, mobile/performance fields, and media references.
3. [DETERMINISTIC] Join with webmaster/index observations and server/log evidence where available.
4. [AI] Classify issues by actual impact pathway: discovery, crawl, render, canonical, index, serving, user experience, conversion, or maintenance risk.
5. [HYBRID] Separate intentional configurations from defects using Brand Context/site type.
6. [HYBRID] Write technical baseline plus Opportunities only for material actionable conditions.

## Decisions / Routing
- Route → SEO Organic Demand Intelligence when baseline evidence needs demand interpretation.
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


