---
id: seo.monitoring.competitors
type: playbook
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
- OrganicCompetitorState
- Competitor
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
updates:
  SEOAssetState:
  - organic_performance
---
# Competitor Monitoring

## Purpose
Refresh business/search/answer competitor movements that materially affect priority opportunities.

## Business Outcome
Improve valuable organic discovery through competitor monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **competitor monitoring**.

## Process
1. [HYBRID] Refresh weighted visibility, major assets, answer citations, backlinks/mentions, local/reputation, offers, and meaningful site changes for prioritized competitors.
2. [HYBRID] Detect sustained gains/losses, new assets/formats, migrations, campaigns, authority events, or category/positioning changes.
3. [HYBRID] Separate industry-wide changes from competitor-specific moves.
4. [HYBRID] Link movements to owned opportunities only when business-relevant.
5. [INTEGRATION] Send novel tactics/hypotheses to SEO ecosystem intelligence / domain-learning review rather than direct imitation.
6. [HYBRID] Update OrganicCompetitorState with timestamps/evidence and publish strategically material observations for Competitor Intelligence.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.


