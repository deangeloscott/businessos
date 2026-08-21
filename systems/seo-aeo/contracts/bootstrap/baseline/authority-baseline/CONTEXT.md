---
id: seo.bootstrap.baseline.authority-baseline
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
- backlink/referring-domain/mention evidence and prospect records
- review mention reputation response history
updates:
  SEOAssetState:
  - organic_performance
  - technical fields crawl indexability index structured data as applicable
  - internal_authority external_authority
---
# Authority and Reputation Baseline

## Purpose
Establish external references, mentions, reviews, trust sources, and competitor context.

## Business Outcome
Improve valuable organic discovery through authority and reputation baseline, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial baseline, scheduled re-baseline, or after a material site/business change when **authority and reputation baseline** must be re-observed.

## Process
1. [HYBRID] Ingest backlinks/referring domains, unlinked mentions, significant third-party profiles, ratings/reviews, press/community references, and authority-provider observations.
2. [DETERMINISTIC] Normalize and classify by topic, source type, legitimacy, destination, context, location/market, and business relevance.
3. [HYBRID] Measure distribution and trend rather than relying on one synthetic authority score.
4. [HYBRID] Compare with relevant competitors at domain/topic/asset level.
5. [AI] Identify link/mention/reputation gaps and concentration risks.
6. [HYBRID] Write baseline state and only create Opportunities with plausible legitimate interventions.

## Decisions / Routing
- Route → SEO Organic Demand Intelligence when baseline evidence needs demand interpretation.
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


