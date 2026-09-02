---
id: seo.bootstrap.baseline.ai-baseline
type: workflow
owner_system: seo-aeo
reads:
- Asset
- Observation
writes:
- SEOAssetState
- Asset
- MetricObservation
context:
- Brand
- Business
- Market
- Offer
- ProductService
evidence_inputs:
- Available AI answer and first-party evidence
- prompt/question observations, answer text, citations, mentions, and competing sources
updates:
  SEOAssetState:
  - organic_performance
---
# AI / Answer Visibility Baseline

## Purpose
Establish a reproducible starting view of how the organization and relevant competitors/sources appear across important AI-answer or conversational discovery prompts.

## Business Outcome
Create a useful comparison point for AI-answer visibility, citations, recommendations, and source presence so later changes can be interpreted against real prior evidence.

## Run When
Use when current answer-visibility state is missing, materially stale, or needed for a concrete AEO diagnosis, opportunity, change evaluation, or trend comparison. A user/runtime may invoke re-baselining; AURA does not own the schedule.

## Process
1. [HYBRID] Build or sample a representative prompt/question set from valuable demand, buyer/customer questions, and observed prompt evidence. Do not enumerate every possible wording.
2. [HYBRID] Observe the answer surfaces that materially matter and preserve prompt, surface/model context, timestamp, and other context needed to interpret nondeterministic results.
3. [AI] Extract organization/competitor mentions, recommendations, links/citations, cited URLs/domains, material factual claims, source roles, and no-answer states without treating every cited source as a business competitor.
4. [HYBRID] Summarize coverage, mention/recommendation/citation presence, repeated source patterns, and business-value weighting at the resolution useful for later comparison.
5. [AI] Preserve sampling and nondeterminism limitations. Connect direct referral or downstream first-party outcomes only where actually observable.
6. [AI] Remember the baseline observations and material gaps that future work benefits from; do not automatically create AEO Opportunities or route the results through another subsystem.

## Verification
- Exact material prompts/questions, surfaces, timestamps, answer evidence, and citation/mention status remain reproducible enough for the intended comparison.
- AI visibility, recommendations, citations, referrals, leads, and revenue remain distinct evidence stages.
- Repeated strong AI visibility can be treated as a meaningful upstream attention/opportunity signal without being mislabeled as observed downstream business outcome.
- Supporting demand, competitor, or execution methods remain optional model/user choices.
