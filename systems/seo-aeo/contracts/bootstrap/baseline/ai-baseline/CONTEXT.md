---
id: seo.bootstrap.baseline.ai-baseline
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
- prompt/question observations, answer text, citations, mentions, and competing sources
updates:
  SEOAssetState:
  - organic_performance
  - technical fields crawl indexability index structured data as applicable
  - internal_authority external_authority
---
# AI / Answer Visibility Baseline

## Purpose
Establish initial brand/competitor answer presence across a weighted prompt universe.

## Business Outcome
Improve valuable organic discovery through ai / answer visibility baseline, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial baseline, scheduled re-baseline, or after a material site/business change when **ai / answer visibility baseline** must be re-observed.

## Process
1. [HYBRID] Build or sample a first prompt universe from Demand Intelligence inputs and high-value buyer questions.
2. [HYBRID] Observe configured answer surfaces with reproducible timestamp/context metadata.
3. [AI] Extract brand mentions, recommendations, links/citations, cited URLs/domains, competitors, factual claims, and no-answer states.
4. [DETERMINISTIC] Calculate separate prompt coverage, mention/recommendation/citation shares weighted by business value.
5. [DETERMINISTIC] Record sampling/nondeterminism limitations and direct referral observations if analytics supports them.
6. [HYBRID] Write baseline Answer Observations and initial AEO Opportunities.

## Decisions / Routing
- Route → SEO Organic Demand Intelligence when baseline evidence needs demand interpretation.
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


