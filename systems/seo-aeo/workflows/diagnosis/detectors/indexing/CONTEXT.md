---
id: seo.diagnosis.detectors.indexing
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
Find Assets whose observed index/canonical/serving state conflicts with intended business/search state.

## Business Outcome
Separate real indexing problems from intentional states and expected propagation, then preserve a focused Opportunity only when the mismatch matters.

## Run When
Use when fresh relevant crawl/index observations exist and the user/model needs to diagnose an **indexing opportunity/problem**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Compare intended Asset/SEOAssetState index state with current crawl/index/search observations.
2. [AI] Identify valuable not-indexed, wrong-canonical, stale-indexed, unexpectedly indexed, or changed-but-not-reflected cases.
3. [HYBRID] Exclude intentional noindex/redirect/removal states and reasonable propagation windows.
4. [HYBRID] Relate discovery/internal links, duplication/content quality, technical directives, and platform diagnostics to plausible causes. Exact joins are mechanical; causal meaning is not.
5. [AI] Create/update an indexing Opportunity only when the mismatch is materially valuable and plausibly addressable; do not route execution automatically.
6. [AI] Preserve an Incident only when evidence supports a genuinely severe broad unexpected loss, not merely because multiple URLs are affected.

## Verification
- Claimed indexing state is grounded in observable crawl/index/search evidence.
- Intentional state, propagation lag, diagnosis, severity, and business impact remain distinct.

## Deterministic local-site evidence
When the scoped evidence is a local/first-party website export, do not hand-author material direct site facts from model memory or prose inspection. Run `scripts/inspect_site_evidence.py`, then persist material direct Observations through `scripts/persist_site_observation.py` using the captured fact IDs. Keep consequences, severity, and visibility implications as inference unless separately measured. Follow `core/policies/local-evidence.md`.
