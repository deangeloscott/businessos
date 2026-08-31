---
id: seo.diagnosis.detectors.indexing
type: detector
version: 1.1.0
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
writes:
- Opportunity
capabilities:
  required:
  - search.index.inspect
  optional:
  - search.index.request
  - cms.page.read
  - crawler.run
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Indexing Opportunity Detector

## Purpose
Find assets whose observed index/canonical/serving state conflicts with intended business/search state.

## Business Outcome
Detect and explain material indexing opportunity early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **indexing opportunity**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Compare intended Asset / SEOAssetState index state with current crawl/index/search observations.
2. [AI] Identify valuable not-indexed, wrong-canonical, stale-indexed, unexpectedly indexed, or changed-but-not-reflected cases.
3. [HYBRID] Exclude intentional noindex/redirect/removal states and expected lag windows.
4. [DETERMINISTIC] Join discovery/internal links, duplication/content quality, technical directives, and platform diagnostics.
5. [HYBRID] Create index-troubleshooting or deindex-removal Opportunities with evidence.
6. [HYBRID] Escalate broad unexpected losses as mass-deindexing Incident.
## Deterministic local-site evidence
When the scoped evidence is a local/first-party website export, do not hand-author material direct site facts from model memory or prose inspection. Run `scripts/inspect_site_evidence.py`, then persist material direct Observations through `scripts/persist_site_observation.py` using the captured fact IDs. Keep consequences, severity, and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.

