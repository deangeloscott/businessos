---
id: seo.monitoring.backlinks
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- MetricObservation
- Opportunity
- Incident
- SEOAssetState
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
  - local_profile.read
schedule:
  class: recurring
  default: daily
  configurable: true
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
updates:
  SEOAssetState:
  - organic_performance
---
# Backlink and Mention Monitoring

## Purpose
Track meaningful new/lost/changed external references and authority opportunities.

## Business Outcome
Improve valuable organic discovery through backlink and mention monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **backlink and mention monitoring**.

## Process
1. [DETERMINISTIC] Refresh link/mention observations and normalize source/target state.
2. [HYBRID] Verify significant new/lost references and distinguish provider noise, redirects, site migrations, spam, and true editorial changes.
3. [HYBRID] Attribute earned links/mentions to outreach/PR/assets where evidence supports it.
4. [HYBRID] Route recoverable valuable losses, unlinked mentions, competitor gaps, or harmful anomalies to authority/incident workflows.
5. [HYBRID] Update source quality/relevance observations without overreacting to synthetic authority score changes.
6. [HYBRID] Measure referral/business value and topic relevance alongside counts.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.

## Verification
- Target relevance and legitimacy over raw link volume; preserve outreach provenance and opt-out/compliance requirements.


