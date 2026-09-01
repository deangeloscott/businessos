---
id: competitor.analysis.competitive-position
type: playbook
owner_system: competitor-intelligence
reads:
- Competitor
- SourceProfile
- SourceRecord
- Observation
- Insight
- type: Insight
  owner_system: customer-intelligence
writes:
- Competitor
- Observation
- Insight
- Asset
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - webpage.screenshot
  - advertising.observe
  - social.observe
  - creator_content.observe
  - public_comment.read
  - review.read
  - search.observe
  - document.read
  - news.read
  - browser.interact
  - crawler.run
completion_evidence:
  profile: intelligence
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - competitor.discovery.competitive-set
  - competitor.analysis.profiling
  - competitor.analysis.benchmark
  - competitor.analysis.competitive-implications
  conditional:
  - id: competitor.analysis.pricing
    when: Pricing, packaging economics, commitment terms, implementation cost, or total-cost comparison is requested or materially affects the decision.
  - id: competitor.analysis.offer-comparison
    when: Customer-facing offers, guarantees, included value, commercial risk, or package economics materially affect the comparison.
  - id: competitor.analysis.capability-comparison
    when: Product/service capabilities or operational fit materially affect the customer decision.
  - id: competitor.analysis.positioning
    when: Positioning, messaging, category framing, promise, or differentiation is requested or materially relevant.
  - id: competitor.analysis.funnels
    when: Acquisition, conversion path, landing experience, qualification, proof, or funnel friction is requested or materially relevant.
  - id: competitor.analysis.advertising
    when: Advertising, paid creative, ad-library patterns, offers, or persuasion patterns are requested or materially relevant.
  - id: competitor.analysis.content-strategy
    when: Organic/social/content patterns, creator behavior, publishing strategy, or attention competition is requested or materially relevant.
  - id: competitor.analysis.customer-sentiment
    when: Customer praise, complaints, switching friction, reviews, or public sentiment is requested or materially relevant.
  - id: competitor.analysis.strategic-change
    when: Recent launches, pricing moves, partnerships, hiring, expansion, M&A, positioning shifts, or other strategic movement is requested or materially relevant.
  - id: competitor.analysis.tactic-validation
    when: The work would claim that an observed competitor tactic works, performs better, is profitable, or should be adapted because of apparent performance.
---
# Competitive Position & Landscape

## Purpose
Build a decision-useful competitive position by composing the existing Competitor Intelligence jobs needed for the question instead of collapsing a broad landscape request into one narrow analysis step.

## Business Outcome
Give the organization a current, evidence-backed understanding of who actually matters, how relevant competitors differ, where the business is ahead/behind/different, which whitespace is credible, and which competitive hypotheses are worth testing.

## Run When
Use when the user asks for broad competitor research, a competitive landscape/set/position, a strengths-and-weaknesses view, where the business can win, or another multi-facet competitor decision that cannot be responsibly answered by one atomic competitor job.

Do **not** use this as a mandatory wrapper around a narrow request. A request such as “compare competitor pricing” should use the focused pricing job unless broader context is genuinely required.

## Process
1. [AI] Define the business decision, target customer/job, market/geography, relevant offer/category, time horizon, and requested dimensions. Reuse the active Objective and current business/customer intelligence where it changes what “competitor” means. Establish the evidence-closure scope at the same time: which subjects and dimensions are material enough that the final position would be misleading without support or an explicit gap.
2. [HYBRID] Establish the real competitive set and comparison cohorts using the operating knowledge in `competitor.discovery.competitive-set`. Distinguish direct competitors, substitutes/status quo, emerging threats, category/aspirational benchmarks, and attention/search/channel competitors rather than flattening them into one list.
3. [HYBRID] Profile the materially relevant competitors using `competitor.analysis.profiling`. Use current authoritative sources for factual state, enough independent/third-party evidence for claims that require it, and the evidence modalities that actually carry the signal. Do not deepen every competitor equally when additional research would not change the decision. When a source is about a resolved competitor/subject, preserve matching `subject_refs` through SourceRecord → Observation → Insight so another subject's evidence cannot be attached as support by convenience.
4. [AI] Apply the conditional dimension knowledge the user explicitly requested or that could materially change the decision. Explicitly requested material dimensions must not silently disappear because a convenient source was unavailable; record the coverage gap/unknown and continue with what can be supported.
5. [HYBRID] Maintain a proportionate evidence-closure map across the material competitor/subject × requested/material dimension intersections. Use states such as `supported`, `limited`, `unknown/blocked`, or `not_material`; preserve the strongest evidence refs and important limitations for supported/limited cells. This is a stopping/quality aid, not a fixed source quota or demand to research every possible cell. If an important unsupported cell could materially change the decision and accessible evidence exists, deepen it before synthesis.
6. [HYBRID] Keep every material factual claim traceable to subject-relevant support-grade evidence at the confidence level stated. A bibliography or pool of sources detached from the claims is not sufficient provenance for a broad decision-grade synthesis. A single review/anecdote cannot establish a market-wide range or recurring sentiment. Do not manufacture precision that the evidence does not contain. If a current public price/term cannot be observed, say so rather than substituting an undated third-party figure as current fact.
7. [DETERMINISTIC] Normalize comparisons where legitimate. Preserve unit, currency, billing period, seat/technician/location assumptions, minimums, contract terms, included/excluded modules, setup/implementation costs, and observable access limitations. When unlike models cannot be normalized responsibly, compare structure rather than inventing a common number.
8. [AI] Separate **observed fact**, **strategic inference**, **customer-sentiment pattern**, **hypothesis**, and **evidence of effectiveness**. Visibility, ad longevity, engagement, repeated messaging, search presence, review prevalence, or sophistication are useful signals/proxies but are not profitability or causal proof.
9. [HYBRID] Use benchmark/strength-weakness operating knowledge to identify decision-relevant advantages, vulnerabilities, parity areas, and whitespace. A whitespace claim must be supported by the examined cohort and framed narrowly enough for the evidence; absence from a bounded sample is not proof that nobody serves the need.
10. [AI] Translate the strongest supported findings into prioritized, evidence-calibrated tactic/position hypotheses. For each material hypothesis record the evidence basis, uncertainty/assumptions, expected decision value, reversibility/urgency where relevant, what would falsify it, the measurement or next evidence needed, and the refresh trigger. Do not invent owned-product capabilities, guarantees, integrations, implementation timelines, performance targets, or outcome forecasts to make a recommendation feel concrete. A deliberately chosen success threshold/stop rule is a decision rule, not an evidence-based impact forecast; label it accordingly.
11. [AI] Preserve machine-auditable support for the broad synthesis in the smallest useful form. Include the actual method, analysis scope/evidence-closure map, literal support excerpts and resolvable refs where material, findings with evidence refs, limitations, recommended actions, comparison/normalization notes where material, and unresolved gaps. Canonical SourceRecord/Observation/Insight/Asset state may carry this support directly. If an optional Run/work receipt exists, it may reference the same material support; a Run is not required to perform, validate, or preserve this work.
12. [AI] Produce a reusable internal competitive-position Asset that makes the result understandable to a decision-maker: competitive cohorts, material competitor profiles, normalized comparisons, requested-dimension findings, strengths/weaknesses, whitespace, important unknowns/coverage gaps, prioritized hypotheses, source/freshness references, and what should be monitored next. Place source/Observation/Insight refs close enough to material factual claims that a reviewer can determine which evidence supports which conclusion.
13. [HYBRID] Use `competitor.analysis.competitive-implications` and any other relevant AURA operating knowledge directly when translating findings into Marketing, Content, SEO/AEO, Customer Optimization, product, or business implications. Do not route findings through internal AURA domain services or create duplicate foreign-domain Opportunities merely to represent composition.
14. [DETERMINISTIC] Validate canonical state and `scripts/validate_research_evidence.py` where applicable. Use structural evidence checks when they add confidence in the actual saved analysis, but do not turn them into a Run-conformance gate. Do not claim decision-grade completion while a material conclusion outruns its subject-relevant evidence; deepen research, narrow/downgrade the conclusion, or leave the gap explicit. Preserve current evidence/snapshot dates and create/update SourceProfiles or refresh triggers only where future change could materially alter the decision.

## Completion Standard
The work is complete when a competent business decision-maker can use the result without rebuilding the core competitive research: the relevant set is justified, requested/material dimensions are actually investigated or visibly marked limited/unknown, the evidence-closure map is proportionate to the decision, comparisons are normalized appropriately, material factual claims resolve to subject-relevant support-grade evidence, effectiveness claims are not inferred from weak proxies, strategic implications are actionable but not overclaimed, and the useful evidence/state is durably reusable by AURA.
