---
id: seo.intelligence.organic-competition.domain-analysis
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- Observation
- OrganicCompetitorState
- Competitor
writes:
- OrganicCompetitorState
- MetricObservation
- Observation
- Competitor
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Competitor Domain Analysis

## Purpose
Build an interpretable domain-level model of how a materially relevant competitor earns discovery and business attention.

## Business Outcome
Understand competitor strengths and mechanisms well enough to improve owned strategy without reducing the domain to superficial scores or copying visible tactics.

## Run When
Use when a competitor has enough real overlap with the organization's important demand or answer visibility that domain-level analysis could change a decision.

## Process
1. [HYBRID] Select the competitor because of demonstrated overlap in business, search, answer, audience, or market opportunities—not merely brand prominence.
2. [HYBRID] Inspect the visible site structure, major page/asset types, topic clusters, information architecture, publishing patterns, local/market structure, conversion paths, and Offers to the depth relevant to the question.
3. [HYBRID] Combine available evidence such as search visibility, backlinks/mentions, answer citations, reputation/local state, freshness, and content patterns without treating provider metrics as ground truth.
4. [AI] Identify concentrated strengths, weaknesses, distinctive assets, and plausible mechanisms rather than collapsing performance into a synthetic authority score.
5. [AI] Keep observed facts separate from inferred strategy or causality; preserve representative pages/data for material conclusions.
6. [AI] Compare the competitor's useful strengths and gaps with the active organization's actual capabilities, positioning, assets, and business priorities. Visible competitor behavior is evidence of behavior, not proof that the tactic works or should be copied.
7. [HYBRID] Preserve only the material competitor evidence, conclusions, and unresolved questions that will improve current or future work.

## Verification
- Domain conclusions remain traceable to observable evidence.
- Observed competitor behavior, inferred strategy, and proven effectiveness remain distinct.
- Third-party metrics and proxies are not presented as first-party business outcomes.
- An Opportunity or follow-on Workflow is optional and should exist only when the resulting meaning is genuinely useful.
