---
id: seo.monitoring.ai-visibility
type: playbook
version: 1.1.0
owner_system: seo-aeo
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
- prompt/question observations, answer text, citations, mentions, and competing sources
updates:
  SEOAssetState:
  - organic_performance
---
# AI / Answer Visibility Monitoring

## Purpose
Refresh high-value prompt observations and detect changes in brand representation, citations, competitors, and factual accuracy.

## Business Outcome
Improve valuable organic discovery through ai / answer visibility monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **AI/answer visibility monitoring**.

## Process
1. [HYBRID] Sample the weighted prompt universe across configured answer surfaces using stable measurement controls.
2. [AI] Extract mentions, recommendations, citations/links, cited assets/domains, competitors, factual claims, and referral observations.
3. [HYBRID] Compare value-weighted coverage/share with previous samples, accounting for nondeterminism and prompt-universe changes.
4. [AI] Detect material new/lost citations, recommendation shifts, competitor displacement, and inaccurate claims.
5. [DETERMINISTIC] Route to AEO detectors/playbooks and log positive patterns for SEO Domain Learning or Core Business Learning, as scope warrants.
6. [HYBRID] Keep surface-specific measurements separate; do not invent a universal AI ranking.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


