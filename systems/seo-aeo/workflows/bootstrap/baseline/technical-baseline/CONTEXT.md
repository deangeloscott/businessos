---
id: seo.bootstrap.baseline.technical-baseline
type: workflow
owner_system: seo-aeo
reads:
- Asset
- Observation
writes:
- SEOAssetState
- Asset
- MetricObservation
context:
- Brand
- Business
- Market
- Offer
- ProductService
updates:
  SEOAssetState:
  - technical fields crawl indexability index structured data as applicable
---
# Technical Baseline

## Purpose
Establish the current technical conditions that materially affect search discovery, rendering, indexing, usability, or future change evaluation.

## Business Outcome
Give technical SEO work a trustworthy starting point without turning every task into a full-site crawl or producing a generic issue inventory disconnected from business value.

## Run When
Use when technical state is missing, materially stale, or needed for a concrete diagnosis, migration, optimization, or before/after comparison.

## Process
1. [HYBRID] Choose representative templates, URL classes, or a broader crawl according to site scale, uncertainty, and the actual decision. Full-site inspection is useful when justified, not a default requirement.
2. [HYBRID] Gather relevant response/status, redirect, robots, directive, canonical, hreflang, sitemap, internal-link/depth, rendering, metadata, structured-data, mobile/performance, and media evidence from whatever valid host methods are available.
3. [HYBRID] Add webmaster/index, server/log, analytics, or first-party evidence when it materially improves the picture.
4. [AI] Interpret conditions by real mechanism: discovery, crawl, render, canonicalization, index eligibility/selection, serving, user experience, conversion, or maintenance risk. Do not turn every technical difference into a defect.
5. [AI] Separate intentional configuration, unknown state, and actual failure using business/site context and evidence.
6. [HYBRID] Preserve the technical baseline and material direct Observations that future work benefits from. Create an Opportunity only when an unresolved actionable condition is worth remembering.

## Deterministic local-site evidence
When scoped evidence is a local/first-party website export, `scripts/inspect_site_evidence.py` and `scripts/persist_site_observation.py` may mechanically capture/persist material direct facts. Keep consequences, severity, and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.

## Verification
- Scope is proportionate to the decision and site complexity.
- Direct technical facts remain distinct from severity, cause, and expected impact.
- Missing tools remain evidence limitations rather than capability-registry objects.
- Specialist diagnosis or execution Workflows are optional expertise selected by the capable model/user, not required routes.
