---
id: seo.diagnosis.traffic-decay
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
- Observation
writes:
- Opportunity
- Incident
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- traffic time series landing page dimensions conversion
---
# Organic Traffic Loss Diagnosis & Recovery

## Purpose
Determine whether valuable organic traffic has materially declined, separate the possible mechanisms, and guide proportionate recovery without assuming ranking loss.

## Business Outcome
Protect qualified organic acquisition and downstream value by distinguishing demand, visibility, click behavior, indexing/technical, analytics, site availability, migration, conversion-path, and other causes before acting.

## Run When
Use when current evidence or the user indicates a meaningful decline in qualified organic visits or related business outcomes. The same Workflow applies from localized decay to a severe broad collapse; severity changes urgency and depth rather than creating a separate incident method.

## Process
1. [HYBRID] Verify that the apparent movement is real. Check analytics/tagging/data-source health and compare qualified organic sessions/users/landing-page visits with appropriate prior, YoY, seasonal, or rolling windows and independent search-performance evidence where available.
2. [HYBRID] Define the materially affected scope and onset using only dimensions that help explain the problem: landing pages/topics, market/geography, device, branded/nonbrand, new/returning, conversion action, or other relevant segmentation.
3. [HYBRID] Decompose traffic into the evidence-supported mechanisms that can change it: underlying demand, ranking/visibility, CTR/SERP layout, index/access/site availability, migration or other site changes, analytics/tracking, landing or conversion-path behavior, and other material business changes.
4. [AI] Separate correlation from cause and preserve an unknown state when the evidence does not yet distinguish contributors. Organic traffic loss does not by itself prove lost demand, ranking decline, technical failure, or a content problem.
5. [HYBRID] Compare timing with relevant ChangeEvents, deployments, migrations, technical/index changes, search-result changes, competitor movement, seasonality, campaigns/business changes, and measurement changes when they could plausibly explain the loss.
6. [AI] Rank plausible controllable contributors by evidence, business impact, reversibility, and expected value of intervention. For severe loss, prioritize containment of high-confidence reversible causes; recommend pausing or reverting likely harmful recent changes only when evidence and rollback safety justify it. The active user/harness owns real execution.
7. [HYBRID] Apply or recommend the smallest useful recovery matched to the diagnosed mechanism rather than creating a generic traffic-recovery task. Use relevant SEO/AEO or other business methods directly when the cause lies elsewhere.
8. [HYBRID] Re-check qualified traffic, search evidence, and downstream conversion/value after enough time for the mechanism to respond. Preserve an Opportunity when a valuable addressable improvement exists and an Incident only when durable visibility for a genuinely severe event helps continuity.
9. [AI] Preserve material root cause, intervention, outcome, unresolved uncertainty, stakeholder-relevant context, and reusable Learning when supported. AURA records organizational meaning; it does not freeze or resume the host runtime.

## Verification
- Analytics, search visibility, and conversion evidence are reconciled where relevant before concluding the business lost demand or rankings.
- Traffic, demand, visibility, CTR/SERP, indexing/technical, tracking, site availability, and conversion-path effects remain distinct.
- Severe-loss containment recommendations are evidence-backed and distinguished from actions actually executed.
- Recovery claims use subsequent evidence and do not overstate causality.
