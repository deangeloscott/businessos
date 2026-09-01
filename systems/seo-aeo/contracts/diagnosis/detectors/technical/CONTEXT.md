---
id: seo.diagnosis.detectors.technical
type: detector
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
Convert crawl/index/performance observations into evidence-backed root-cause technical opportunities.

## Business Outcome
Identify systemic technical problems worth fixing without creating thousands of duplicate URL tasks or turning the detector into an automated remediation controller.

## Run When
Use when fresh relevant technical observations exist and the user/model needs to diagnose a **technical SEO opportunity/problem**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Group technical baseline/monitoring observations by plausible shared template/configuration/root cause.
2. [HYBRID] Relate affected Assets to business value, demand, traffic, index state, conversions, backlinks, and relevant change history. Exact joins are mechanical; materiality/root cause are not.
3. [AI] Assess affected scope, intentionality, severity, and the evidence for each plausible cause.
4. [AI] Prefer systemic root-cause interventions over duplicate per-URL tasks when one mechanism plausibly explains the evidence.
5. [AI] Create/update an Opportunity only when the issue is materially valuable and a plausible technical intervention exists; later method/tool choice remains with the model/harness.
6. [AI] Preserve an Incident only when actual evidence supports a severe sitewide/access/security condition requiring durable incident awareness.

## Verification
- Symptom count alone does not establish root cause or severity.
- Technical execution/remediation remains with the active model/harness and real system.

## Deterministic local-site evidence
When the scoped evidence is a local/first-party website export, do not hand-author material direct site facts from model memory or prose inspection. Run `scripts/inspect_site_evidence.py`, then persist material direct Observations through `scripts/persist_site_observation.py` using the captured fact IDs. Keep consequences, severity, and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.
