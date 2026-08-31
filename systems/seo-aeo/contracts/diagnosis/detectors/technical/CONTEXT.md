---
id: seo.diagnosis.detectors.technical
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
  - crawler.run
  optional:
  - webpage.fetch
  - cms.page.read
  - cms.page.update
  - search.index.inspect
context:
- AudienceSegment
- Market
- Objective
- Offer
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Technical Opportunity Detector

## Purpose
Convert crawl/index/performance observations into prioritized, root-cause technical opportunities.

## Business Outcome
Detect and explain material technical opportunity early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **technical opportunity**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [HYBRID] Ingest technical baseline/monitoring issues and group occurrences by underlying template/configuration/root cause.
2. [DETERMINISTIC] Join affected assets with business value, demand, traffic, index state, conversions, backlinks, and change history.
3. [HYBRID] Estimate affected scope and whether the configuration is intentional.
4. [AI] Prioritize systemic fixes over thousands of duplicate per-URL tickets when one root cause explains them.
5. [HYBRID] Create an Opportunity with issue class, evidence, affected set, risk, and routed technical playbook.
6. [HYBRID] Escalate sitewide/access/security failures to Incident handling.
## Deterministic local-site evidence
When the scoped evidence is a local/first-party website export, do not hand-author material direct site facts from model memory or prose inspection. Run `scripts/inspect_site_evidence.py`, then persist material direct Observations through `scripts/persist_site_observation.py` using the captured fact IDs. Keep consequences, severity, and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.

