---
id: seo.monitoring.search-reputation
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
- review mention reputation response history
updates:
  SEOAssetState:
  - organic_performance
---
# Reputation Monitoring

## Purpose
Track review, rating, sentiment, profile, and high-visibility brand-claim changes.

## Business Outcome
Improve valuable organic discovery through reputation monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **reputation monitoring**.

## Process
1. [HYBRID] Refresh review/mention/profile observations by location/product/source.
2. [HYBRID] Detect material rating shifts, review spikes/drops, recurring negative themes, response backlog, misinformation, impersonation, or viral exposure.
3. [AI] Assess reach/severity/business impact and privacy/legal risk.
4. [HYBRID] Route normal reviews/themes to reputation playbooks and crisis/high-risk states to Incident response.
5. [HYBRID] Feed trust/reputation changes into Local/AEO/Search Opportunities when they affect discovery/choice.
6. [HYBRID] Track resolution and recurrence by root cause.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.


